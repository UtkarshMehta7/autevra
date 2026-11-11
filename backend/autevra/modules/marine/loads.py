"""Vessel load cases, compliance rows, production stations and a stack-up.

Loads (stated, concept level): hydrostatic pressure at the keel rho g T; still-water
bending moment estimated as the displacement weight times the length over 35 (a rough
small-craft figure; a real check integrates the weight and buoyancy curves); propeller
thrust from the viscous resistance at the design speed (a lower bound, see the hull
module). Compliance: the IMO IS Code general criteria computed from the GZ curve; the
scantling and small-craft stability standards are references still to show.
"""

from autevra.marine import hull as hk
from autevra.modules import Values
from autevra.modules.marine.vessel import spec_of
from autevra.product.loads import Compliance, LoadAt, LoadCase
from autevra.quality import Contributor, Stack


def cases(values: Values) -> list[LoadCase]:
    s = spec_of(values)
    hs = hk.hydrostatics(s)
    disp_n = hs["displacement_t"] * 1000 * hk.G
    p_keel = hk.RHO_SW * hk.G * s.draft
    res = hk.resistance(s)
    return [
        LoadCase(id="hydrostatic", name="Hydrostatic pressure at the design draft",
                 kind="operating", factors={"draft_m": s.draft},
                 method="rho g T at the keel", results={"keel_pressure_kpa": p_keel / 1000},
                 loads=[LoadAt(location="bottom plating at the keel", fz=round(p_keel))]),
        LoadCase(id="still_water", name="Still-water bending (estimate)", kind="limit",
                 factors={"divisor": 35.0}, method="displacement weight x L / 35 (rough "
                 "small-craft estimate)", results={"bending_knm": disp_n * s.length / 35 / 1e3},
                 loads=[LoadAt(location="midship section", my=round(disp_n * s.length / 35))]),
        LoadCase(id="thrust", name="Propeller thrust at the design speed", kind="operating",
                 factors={"speed_kn": s.speed_kn}, method="viscous resistance (lower bound)",
                 results={"thrust_n": res["viscous_resistance_n"]},
                 loads=[LoadAt(location="thrust bearing", fx=round(res["viscous_resistance_n"]))]),
    ]  # fmt: skip


def compliance(values: Values) -> list[Compliance]:
    crit = hk.imo_criteria(spec_of(values))
    failed = [c for c in crit if not c["pass"]]
    return [
        Compliance(clause="IMO IS Code 2008, Part A 2.2", requirement="general intact "
                   "stability criteria (GZ areas, GZ at 30°, angle of maximum, GM0)",
                   means="analysis", evidence=f"{len(crit) - len(failed)} of {len(crit)} met "
                   "from the computed GZ curve", status="shown" if not failed else "not shown"),
        Compliance(clause="IMO IS Code 2008, Part A 2.3", requirement="severe wind and rolling "
                   "(weather) criterion", means="analysis", evidence="not yet computed",
                   status="open"),
        Compliance(clause="ISO 12215-5", requirement="small-craft hull scantlings",
                   means="analysis", evidence="design pressures and plate sizing planned",
                   status="open"),
        Compliance(clause="COLREG Annex I", requirement="positions of navigation lights",
                   means="inspection", evidence="light positions not yet placed", status="open"),
    ]  # fmt: skip


STATIONS = (("SFI 100", "Hull fabrication"), ("SFI 200", "Machinery installation"),
            ("SFI 300", "Machinery installation"), ("SFI 500", "Outfitting"),
            ("SFI 600", "Outfitting"), ("SFI 400", "Commissioning"))  # fmt: skip
ORDER = ("Hull fabrication", "Machinery installation", "Outfitting", "Commissioning")


def stackups(values: Values) -> list[Stack]:
    """Engine coupling to shaft alignment (vertical offset at the coupling face)."""
    return [Stack(name="Shaft alignment at the coupling", lsl=-0.15, usl=0.15, contributors=[
        Contributor(name="engine bed top (machined after welding)", nominal=500.0, plus=0.05,
                    minus=0.05),
        Contributor(name="engine mount height (adjustable chocks)", nominal=120.0, plus=0.05,
                    minus=0.05),
        Contributor(name="gearbox output centre height", nominal=180.0, plus=0.03, minus=0.03),
        Contributor(name="stern tube centre height", nominal=800.0, plus=0.08, minus=0.08,
                    direction=-1),
    ])]  # fmt: skip
