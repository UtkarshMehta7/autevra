"""The automotive engineering domain module.

Everything specific to road vehicles lives here: parameters, derived physics, design rules,
CAD builders, the vehicle assembly, solvers, component tests, integration checks and the
specification interview. The shared core (``autevra.core``, ``autevra.assembly``,
``autevra.cad``, ``autevra.engineering``) knows none of it; this module registers it into
the core registries through the same extension API plugins use.

Importing the package registers the domain once (idempotent).
"""

from autevra import extensions
from autevra.domains.automotive import (
    builders,
    derived,
    integration,
    interior,
    language,
    parameters,
    powertrain,
    rules,
    spec,
    vehicle,
)
from autevra.domains.automotive import tests as test_definitions

DOMAIN_ID = "automotive"

PLUGIN = extensions.Plugin(
    name=DOMAIN_ID,
    version="1.0.0",
    description="Road vehicles: ladder-frame template with body, frame, axles, wheels and "
    "coil-over dampers; suspension, longitudinal and packaging analysis.",
    parameters=parameters.DEFINITIONS,
    group_aliases=parameters.GROUP_ALIASES,
    derived=tuple(derived.DEFINITIONS.values()),
    rules=tuple(rules.DEFINITIONS),
    builders={
        "body": builders.build_body,
        "glass": builders.build_glass,
        "head_lamps": builders.build_head_lamps,
        "tail_lamps": builders.build_tail_lamps,
        "seats": interior.build_seats,
        "dashboard": interior.build_dashboard,
        "display": interior.build_display,
        "steering_wheel": interior.build_steering_wheel,
        "console": interior.build_console,
        **{
            name: getattr(powertrain, f"build_{name}")
            for name in (
                "engine",
                "gearbox",
                "fuel_tank",
                "exhaust",
                "radiator",
                "traction_battery",
                "front_motor",
                "rear_motor",
                "inverters",
                "charger",
                "charge_port",
                "hv_cables",
                "battery_12v",
                "ecus",
                "harness",
            )
        },  # fmt: skip
        "frame": builders.build_frame,
        "axle": builders.build_axle,
        "wheel": builders.build_wheel,
        "damper": builders.build_damper,
    },
    components=vehicle.COMPONENTS,
    coincidences=vehicle.COINCIDENCES,
    load_paths=vehicle.LOAD_PATHS,
    compatible_interfaces=integration.COMPATIBLE,
    clearances=integration.CLEARANCES,
    tests=test_definitions.DEFINITIONS,
    integration_checks=(
        integration.travel_checks,
        integration.interior_checks,
        integration.platform_checks,
    ),
    notes=integration.NOT_CHECKED,
    language=language.LANGUAGE,
    templates=tuple(spec.project_templates()),
)


def register() -> None:
    if DOMAIN_ID not in extensions.LOADED:
        extensions.register(PLUGIN)


register()
