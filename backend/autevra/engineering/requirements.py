"""Requirements as first-class engineering records, and their verification from evidence.

Two kinds:
- ``performance``: a limit on a test metric (e.g. rear peak body acceleration over the road
  hump <= 6 m/s²). Verified by **test**: the criterion takes part in the test verdict, and
  the requirement is verified only by current runs (inputs unchanged since the run).
- ``text``: a statement with no machine-checkable form (typically imported from another
  tool). Tracked and linked, verified manually; never reported as verified automatically.
- ``design``: a limit on a design parameter or derived value (e.g. ground clearance >= 150
  mm, front ride frequency <= 1.5 Hz). Verified by **analysis** or **inspection**: evaluated
  deterministically on the current design.

Verification status: ``verified`` (all evidence current and passing), ``failed``,
``stale`` (evidence exists but the design changed since), ``not_verified`` (no evidence),
``not_approved`` (provisional; takes no part in verdicts), ``manual`` (text
requirements). Statuses describe the model;
they are evidence for, not a claim of, compliance with any standard.
"""

from collections.abc import Callable, Iterable, Mapping
from datetime import UTC, datetime
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field, model_validator

from autevra.domain import derived as d
from autevra.domain.parameters import REGISTRY
from autevra.domain.units import UnitError, convert, parse_unit
from autevra.engineering import testing as tst

Values = Mapping[str, float]
Comparator = Literal["<=", "<", ">=", ">"]
COMPARATOR_WORDS = {"<=": "at most", "<": "below", ">=": "at least", ">": "above"}


class Requirement(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex[:12])
    key: str = ""  # human-readable identifier, e.g. REQ-003 (assigned on creation if empty)
    title: str = ""
    text: str = ""  # the requirement statement; generated if empty
    rationale: str = ""
    kind: Literal["performance", "design", "text"] = "performance"
    verification: Literal["test", "analysis", "inspection"] = "test"
    priority: Literal["must", "should", "may"] = "must"
    parent: str | None = None  # id of the requirement this one refines
    approved: bool = True
    source: str = "user"  # user | reqif | system
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    # performance
    test_id: str | None = None
    target: str = "*"  # front | rear | *
    scenario_id: str = "*"
    metric: str | None = None
    # design
    quantity: str | None = None  # parameter or derived value id
    # both
    comparator: Comparator = "<="
    limit: float = 0.0
    unit: str = ""
    note: str = ""

    @model_validator(mode="after")
    def _consistent(self) -> "Requirement":
        if self.kind == "text":
            if not self.text:
                raise ValueError("a text requirement needs its statement")
            if self.verification == "test":
                self.verification = "inspection"
        elif self.kind == "performance":
            self.test_id = self.test_id or "quarter_car"
            definition = tst.DEFINITIONS.get(self.test_id)
            if definition is None or self.metric not in definition.metrics:
                raise ValueError(f"unknown test or metric: {self.test_id} / {self.metric}")
            if self.target not in (*definition.targets, "*"):
                raise ValueError(f"unknown target '{self.target}'")
            if self.scenario_id != "*":
                try:
                    definition.scenario(self.scenario_id)
                except KeyError as exc:
                    raise ValueError(str(exc).strip("'\"")) from None
            if self.verification != "test":
                raise ValueError("performance requirements are verified by test")
            metric_unit = definition.metrics[self.metric][1]
            if self.unit and self.unit != metric_unit:
                raise ValueError(f"{self.metric} is in '{metric_unit}', not '{self.unit}'")
            self.unit = metric_unit
        else:
            if self.quantity not in REGISTRY and self.quantity not in d.DERIVED:
                raise ValueError(f"unknown parameter or derived value '{self.quantity}'")
            if self.verification == "test":
                self.verification = "analysis"
            self.limit = self.limit_in_quantity_unit()
            self.unit = quantity_unit(self.quantity)
        if not self.text:
            self.text = statement(self)
        if not self.title:
            self.title = self.text[:80]
        return self

    def limit_in_quantity_unit(self) -> float:
        """The limit converted to the quantity's own unit (units must be compatible)."""
        assert self.quantity is not None
        own = quantity_unit(self.quantity)
        if not self.unit or self.unit == own:
            return self.limit
        try:
            return convert(self.limit, parse_unit(self.unit), parse_unit(own))
        except UnitError as exc:
            raise ValueError(f"{self.quantity}: {exc}") from None

    def as_test_requirement(self) -> tst.Requirement | None:
        """The criterion form used in test verdicts (performance requirements only)."""
        if self.kind != "performance":
            return None
        assert self.test_id is not None and self.metric is not None
        return tst.Requirement(
            id=self.id,
            test_id=self.test_id,
            target=self.target,
            scenario_id=self.scenario_id,
            metric=self.metric,
            comparator=self.comparator,
            limit=self.limit,
            unit=self.unit,
            approved=self.approved,
            note=self.key,
        )


def quantity_unit(quantity: str) -> str:
    if quantity in REGISTRY:
        return str(REGISTRY[quantity].unit)
    return d.DERIVED[quantity].unit


def quantity_label(quantity: str) -> str:
    return REGISTRY[quantity].label if quantity in REGISTRY else d.DERIVED[quantity].label


def quantity_value(quantity: str, values: Values) -> float:
    return values[quantity] if quantity in REGISTRY else d.compute(quantity, values)


def statement(r: Requirement) -> str:
    words = COMPARATOR_WORDS[r.comparator]
    unit = f" {r.unit}" if r.unit else ""
    if r.kind == "design":
        assert r.quantity is not None
        return f"The {quantity_label(r.quantity).lower()} shall be {words} {r.limit:g}{unit}."
    definition = tst.DEFINITIONS[r.test_id or ""]
    label = definition.metrics[r.metric or ""][0].lower()
    corner = "each corner" if r.target == "*" else f"the {r.target} corner"
    where = (
        "in every scenario"
        if r.scenario_id == "*"
        else f"in the {definition.scenario(r.scenario_id).label} scenario"
    )
    return (
        f"The {label} of {corner} shall be {words} {r.limit:g}{unit} {where} ({definition.name})."
    )


def linked_parameters(r: Requirement) -> list[str]:
    """Design parameters that can change whether the requirement holds."""
    if r.kind == "text":
        return []
    if r.kind == "design":
        assert r.quantity is not None
        if r.quantity in REGISTRY:
            return [r.quantity]
        return list(d.DERIVED[r.quantity].controlled_by)
    definition = tst.DEFINITIONS[r.test_id or ""]
    targets = definition.targets if r.target == "*" else (r.target,)
    return list(dict.fromkeys(p for t in targets for p in definition.inputs(t)))


def linked_cases(r: Requirement) -> list[tuple[str, str, str]]:
    """(test, target, scenario) cases that verify a performance requirement."""
    if r.kind != "performance":
        return []
    definition = tst.DEFINITIONS[r.test_id or ""]
    targets = definition.targets if r.target == "*" else (r.target,)
    scenarios = [s.id for s in definition.scenarios] if r.scenario_id == "*" else [r.scenario_id]
    return [(definition.id, t, sc) for t in targets for sc in scenarios]


class Evidence(BaseModel):
    kind: str  # analysis | run
    status: str  # pass | fail | stale | missing
    detail: str
    run_id: str | None = None
    test_id: str | None = None
    target: str | None = None
    scenario_id: str | None = None
    measured: float | None = None
    limit: float | None = None
    unit: str = ""
    design_revision: int | None = None


class Verification(BaseModel):
    requirement: str
    key: str
    status: str  # verified | failed | stale | not_verified | not_approved
    evidence: list[Evidence]
    summary: str


# Finds the latest run for a case: (test, target, scenario) -> (run or None, current?)
RunLookup = Callable[[str, str, str], tuple[tst.RunRecord | None, bool]]


def verify(r: Requirement, values: Values, latest_run: RunLookup, cursor: int = 0) -> Verification:
    if not r.approved:
        return Verification(
            requirement=r.id,
            key=r.key,
            status="not_approved",
            evidence=[],
            summary="provisional: approve it to include it in verdicts",
        )
    evidence: list[Evidence] = []
    if r.kind == "text":
        return Verification(
            requirement=r.id,
            key=r.key,
            status="manual",
            evidence=[],
            summary=f"verified manually by {r.verification}",
        )
    if r.kind == "design":
        assert r.quantity is not None
        value = quantity_value(r.quantity, values)
        ok = tst.COMPARATORS[r.comparator](value, r.limit)
        evidence.append(
            Evidence(
                kind="analysis",
                status="pass" if ok else "fail",
                detail=f"{quantity_label(r.quantity)} is {value:.4g} {r.unit} on the current "
                f"design (deterministic {r.verification})",
                measured=round(value, 6),
                limit=r.limit,
                unit=r.unit,
                design_revision=cursor,
            )
        )
    for test_id, target, scenario in linked_cases(r):
        run, current = latest_run(test_id, target, scenario)
        if run is None:
            evidence.append(
                Evidence(
                    kind="run",
                    status="missing",
                    test_id=test_id,
                    target=target,
                    scenario_id=scenario,
                    detail=f"no run of {test_id} {target} {scenario}",
                )
            )
            continue
        crit = next((c for c in run.criteria if c.id == f"user:{r.id}"), None)
        if not current or crit is None:
            evidence.append(
                Evidence(
                    kind="run",
                    status="stale",
                    run_id=run.id,
                    test_id=test_id,
                    target=target,
                    scenario_id=scenario,
                    design_revision=run.revision.history_cursor,
                    detail="the design or the requirement changed since this run; rerun the test",
                )
            )
            continue
        ok = crit.passed is True and run.status is not tst.RunStatus.INVALID
        evidence.append(
            Evidence(
                kind="run",
                status="pass" if ok else "fail",
                run_id=run.id,
                test_id=test_id,
                target=target,
                scenario_id=scenario,
                measured=crit.measured,
                limit=crit.limit,
                unit=crit.unit,
                design_revision=run.revision.history_cursor,
                detail=f"{run.scenario['label']}, {target}: "
                f"{crit.measured:.4g} {crit.unit}".rstrip()
                + f" ({run.credibility.value.replace('_', ' ')})",
            )
        )
    statuses = {e.status for e in evidence}
    if "fail" in statuses:
        status = "failed"
    elif "stale" in statuses:
        status = "stale"
    elif "missing" in statuses or not evidence:
        status = "not_verified"
    else:
        status = "verified"
    counts = ", ".join(
        f"{sum(e.status == s for e in evidence)} {s}"
        for s in ("pass", "fail", "stale", "missing")
        if any(e.status == s for e in evidence)
    )
    return Verification(
        requirement=r.id,
        key=r.key,
        status=status,
        evidence=evidence,
        summary=f"{status.replace('_', ' ')}: {counts or 'no evidence'}",
    )


def next_key(existing: Iterable[Requirement]) -> str:
    numbers = [int(r.key[4:]) for r in existing if r.key.startswith("REQ-") and r.key[4:].isdigit()]
    return f"REQ-{(max(numbers) if numbers else 0) + 1:03d}"
