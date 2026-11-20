"""Machine elements: closed-form checks taken from the feature test catalogue
(docs/test-cases, areas JNT and ELM) and from the published worked examples."""

import math

import pytest
from fastapi.testclient import TestClient

from autevra.elements import fatigue, gears, joints, springs

rel = pytest.approx


@pytest.mark.parametrize(
    ("d", "p", "grade", "k", "a_s", "fi", "t"),
    [
        (3, 0.5, "8.8", 0.12, 5.0308, 2.6261, 0.9454),  # JNT-0001
        (3, 0.5, "12.9", 0.2, 5.0308, 4.3919, 2.6352),  # JNT-0009
        (16, 2.0, "12.9", 0.2, 156.67, 136.77, 437.67),  # JNT-0072
        (20, 2.5, "8.8", 0.2, 244.79, 132.19, 528.76),  # JNT-0075 (Sp 600 above M16)
        (24, 3.0, "10.9", 0.2, 352.5, 263.32, 1263.9),  # JNT-0087
    ],
)
def test_bolt_preload_and_torque(d, p, grade, k, a_s, fi, t):
    out = joints.bolt_joint(joints.BoltJointIn(d=d, pitch=p, grade=grade, nut_factor=k))
    assert out["stress_area_mm2"] == rel(a_s, rel=2e-4)
    assert out["preload_kN"] == rel(fi, rel=2e-4)
    assert out["torque_Nm"] == rel(t, rel=2e-4)


def test_joint_stiffness_and_load_sharing():
    j = joints.BoltJointIn(d=12, pitch=1.75, grip=40, threaded_in_grip=10, load_kN=20)
    out = joints.bolt_joint(j)
    a_d, a_t = math.pi / 4 * 144, out["stress_area_mm2"]
    kb = a_d * a_t * j.e_bolt / (a_d * 10 + a_t * 30)
    assert out["kb_N_per_mm"] == rel(kb)
    c = out["joint_constant"]
    assert 0.1 < c < 0.5  # members stiffer than the bolt
    assert out["bolt_load_kN"] == rel(out["preload_kN"] + c * 20)
    assert out["member_load_kN"] == rel(out["preload_kN"] - (1 - c) * 20)
    assert out["separation_load_kN"] == rel(out["preload_kN"] / (1 - c))


def test_joint_separates_under_large_load():
    out = joints.bolt_joint(joints.BoltJointIn(d=6, pitch=1.0, preload_fraction=0.3, load_kN=12))
    assert out["member_load_kN"] < 0
    assert any("separates" in w for w in out["warnings"])


def test_friction_grip_slip():
    out = joints.bolt_joint(joints.BoltJointIn(d=10, pitch=1.5, shear_kN=50, friction=0.2))
    assert out["slip_resistance_kN"] == rel(0.2 * out["preload_kN"])
    assert any("slips" in w for w in out["warnings"])


@pytest.mark.parametrize(
    ("leg", "length", "force", "tau", "flag"),
    [(3, 50, 10, 94.281, False), (3, 50, 50, 471.41, True)],
)
def test_fillet_weld_throat_shear(leg, length, force, tau, flag):  # JNT-0091/0092
    out = joints.fillet_weld(joints.FilletWeldIn(leg=leg, length=length, force_kN=force))
    assert out["throat_mm"] == rel(2.1213, rel=1e-4)
    assert out["tau"] == rel(tau, rel=1e-4)
    assert any("allowable" in w for w in out["warnings"]) is flag


def test_weld_directional_method():
    # transverse: sigma_perp = tau_perp = F / (sqrt2 a L); equivalent = sqrt(4) * that
    out = joints.fillet_weld(
        joints.FilletWeldIn(leg=6, length=200, force_kN=100, direction="transverse")
    )
    a = 6 * math.sqrt(0.5)
    s = 100e3 / (math.sqrt(2) * a * 200)
    assert out["sigma_perp"] == rel(s)
    assert out["equivalent"] == rel(2 * s)
    assert out["limit"] == rel(490 / (0.9 * 1.25))
    assert out["capacity_kN"] == rel(100 / out["utilisation"])


@pytest.mark.parametrize(
    ("sut", "se", "sa", "sm", "n"),
    [
        (400, 140, 50, 0, 2.8),
        (1200, 420, 150, 200, 1.909),
        (1200, 420, 250, 100, 1.474),
        (1200, 600, 100, 300, 2.4),
        (1200, 600, 250, 200, 1.714),
    ],
)
def test_goodman(sut, se, sa, sm, n):  # JNT-0157, 0263, 0266, 0276, 0283
    f = fatigue.safety_factors(sa, sm, se, sut, 0.8 * sut)
    assert f["goodman"] == rel(n, abs=1e-3)


def test_mean_stress_criteria_ordering():
    f = fatigue.safety_factors(100, 150, 250, 700, 500)
    # Gerber is the least conservative, Soderberg the most (for these numbers)
    assert f["soderberg"] < f["goodman"] < f["gerber"]
    assert f["asme_elliptic"] == rel(1 / math.sqrt((100 / 250) ** 2 + (150 / 500) ** 2))
    assert f["langer"] == rel(500 / 250)
    # compressive mean: no credit
    assert fatigue.safety_factors(100, -200, 250, 700, 500)["goodman"] == rel(2.5)


def test_marin_factors_shigley_example():
    # Shigley ex. 6-3/6-4: machined, Sut 520 MPa -> ka = 4.51 * 520^-0.265 = 0.860;
    # 32 mm rotating bending -> kb = 1.24 * 32^-0.107 = 0.856
    end = fatigue.endurance(fatigue.FatigueIn(sut=520, sy=400, surface="machined", diameter=32))
    assert end["ka"] == rel(0.860, abs=1e-3)
    assert end["kb"] == rel(0.856, abs=1e-3)
    assert end["Se_prime"] == 260
    assert fatigue.endurance(fatigue.FatigueIn(sut=1600, sy=1400))["Se_prime"] == 700
    assert fatigue.endurance(fatigue.FatigueIn(loading="axial"))["kb"] == 1.0
    assert fatigue.reliability_factor(99) == 0.814
    assert fatigue.temperature_factor(20) == rel(1.0, abs=2e-3)


def test_sn_life():
    # Shigley ex. 6-2: Sut 1050 MPa, Se 525 -> f = 0.9 gives a = 1701, b = -0.0851;
    # at 700 MPa fully reversed N = (700 / a)^(1/b)
    a, b = fatigue.sn_constants(1050, 525)
    assert a == rel(1701, rel=1e-3)
    assert b == rel(-0.0851, rel=2e-3)
    assert fatigue.cycles_to_failure(700, 1050, 525) == rel((700 / a) ** (1 / b))
    assert fatigue.cycles_to_failure(500, 1050, 525) == math.inf


def test_rainflow_astm_e1049_example():
    cycles = fatigue.rainflow([-2, 1, -3, 5, -1, 3, -4, 4, -2])
    totals: dict[float, float] = {}
    for c in cycles:
        totals[c["range"]] = totals.get(c["range"], 0) + c["count"]
    assert totals == {3: 0.5, 4: 1.5, 6: 0.5, 8: 1.0, 9: 0.5}


def test_miner_damage():
    out = fatigue.damage(
        fatigue.HistoryIn(series=[0, 400, 0, 400, 0], sut=800, se=200, repeats=1000)
    )
    # two zero-based 0..400 cycles (sa = sm = 200 -> sar = 200 / (1 - 0.25) = 266.7 MPa)
    life = fatigue.cycles_to_failure(200 / 0.75, 800, 200)
    assert out["damage_per_pass"] == rel(2 / life)
    assert out["damage"] == rel(2000 / life)


@pytest.mark.parametrize(("n", "k"), [(4, 0.15488), (6, 0.10326), (10, 0.061953), (15, 0.041302)])
def test_spring_rate(n, k):  # ELM-0001..0004
    out = springs.spring(springs.SpringIn(d=0.5, D=10, n=n, shear_modulus=79300, free_length=30))
    assert out["rate_N_per_mm"] == rel(k, rel=1e-4)
    assert out["index"] == 20


def test_spring_index_warning_and_solid():  # ELM-0005
    out = springs.spring(springs.SpringIn(d=0.5, D=20, n=4, free_length=40))
    assert any("outside 4–20" in w for w in out["warnings"])
    s = springs.spring(springs.SpringIn(d=2, D=16, n=8, free_length=60, ends="closed-ground"))
    assert s["solid_length"] == 20 and s["total_coils"] == 10
    c = 8.0
    assert s["bergstrasser"] == rel((4 * c + 2) / (4 * c - 3))
    assert s["wahl"] == rel((4 * c - 1) / (4 * c - 4) + 0.615 / c)


@pytest.mark.parametrize(
    ("m", "z1", "z2", "a", "under"),
    [
        (1, 12, 20, 16, True),
        (1, 17, 100, 58.5, False),
        (8, 20, 100, 480, False),
        (8, 30, 20, 200, False),
        (8, 12, 60, 288, True),
    ],
)
def test_gear_pair_geometry(m, z1, z2, a, under):  # ELM-0097, 0104, 0204, 0205, 0195
    out = gears.pair(gears.GearPairIn(module=m, z1=z1, z2=z2))
    assert out["gear1"]["d"] == m * z1 and out["gear2"]["d"] == m * z2
    assert out["centre_distance"] == rel(a)
    assert out["ratio"] == rel(z2 / z1)
    assert any("Undercut" in w for w in out["warnings"]) is under


def test_gear_contact_ratio_and_shift():
    out = gears.pair(gears.GearPairIn(module=2, z1=20, z2=40))
    # textbook: z 20/40, 20 deg, standard -> eps ~ 1.64
    assert out["contact_ratio"] == rel(1.635, abs=2e-3)
    shifted = gears.pair(gears.GearPairIn(module=2, z1=12, z2=30, x1=0.3, x2=0.2))
    inv_w = gears.inv(math.radians(20)) + 2 * math.tan(math.radians(20)) * 0.5 / 42
    assert gears.inv(math.radians(shifted["working_pressure_angle"])) == rel(inv_w)
    assert shifted["centre_distance"] == rel(
        42 * math.cos(math.radians(20)) / math.cos(math.radians(shifted["working_pressure_angle"]))
    )
    assert not any("Undercut" in w for w in shifted["warnings"])  # x1 0.3 >= 0.298


def test_gear_loads():
    out = gears.pair(
        gears.GearPairIn(module=2, z1=20, z2=40, face_width=20, torque_Nm=50, rpm=1500)
    )
    assert out["tangential_force_N"] == rel(2500)
    assert out["bending_pinion"] == rel(out["Kv"] * 2500 / (20 * 2 * 0.322))
    assert out["Z_H"] == rel(2.495, abs=1e-3)
    assert out["power_kW"] == rel(50 * 1500 * 2 * math.pi / 60 / 1000)


def test_tooth_outline_symmetric_and_bounded():
    pts = gears.tooth_outline(2, 20, 0.0, 20, 44, 35)
    xs = sorted(round(x, 6) for x, _ in pts)
    assert xs == sorted(round(-x, 6) for x, _ in pts)
    assert max(math.hypot(x, y) for x, y in pts) == rel(22, rel=1e-6)


def test_api_and_gear_parts(client: TestClient):
    c = client
    assert c.post("/api/elements/spring", json={"d": 2, "D": 16, "n": 8}).status_code == 200
    out = c.post("/api/elements/gears", json={"module": 2, "z1": 18, "z2": 42}).json()
    assert len(out["gear1"]["outline"]) > 10
    bad = c.post("/api/elements/gears", json={"module": 2, "z1": 18, "z2": 42, "bore1": 40})
    assert bad.status_code == 422
    pid = c.post("/api/projects", json={"name": "Gears", "domain": "machinery"}).json()["id"]
    parts = c.post(
        f"/api/projects/{pid}/elements/gears", json={"module": 2, "z1": 12, "z2": 20, "bore1": 6}
    ).json()
    assert [p["document"]["name"] for p in parts] == ["Pinion z12 m2", "Gear z20 m2"]
    assert parts[1]["document"]["at"]["x"] == rel(32)


def test_vdi2230_permissible_preload_and_torque():
    v = joints.VdiIn(d=14, pitch=1.5, grade="10.9", mu_thread=0.12, mu_head=0.12)
    out = joints.vdi2230(v)
    # VDI 2230 table A1 lists about 95 kN for M14x1.5 10.9 at mu_G 0.12
    assert out["F_M_zul_kN"] == rel(95.0, rel=0.01)
    d2 = out["d2"]
    lever = 0.16 * 1.5 + 0.58 * d2 * 0.12 + out["D_Km"] / 2 * 0.12
    assert out["torque_Nm"] == rel(out["F_M_zul_kN"] * lever)
    assert out["torque_Nm"] == rel(out["thread_torque_Nm"] + out["head_torque_Nm"])
    assert out["F_M_min_kN"] == rel(out["F_M_zul_kN"] / 1.6)
    assert out["embedding_um"] == 7.0  # thread 3 + head 2.5 + one inner interface 1.5


def test_vdi2230_flags_slip_and_surface_pressure():
    slip = joints.vdi2230(joints.VdiIn(shear_kN=20, mu_interface=0.1))
    assert slip["F_K_req_kN"] == rel(200) and any("Residual clamp" in w for w in slip["warnings"])
    soft = joints.vdi2230(joints.VdiIn(member="AlMgSi1 F31", head_bearing=17))
    assert soft["p_max"] > soft["p_G"] and any("hardened washer" in w for w in soft["warnings"])
    better = joints.vdi2230(joints.VdiIn(alpha_a=1.1))  # angle-controlled tightening
    assert better["F_KR_min_kN"] > joints.vdi2230(joints.VdiIn())["F_KR_min_kN"]


def test_suspension_spring_from_ride_frequency():
    s = springs.SuspensionIn(corner_mass_kg=400, ride_hz=1.3, tyre_rate=250, motion_ratio=0.9)
    out = springs.suspension_spring(s)
    kr = 400 * (2 * math.pi * 1.3) ** 2 / 1000
    assert out["ride_rate"] == rel(kr)
    assert out["wheel_rate"] == rel(kr * 250 / (250 - kr))
    assert out["spring_rate"] == rel(out["wheel_rate"] / 0.81)
    d, big_d = out["wire_d"], 110.0
    assert out["active_coils"] == rel(77_200 * d**4 / (8 * big_d**3 * out["spring_rate"]))
    assert out["tau_bump"] <= out["allowable"]
    # one size thinner would be overstressed: the wire is the smallest that works
    c = big_d / (d - 0.1)
    kb = (4 * c + 2) / (4 * c - 3)
    assert (
        kb * 8 * out["bump_force_N"] * big_d / (math.pi * (d - 0.1) ** 3)
        > 0.55 * 1974 / (d - 0.1) ** 0.108
    )
    assert 3 < out["mass_kg"] < 7 and out["surge_hz"] > 25
    with pytest.raises(ValueError):
        springs.suspension_spring(springs.SuspensionIn(tyre_rate=20, ride_hz=3))
