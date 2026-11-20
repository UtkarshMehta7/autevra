"""Process FMEA generated from the process plan.

Every made part gets the generic failure modes of its process, and every fitted part the
generic modes of assembly, each with its usual cause, a prevention control and a detection
control. Ratings (1-10):
- severity: the mode's generic severity by what it harms (appearance 3, fit 5, function
  7, strength 8); for function and strength modes it is raised to the worst design-FMEA
  severity of the logical block the part realises, so a process escape on a part whose
  design failure is rated 10 is rated 10 too (the link from design FMEA to process FMEA);
- occurrence and detection: generic ratings of the process and of the stated control.
These are starting ratings to be replaced by the plant's own capability and inspection
data; they are not measured values. Priority uses the same simplified rule as the design
FMEA (product/systems.py), not the AIAG-VDA action-priority table.
"""

from pydantic import BaseModel

from autevra.manufacturing import Operation
from autevra.product.systems import Architecture, FailureMode

SEVERITY = {"appearance": 3, "fit": 5, "function": 7, "strength": 8}

# process -> (mode, effect, harms, cause, prevention, detection, occurrence, detection rating)
Row = tuple[str, str, str, str, str, str, int, int]
# fmt: off
MODES: dict[str, list[Row]] = {
    "sheet metal": [
        ("split or thinning in the draw", "panel cracks in service", "strength",
         "blank-holder force or lubrication off", "forming simulation; press force monitor",
         "thinning check on first-off and per coil", 4, 4),
        ("springback out of tolerance", "panel does not fit its neighbours", "fit",
         "material strength varies by coil", "over-crown compensation in the die",
         "checking fixture, sampled", 5, 4),
        ("surface low or dent", "visible surface defect", "appearance",
         "dirt on the die; handling", "die cleaning interval; racks",
         "highlight inspection", 5, 5),
    ],
    "casting": [
        ("gas or shrinkage porosity", "reduced strength; leak path", "strength",
         "melt hydrogen; feeding of thick sections", "degassing; solidification simulation",
         "X-ray sampling; leak test where sealed", 5, 6),
        ("cold shut or misrun", "incomplete section", "strength",
         "low melt or die temperature", "temperature windows monitored",
         "visual inspection of every part", 3, 4),
        ("dimension out after heat treatment", "machining stock or fit lost", "fit",
         "distortion in quench", "quench fixture", "CMM sampling", 4, 4),
    ],
    "forging": [
        ("lap or fold", "crack starter under fatigue load", "strength",
         "preform shape; die wear", "die-fill simulation; die life count",
         "magnetic-particle inspection", 3, 4),
        ("wrong heat-treatment condition", "strength below the allowable", "strength",
         "furnace load or time off", "furnace charts per batch", "hardness test per batch",
         3, 3),
    ],
    "machining": [
        ("dimension out of tolerance", "part does not assemble or seal", "fit",
         "tool wear; thermal drift", "tool-life count; warm-up cycle",
         "in-process probing; gauge", 4, 3),
        ("surface finish too rough", "seal or bearing life reduced", "function",
         "worn insert; chatter", "insert change interval", "roughness sampling", 3, 5),
        ("burr left on an edge", "debris in the system; cut hazard", "function",
         "no deburr operation on the feature", "deburr in the cycle", "visual inspection",
         4, 5),
    ],
    "moulding": [
        ("short shot", "incomplete part", "fit", "low pack pressure; blocked vent",
         "cavity-pressure monitoring", "weight check; vision", 3, 3),
        ("sink mark or warpage", "visible defect; clips do not line up", "fit",
         "cooling uneven; thick ribs", "mould-flow study; cooling balance",
         "checking fixture, sampled", 4, 5),
        ("weak weld line", "cracks at a clip or boss", "strength",
         "flow fronts meet cold", "gate position from the flow study",
         "destructive test per shift", 3, 6),
    ],
    "extrusion": [
        ("section out of tolerance", "joint gap or misfit", "fit", "die wear; pull speed",
         "die correction interval", "profile gauge, sampled", 4, 4),
        ("twist or bow over length", "does not sit in the fixture", "fit",
         "uneven cooling; stretch", "stretcher setting", "straightness table", 4, 4),
    ],
    "weldment": [
        ("lack of fusion or undersize weld", "joint fails under load", "strength",
         "torch angle; fit-up gap; current", "weld procedure qualified; seam tracking",
         "visual every weld; sectioning or ultrasonic, sampled", 4, 6),
        ("distortion", "mounting points out of position", "fit",
         "heat input and sequence", "weld sequence; clamping fixture", "CMM on mounts", 5, 4),
        ("missed weld", "joint missing", "strength", "program or manual skip",
         "weld count interlock", "weld-count check", 2, 3),
    ],
    "composite": [
        ("ply misoriented or missing", "stiffness and strength off the laminate design",
         "strength", "manual lay-up error", "laser ply projection; ply book sign-off",
         "ply count record per part", 4, 6),
        ("void or porosity", "interlaminar strength reduced", "strength",
         "vacuum leak; cure pressure", "bag leak check before cure",
         "ultrasonic C-scan", 4, 4),
        ("delamination from trimming", "edge crack growth", "strength",
         "worn router; feed too high", "tool-life count", "tap test or ultrasonic at edges",
         3, 5),
    ],
    "tube": [
        ("ovality or wrinkle at a bend", "flow restriction; fatigue crack", "function",
         "mandrel worn or bend too tight", "bend radius rule; mandrel interval",
         "ball gauge; visual", 3, 4),
        ("end form out of tolerance", "joint leaks", "function", "tool wear",
         "tool-life count", "go/no-go gauge; leak test", 3, 3),
    ],
    "additive": [
        ("lack-of-fusion porosity", "fatigue strength reduced", "strength",
         "laser power, gas flow or powder condition", "qualified parameter set; powder lots",
         "CT sampling; witness coupons per build", 4, 6),
        ("distortion off the plate", "machining stock lost", "fit",
         "residual stress; supports", "build simulation; stress relief before removal",
         "3D scan", 4, 4),
    ],
}
FIT: list[Row] = [
    ("fastener under-torqued or missed", "joint loosens in service", "function",
     "tool calibration; operator skip", "DC tool with angle monitoring and count",
     "torque and angle recorded per joint", 3, 3),
    ("wrong variant fitted", "function or option not as ordered", "function",
     "similar parts at the station", "pick-to-light; part scan", "scan against the build order",
     3, 3),
    ("damaged while fitting", "visible damage or early failure", "appearance",
     "handling; tool contact", "protective covers; fitting aid", "visual at end of station",
     4, 5),
]

# fmt: on


class ProcessFailure(BaseModel):
    part: str
    name: str
    station: str
    step: str  # the process, or "fit" for the assembly step
    mode: str
    effect: str
    cause: str
    prevention: str
    detection_control: str
    severity: int
    severity_from: str  # "generic" or the design failure mode that set it
    occurrence: int
    detection: int
    rpn: int
    priority: str


def _priority(s: int, o: int, d: int) -> str:
    return FailureMode(id="x", function="x", block="x", mode="x", effect="x", severity=s,
                       occurrence=o, detection=d).priority  # fmt: skip


def generate(operations: list[Operation], templates: dict[str, str],
             arch: Architecture | None = None) -> list[ProcessFailure]:  # fmt: skip
    """Process FMEA rows for a plan. ``templates`` maps a part id to its part template, the
    key by which the architecture's blocks (and their design failure modes) are found."""
    worst: dict[str, tuple[int, str]] = {}  # template -> (severity, design mode)
    if arch is not None:
        by_block: dict[str, tuple[int, str]] = {}
        for m in arch.failure_modes:
            if m.severity > by_block.get(m.block, (0, ""))[0]:
                by_block[m.block] = (m.severity, m.mode)
        for b in arch.blocks:
            if b.id in by_block:
                for t in b.templates:
                    if by_block[b.id][0] > worst.get(t, (0, ""))[0]:
                        worst[t] = by_block[b.id]
    out = []
    for op in operations:
        design = worst.get(templates.get(op.part, ""), (0, ""))
        steps = [] if op.bought_out else [(op.process, r) for r in MODES.get(op.process, [])]
        steps += [("fit", r) for r in FIT]
        for step, (mode, effect, harms, cause, prev, det, o, d) in steps:
            s, source = SEVERITY[harms], "generic"
            if harms in ("function", "strength") and design[0] > s:
                s, source = design
            out.append(ProcessFailure(
                part=op.part, name=op.name, station=op.station, step=step, mode=mode,
                effect=effect, cause=cause, prevention=prev, detection_control=det,
                severity=s, severity_from=source, occurrence=o, detection=d, rpn=s * o * d,
                priority=_priority(s, o, d)))  # fmt: skip
    order = {"high": 0, "medium": 1, "low": 2}
    return sorted(out, key=lambda r: (order[r.priority], -r.rpn, r.name))


def summary(rows: list[ProcessFailure]) -> dict:
    by_priority = {p: sum(r.priority == p for r in rows) for p in ("high", "medium", "low")}
    stations: dict[str, dict[str, int]] = {}
    for r in rows:
        st = stations.setdefault(r.station, {"high": 0, "medium": 0, "low": 0, "max_rpn": 0})
        st[r.priority] += 1
        st["max_rpn"] = max(st["max_rpn"], r.rpn)
    return {"rows": len(rows), "by_priority": by_priority, "stations": stations,
            "linked_to_design": sum(r.severity_from != "generic" for r in rows)}  # fmt: skip
