"""Part templates: the contract every part generator implements, in a registry keyed by
module (a project only ever sees its own module's templates).

M1 implements the contract's identity, process, functions and mass estimator; geometry
generators per maturity level, rules, load cases, joints, failure modes and manufacturing
data are added by later milestones (docs/PART_CATALOGUE.md, section 3).
"""

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field

PROCESSES = ("sheet metal", "casting", "forging", "machining", "moulding", "composite",
             "extrusion", "weldment", "tube", "additive", "glass", "assembly",
             "standard", "inventory")  # fmt: skip

# (design values, instance count) -> (mass of all instances in kg, basis of the estimate)
Estimator = Callable[[Mapping[str, float], int], tuple[float, str]]


@dataclass(frozen=True)
class PartTemplate:
    id: str
    module: str
    name: str
    code: str  # breakdown code pattern in the module's standard
    process: str
    functions: tuple[str, ...] = ()
    estimator: Estimator | None = None  # None: mass is allocated from the parent budget
    max_maturity: int = 0  # the highest level the template's generators reach today
    description: str = ""
    tags: tuple[str, ...] = field(default=())

    def __post_init__(self) -> None:
        if self.process not in PROCESSES:
            raise ValueError(f"template '{self.id}': unknown process '{self.process}'")


_REGISTRY: dict[str, dict[str, PartTemplate]] = {}


def register(*templates: PartTemplate) -> None:
    for t in templates:
        by_module = _REGISTRY.setdefault(t.module, {})
        if t.id in by_module and by_module[t.id] != t:
            raise ValueError(f"template '{t.id}' already registered in module '{t.module}'")
        by_module[t.id] = t


def of(module: str) -> dict[str, PartTemplate]:
    """The templates of one module (empty if none)."""
    return dict(_REGISTRY.get(module, {}))


def get(module: str, template_id: str) -> PartTemplate:
    try:
        return _REGISTRY[module][template_id]
    except KeyError:
        raise KeyError(f"no template '{template_id}' in module '{module}'") from None
