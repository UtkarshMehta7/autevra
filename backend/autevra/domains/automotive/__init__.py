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
    language,
    parameters,
    rules,
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
    integration_checks=(integration.travel_checks,),
    notes=integration.NOT_CHECKED,
    language=language.LANGUAGE,
)


def register() -> None:
    if DOMAIN_ID not in extensions.LOADED:
        extensions.register(PLUGIN)


register()
