"""Traceability matrix and impact preview.

The matrix links every requirement to the parameters that can change it, the components
those parameters build or place, the test cases that verify it and the evidence.

``preview`` answers "what happens if I apply this command?" without applying it: changed
values and derived values, rule violations, components rebuilt or moved, tests made stale,
packaging warnings that appear or clear, and each requirement's status before and after.
Design requirements are re-evaluated on the proposed values; performance requirements
whose test inputs change become "needs re-verification" (no result is predicted).
"""

from collections.abc import Iterable, Mapping

from pydantic import BaseModel

from autevra.assembly import graph
from autevra.core import derived as d
from autevra.core.commands import SetParameters, resolve
from autevra.core.parameters import REGISTRY
from autevra.core.rules import Violation, validate
from autevra.engineering import integration
from autevra.engineering import requirements as rq
from autevra.engineering import testing as tst

Values = Mapping[str, float]


class TraceRow(BaseModel):
    requirement: rq.Requirement
    verification: rq.Verification
    parameters: list[str]
    components: list[str]
    cases: list[str]  # "test:target:scenario"


def components_for(r: rq.Requirement) -> list[str]:
    params = rq.linked_parameters(r)
    found = set(graph.impact(params).affected)
    for test_id, target, _ in rq.linked_cases(r):
        found |= set(tst.DEFINITIONS[test_id].components[target])
    return sorted(found)


def matrix(
    records: Iterable[rq.Requirement], values: Values, latest_run: rq.RunLookup, cursor: int
) -> list[TraceRow]:
    return [
        TraceRow(
            requirement=r,
            verification=rq.verify(r, values, latest_run, cursor),
            parameters=rq.linked_parameters(r),
            components=components_for(r),
            cases=[":".join(c) for c in rq.linked_cases(r)],
        )
        for r in records
    ]


class ValueChange(BaseModel):
    id: str
    label: str
    unit: str
    before: float
    after: float


class RequirementChange(BaseModel):
    key: str
    title: str
    before: str
    after: str  # status, or "needs_reverification"
    detail: str


class ImpactPreview(BaseModel):
    valid: bool
    violations: list[Violation]
    changes: list[ValueChange]
    derived: list[ValueChange]
    rebuild: list[str]
    move: list[str]
    retest: list[str]
    requirements: list[RequirementChange]
    warnings_added: list[str]
    warnings_cleared: list[str]
    summary: str


def preview(
    command: SetParameters,
    values: Values,
    records: Iterable[rq.Requirement],
    latest_run: rq.RunLookup,
    cursor: int,
) -> ImpactPreview:
    proposed = dict(values) | resolve(command, values)
    changed = [p for p in proposed if proposed[p] != values[p]]
    violations = validate(proposed)
    impact = graph.impact(changed)
    before_d, after_d = d.compute_all(values), d.compute_all(proposed)
    derived_changes = [
        ValueChange(
            id=k,
            label=d.DERIVED[k].label,
            unit=d.DERIVED[k].unit,
            before=round(before_d[k], 6),
            after=round(after_d[k], 6),
        )
        for k in d.DERIVED
        if abs(after_d[k] - before_d[k]) > 1e-9
    ]
    req_changes = []
    for r in records:
        now = rq.verify(r, values, latest_run, cursor)
        if r.kind == "design":
            later = rq.verify(r, proposed, latest_run, cursor)
            after, detail = later.status, later.evidence[0].detail if later.evidence else ""
        elif set(rq.linked_parameters(r)) & set(changed):
            after = "needs_reverification"
            detail = "its test inputs change; rerun the linked tests to verify it"
        else:
            continue
        if after != now.status or r.kind != "design":
            req_changes.append(
                RequirementChange(
                    key=r.key, title=r.title, before=now.status, after=after, detail=detail
                )
            )
    warn_before = {c.message for c in integration.domain_checks(values) if c.status != "pass"}
    warn_after = {c.message for c in integration.domain_checks(proposed) if c.status != "pass"}
    retest = [f"{t}:{target}" for t, target in tst.tests_affected(changed)]
    broken = [c for c in req_changes if c.after == "failed"]
    parts = [
        f"{len(changed)} parameter(s) change",
        f"{len(impact.rebuild)} component(s) rebuilt, {len(impact.move)} moved",
        f"{len(retest)} test case group(s) to rerun",
    ]
    if violations:
        parts.insert(0, f"REJECTED by {len(violations)} rule(s)")
    if broken:
        parts.append(
            f"{len(broken)} requirement(s) would fail: " + ", ".join(c.key for c in broken)
        )
    return ImpactPreview(
        valid=not violations,
        violations=violations,
        changes=[
            ValueChange(
                id=p,
                label=REGISTRY[p].label,
                unit=str(REGISTRY[p].unit),
                before=values[p],
                after=proposed[p],
            )
            for p in changed
        ],
        derived=derived_changes,
        rebuild=sorted(impact.rebuild),
        move=sorted(impact.move),
        retest=retest,
        requirements=req_changes,
        warnings_added=sorted(warn_after - warn_before),
        warnings_cleared=sorted(warn_before - warn_after),
        summary="; ".join(parts) + ".",
    )
