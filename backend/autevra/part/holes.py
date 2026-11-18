"""ISO metric hole data for the Hole feature.

- Coarse pitches: ISO 261/262. Tap drills: ISO 2306 class 6H recommendations (about
  d - P).
- Clearance holes: ISO 273 fine, medium and coarse series.
- Counterbores for ISO 4762 socket head cap screws: diameter from DIN 974-1 row 1, depth
  = head height k + 0.4 mm so the head sits just below the face.
- Countersinks for ISO 10642 countersunk screws: 90 deg, diameter = theoretical head
  diameter dk.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class HoleSize:
    d: float
    pitch: float
    tap_drill: float
    clearance: tuple[float, float, float]  # fine, medium, coarse
    cbore_d: float
    cbore_depth: float
    csink_d: float


# size: d, P, tap drill, ISO 273 (f, m, c), DIN 974-1 cbore dia, k + 0.4, ISO 10642 dk
METRIC: dict[str, HoleSize] = {
    "M2": HoleSize(2, 0.4, 1.6, (2.2, 2.4, 2.6), 4.3, 2.4, 4.4),
    "M2.5": HoleSize(2.5, 0.45, 2.05, (2.7, 2.9, 3.1), 5.0, 2.9, 5.5),
    "M3": HoleSize(3, 0.5, 2.5, (3.2, 3.4, 3.6), 6.5, 3.4, 6.72),
    "M4": HoleSize(4, 0.7, 3.3, (4.3, 4.5, 4.8), 8.0, 4.4, 8.96),
    "M5": HoleSize(5, 0.8, 4.2, (5.3, 5.5, 5.8), 10.0, 5.4, 11.2),
    "M6": HoleSize(6, 1.0, 5.0, (6.4, 6.6, 7.0), 11.0, 6.4, 13.44),
    "M8": HoleSize(8, 1.25, 6.8, (8.4, 9.0, 10.0), 15.0, 8.4, 17.92),
    "M10": HoleSize(10, 1.5, 8.5, (10.5, 11.0, 12.0), 18.0, 10.4, 22.4),
    "M12": HoleSize(12, 1.75, 10.2, (13.0, 13.5, 14.5), 20.0, 12.4, 26.88),
    "M14": HoleSize(14, 2.0, 12.0, (15.0, 15.5, 16.5), 24.0, 14.4, 30.8),
    "M16": HoleSize(16, 2.0, 14.0, (17.0, 17.5, 18.5), 26.0, 16.4, 33.6),
    "M20": HoleSize(20, 2.5, 17.5, (21.0, 22.0, 24.0), 33.0, 20.4, 40.32),
    "M24": HoleSize(24, 3.0, 21.0, (25.0, 26.0, 28.0), 40.0, 24.4, 48.0),
}
FITS = {"fine": 0, "medium": 1, "coarse": 2}


def size(name: str) -> HoleSize:
    try:
        return METRIC[name]
    except KeyError:
        raise ValueError(f"unknown thread size {name!r}; use one of {', '.join(METRIC)}") from None
