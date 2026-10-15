"""Design tables as CSV: a header ``variant,<param>,...`` and one row per variant."""

import csv
import io

from autevra.part.features import DesignTable, Variant


def to_csv(table: DesignTable) -> str:
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(["variant", *table.columns])
    for row in table.rows:
        writer.writerow([row.name, *(f"{v:g}" for v in row.values)])
    return out.getvalue()


def from_csv(text: str, active: str | None = None) -> DesignTable:
    """Parse a CSV design table; raises ValueError with the line at fault."""
    rows = [r for r in csv.reader(io.StringIO(text.strip())) if any(c.strip() for c in r)]
    if not rows:
        raise ValueError("the CSV is empty")
    header = [c.strip() for c in rows[0]]
    if len(header) < 2 or header[0].lower() not in ("variant", "name"):
        raise ValueError("the first column must be 'variant', followed by parameter names")
    variants = []
    for line, cells in enumerate(rows[1:], start=2):
        if len(cells) != len(header):
            raise ValueError(f"line {line}: expected {len(header)} cells, got {len(cells)}")
        try:
            values = [float(c) for c in cells[1:]]
        except ValueError:
            raise ValueError(f"line {line}: values must be numbers") from None
        variants.append(Variant(name=cells[0].strip(), values=values))
    return DesignTable(columns=header[1:], rows=variants, active=active)
