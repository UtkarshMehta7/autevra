"""Automotive integration checks: clearance pairs, interface kinds and wheel travel."""

from collections.abc import Mapping

from autevra.domains.automotive import derived as d
from autevra.engineering.integration import Check, Clearance, Status

Values = Mapping[str, float]

COMPATIBLE = (
    ("axle_mount", "centre"), ("hub", "hub"), ("shock", "lower_eye"), ("shock_tower", "upper_eye"),
)  # fmt: skip

_TYRE = ("rim_diameter", "tyre_width", "tyre_aspect_ratio")
CLEARANCES: tuple[Clearance, ...] = tuple(
    item
    for c, axle in (("fl", "front"), ("fr", "front"), ("rl", "rear"), ("rr", "rear"))
    for item in (
        Clearance(f"wheel_{c}", "body", 5.0, "tyre must not touch the body at ride height",
                  ("arch_clearance", *_TYRE)),
        Clearance(f"wheel_{c}", "frame", 30.0, "frame rail clearance to the tyre",
                  ("rail_spacing", "rail_width", f"track_{axle}", "tyre_width")),
        Clearance(f"wheel_{c}", f"damper_{c}", 20.0, "coil-over clearance to the tyre",
                  ("spring_coil_diameter", f"{axle}_spring_rate", "rail_spacing",
                   f"track_{axle}", "tyre_width")),
        Clearance(f"damper_{c}", "frame", 5.0, "coil-over clearance to the frame",
                  ("rail_spacing", "rail_height", "ground_clearance")),
    )
)  # fmt: skip


def travel_checks(values: Values) -> list[Check]:
    """Warnings when the packaging, not the suspension, sets the usable wheel travel."""
    out = []
    for a in d.AXLES:
        limits = d.travel_limits(values, a)
        for kinds, label, name in (
            (d.BUMP_LIMITS, "bump", "bump_stop"), (d.REBOUND_LIMITS, "rebound", "droop")
        ):  # fmt: skip
            governing = min(kinds, key=lambda k: limits[k][0])
            value, param = limits[governing]
            design = limits[name][0]
            if governing == name:
                message = f"{a} {label} travel {value:.1f} mm is set by the suspension"
                out.append(Check(
                    f"travel:{a}_{label}", "travel", Status.PASS, message,
                    parameters=(param,), measured=round(value, 3), unit="mm",
                ))  # fmt: skip
                continue
            out.append(Check(
                f"travel:{a}_{label}", "travel", Status.WARNING,
                f"{a} {label} travel is limited to {value:.1f} mm by the "
                f"{governing.replace('_', ' ')} ({param}), below the {design:.0f} mm "
                f"{name.replace('_', ' ')} travel",
                parameters=(param, limits[name][1]), measured=round(value, 3), limit=design,
                unit="mm",
            ))  # fmt: skip
    return out


NOT_CHECKED: tuple[str, ...] = (
    "Parts packaged inside the body envelope (axles, dampers) are not checked against the body: "
    "the body is a solid envelope, not a shell.",
    "Clearances are static (ride height, straight ahead); wheel travel and steering sweeps are "
    "covered by the suspension tests and a later steering sweep check.",
)


HEADROOM_MIN = 25.0  # mm, below this the check warns (allowance-based, not a regulation)


def interior_checks(values: Values) -> list[Check]:
    """Front-row headroom from the seated-height allowance (see ``interior``)."""
    room = d.front_headroom(values)
    ok = room >= HEADROOM_MIN
    message = (
        f"front headroom {room:.0f} mm"
        + ("" if ok else f": a large adult's head is within {HEADROOM_MIN:.0f} mm of the roof"
           if room >= 0 else ": a large adult's head would touch the roof")
    )  # fmt: skip
    return [Check("interior:front_headroom", "packaging", Status.PASS if ok else Status.WARNING,
                  message, parameters=("overall_height", "ground_clearance", "rail_height"),
                  measured=round(room, 1), limit=HEADROOM_MIN, unit="mm")]  # fmt: skip


def platform_checks(values: Values) -> list[Check]:
    """A skateboard platform without a traction battery is allowed (so the platform can be
    chosen before the powertrain) but flagged: its floor is sized for a pack."""
    if d.chassis(values) == "skateboard" and d.powertrain(values) == "combustion":
        message = ("skateboard platform with a combustion powertrain: the floor is sized for "
                   "a battery that is not fitted")  # fmt: skip
        return [Check("platform:skateboard_battery", "packaging", Status.WARNING, message,
                      parameters=("chassis_type", "powertrain_type"))]  # fmt: skip
    return []
