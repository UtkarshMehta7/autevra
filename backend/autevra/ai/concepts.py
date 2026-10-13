"""Automotive concepts behind vague or out-of-model requests.

These turn such requests into honest, specific questions instead of guesses.
"Make the suspension softer" names a modelled system but not a quantity: it
could mean spring rate, bump (compression) damping or rebound damping.
"Fit bigger brakes" names a system that is not modelled yet. The scope check
keeps the assistant on automotive design and engineering.
"""

import re
from dataclasses import dataclass

from autevra.ai import lexicon as lx


@dataclass(frozen=True)
class Concept:
    id: str
    words: tuple[str, ...]
    meanings: tuple[str, ...]  # the engineering quantities the words can refer to
    phase: str  # roadmap phase where it becomes editable
    modelled: bool = False  # True: editable parameters exist, the request is just ambiguous


CONCEPTS: tuple[Concept, ...] = (
    Concept(
        "suspension",
        (
            "suspension",
            "ride",
            "spring",
            "springs",
            "damper",
            "dampers",
            "damping",
            "shock",
            "shocks",
            "shock absorber",
            "coilover",
            "coilovers",
        ),
        (
            "spring rate (N/mm)",
            "bump (compression) damping (N·s/m)",
            "rebound damping (N·s/m)",
            "ride height (ground clearance)",
        ),
        "now",
        modelled=True,
    ),
    Concept(
        "brakes",
        ("brake", "brakes", "braking", "disc", "discs", "rotor", "rotors", "caliper", "calipers"),
        ("brake disc diameter", "disc thickness", "caliper piston area"),
        "Phase 5 (brakes)",
    ),
    Concept(
        "engine",
        (
            "engine",
            "motor",
            "horsepower",
            "power",
            "torque",
            "displacement",
            "turbo",
            "cylinder",
            "cylinders",
            "piston",
            "pistons",
            "crankshaft",
        ),
        ("power and torque targets", "displacement", "engine envelope dimensions"),
        "Phase 3 (specification) and Phase 5 (powertrain geometry)",
    ),
    Concept(
        "transmission",
        (
            "gearbox",
            "transmission",
            "gear",
            "gears",
            "gear ratio",
            "final drive",
            "differential",
            "clutch",
        ),
        ("gear ratios", "final drive ratio", "gearbox envelope"),
        "Phase 5 (gearbox) and Phase 6 (powertrain simulation)",
    ),
    Concept(
        "steering_system",
        ("steering ratio", "steering rack", "rack", "tie rod", "tie rods", "ackermann"),
        ("steering ratio", "rack travel", "Ackermann geometry"),
        "Phase 5 (steering); max steer angle is editable now",
    ),
    Concept(
        "appearance",
        (
            "colour",
            "color",
            "paint",
            "red",
            "blue",
            "black",
            "white",
            "silver",
            "chrome",
            "glossy",
            "matte",
        ),
        ("material appearance",),
        "later (appearance is kept separate from engineering geometry)",
    ),
)

SOFTER = frozenset(
    {
        "softer",
        "soft",
        "stiffer",
        "stiff",
        "firmer",
        "firm",
        "harder",
        "comfier",
        "sportier",
        "plusher",
    }
)

# Vocabulary that marks a request as automotive even when no parameter matches.
_AUTOMOTIVE_WORDS = frozenset(
    {
        "car",
        "hub",
        "hubs",
        "road",
        "tarmac",
        "vehicle",
        "it",
        "chassis",
        "frame",
        "body",
        "axle",
        "axles",
        "wheel",
        "wheels",
        "tyre",
        "tyres",
        "tire",
        "tires",
        "cabin",
        "roof",
        "bonnet",
        "hood",
        "boot",
        "trunk",
        "door",
        "doors",
        "bumper",
        "fender",
        "arch",
        "arches",
        "design",
        "model",
        "suv",
        "sedan",
        "hatchback",
        "pickup",
        "truck",
        "coupe",
        "drivetrain",
        "awd",
        "fwd",
        "rwd",
        "simulation",
        "simulate",
        "test",
        "acceleration",
        "cornering",
        "stopping",
        "pothole",
        "potholes",
        "speed",
        "drag",
        "aero",
        "aerodynamic",
        "step",
        "export",
        "cad",
    }
)


def _words(text: str) -> set[str]:
    return set(re.findall(r"[a-z]+", text.lower()))


def find(text: str) -> Concept | None:
    t = text.lower()
    for concept in CONCEPTS:
        for w in concept.words:
            if re.search(rf"(?<![a-z]){re.escape(w)}(?![a-z])", t):
                return concept
    return None


def clarification(concept: Concept, text: str) -> tuple[str, list[str]]:
    words = _words(text)
    if concept.id == "suspension" and words & SOFTER:
        softer = bool(words & {"softer", "soft", "comfier", "plusher"})
        verb = "reduce" if softer else "increase"
        question = (
            f"'{'Softer' if softer else 'Stiffer'}' could mean the spring rate, the bump "
            "(compression) damping or the rebound damping, front, rear or both. Which one do "
            "you mean, and by how much?"
        )
        return question, [
            f"{verb} the spring rate by 10%",
            f"{verb} the bump damping by 10%",
            f"{verb} the rebound damping by 10%",
        ]
    if concept.modelled:
        meanings = ", ".join(concept.meanings)
        return (
            f"Which {concept.id.replace('_', ' ')} quantity should change: {meanings}? "
            "Say front, rear or both, and the amount.",
            [],
        )
    meanings = ", ".join(concept.meanings)
    question = (
        f"That refers to {concept.id.replace('_', ' ')} ({meanings}), which is not an "
        f"editable parameter yet; it is planned for {concept.phase}."
    )
    return question, []


def is_automotive(text: str) -> bool:
    """True if the text plausibly concerns the vehicle design (conservative: errs inward)."""
    words = _words(text)
    if words & _AUTOMOTIVE_WORDS:
        return True
    if find(text) is not None:
        return True
    if any(alias in text.lower() for alias in lx.ALIASES):
        return True
    verbs = lx.INCREASE_VERBS | lx.DECREASE_VERBS | lx.SET_VERBS | set(lx.COMPARATIVES)
    return bool(words & verbs) or bool(re.search(r"\d", text))
