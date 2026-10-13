"""Design state: current parameter values plus an undoable command history.

The history is the source of truth together with the defaults: replaying
every applied entry over the defaults reproduces the current values exactly.
"""

from collections.abc import Mapping
from datetime import UTC, datetime
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from autevra.core import parameters
from autevra.core.commands import SetParameters, resolve
from autevra.core.rules import Violation, validate


class ValueChange(BaseModel):
    model_config = ConfigDict(frozen=True)

    parameter: str
    old: float
    new: float


class HistoryEntry(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str = Field(default_factory=lambda: uuid4().hex)
    command: SetParameters
    changes: tuple[ValueChange, ...]
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class CommandRejectedError(ValueError):
    def __init__(self, violations: list[Violation]) -> None:
        self.violations = violations
        super().__init__("; ".join(v.message for v in violations))


class ApplyResult(BaseModel):
    entry: HistoryEntry | None
    changed: tuple[str, ...]


class DesignState(BaseModel):
    """Serialisable design state. ``cursor`` counts the applied history entries."""

    values: dict[str, float] = Field(default_factory=parameters.default_values)
    history: list[HistoryEntry] = Field(default_factory=list)
    cursor: int = 0

    def preview(self, command: SetParameters) -> dict[str, float]:
        """The full parameter set after ``command``, without applying it."""
        return self.values | resolve(command, self.values)

    def apply(self, command: SetParameters) -> ApplyResult:
        proposed = self.preview(command)
        violations = validate(proposed)
        if violations:
            raise CommandRejectedError(violations)
        changes = tuple(
            ValueChange(parameter=pid, old=self.values[pid], new=proposed[pid])
            for pid in dict.fromkeys(c.parameter for c in command.changes)
            if proposed[pid] != self.values[pid]
        )
        if not changes:
            return ApplyResult(entry=None, changed=())
        entry = HistoryEntry(command=command, changes=changes)
        del self.history[self.cursor :]  # a new command discards the redo branch
        self.history.append(entry)
        self.cursor += 1
        self.values = proposed
        return ApplyResult(entry=entry, changed=tuple(c.parameter for c in changes))

    @property
    def can_undo(self) -> bool:
        return self.cursor > 0

    @property
    def can_redo(self) -> bool:
        return self.cursor < len(self.history)

    def undo(self) -> HistoryEntry | None:
        if not self.can_undo:
            return None
        self.cursor -= 1
        entry = self.history[self.cursor]
        self.values = self.values | {c.parameter: c.old for c in entry.changes}
        return entry

    def redo(self) -> HistoryEntry | None:
        if not self.can_redo:
            return None
        entry = self.history[self.cursor]
        self.values = self.values | {c.parameter: c.new for c in entry.changes}
        self.cursor += 1
        return entry

    def replay(self) -> Mapping[str, float]:
        """Recompute values from defaults and the applied history (consistency check)."""
        values = parameters.default_values()
        for entry in self.history[: self.cursor]:
            values |= {c.parameter: c.new for c in entry.changes}
        return values
