"""ISO / Fanuc-style G-code post-processor (3-axis mill, metric).

Program layout: safety block (G21 G17 G90 G94 G40 G49 G80), then per operation a tool
change (T M6), spindle (S M3), work offset G54, length compensation G43 H, coolant M8,
the moves (G0 rapids, G1 feeds; F only when it changes) or a canned cycle (G81 drill,
G82 drill with dwell, G83 peck drill, G84 rigid tap with M29) cancelled by G80, and the
end block (M9 M5, G91 G28 Z0 home, M30). Coordinates are relative to the work zero:
X/Y at the stock's min corner, Z at the stock top. Tested against the move list, not on a
machine: check the program in a simulator and dry-run above the part first.
"""

from autevra.cam.milling import Operation, Setup


def _n(v: float) -> str:
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def _ascii(text: str) -> str:
    """Comment text most controllers accept: upper-case ASCII without parentheses."""
    text = text.replace("⌀", "DIA ").replace("°", " DEG").replace("×", "X").replace("²", "2")
    return "".join(ch if ch.isascii() and ch not in "()" else " " for ch in text).upper()


def _f(v: float) -> str:
    return str(max(1, round(v)))


def post(ops: list[Operation], setup: Setup, program: int = 1000, title: str = "AUTEVRA") -> str:
    x0, y0, _, _, _, z_top = setup.stock
    safe = setup.safe_z - z_top

    def xyz(p: tuple[float, float, float]) -> str:
        return f"X{_n(p[0] - x0)} Y{_n(p[1] - y0)} Z{_n(p[2] - z_top)}"

    clean = _ascii(title)[:40]
    out = [
        "%",
        f"O{program:04d} ({clean})",
        "(WORK ZERO: X0 Y0 STOCK MIN CORNER, Z0 STOCK TOP)",
        f"(STOCK {_n(setup.stock[3] - x0)} X {_n(setup.stock[4] - y0)} X "
        f"{_n(z_top - setup.stock[2])} MM)",
        "G21 G17 G90 G94 G40 G49 G80",
    ]
    current_tool = None
    for op in ops:
        t = op.tool
        out.append(f"({_ascii(op.name)})")
        if t.number != current_tool:
            out += [f"({_ascii(t.label)})", "M9", "M5", "G91 G28 Z0", "G90", f"T{t.number} M6"]
            current_tool = t.number
        out += [f"S{round(op.speeds.rpm)} M3", "G54", f"G43 H{t.number} Z{_n(safe)}", "M8"]
        if op.cycle:
            c = op.cycle
            pts = c["points"]
            r_plane = f"R{_n(pts[0][2] + c['r'] - z_top)}"
            bottom = f"Z{_n(pts[0][2] - c['depth'] - z_top)}"
            fword = f"F{_f(op.speeds.feed)}"
            first = f"X{_n(pts[0][0] - x0)} Y{_n(pts[0][1] - y0)}"
            if c["code"] == "G84":
                out += [
                    f"M29 S{round(op.speeds.rpm)}",
                    f"G98 G84 {first} {bottom} {r_plane} {fword}",
                ]
            elif c["code"] == "G83":
                out.append(f"G98 G83 {first} {bottom} {r_plane} Q{_n(c['peck'])} {fword}")
            elif c["code"] == "G82":
                dwell = round(1000 * c.get("dwell", 0.3))
                out.append(f"G98 G82 {first} {bottom} {r_plane} P{dwell} {fword}")
            else:
                out.append(f"G98 G81 {first} {bottom} {r_plane} {fword}")
            out += [f"X{_n(p[0] - x0)} Y{_n(p[1] - y0)}" for p in pts[1:]]
            out.append("G80")
            continue
        feed: str | None = None
        last: str | None = None
        for m in op.moves:
            if not m.pts:
                continue
            if m.kind == "rapid":
                for p in m.pts if last is None else m.pts[1:]:
                    if (pos := xyz(p)) != last:
                        out.append(f"G0 {pos}")
                        last = pos
                continue
            word = _f(m.feed)
            for p in m.pts:
                pos = xyz(p)
                if pos == last:
                    continue
                out.append(f"G1 {pos}" + (f" F{word}" if word != feed else ""))
                feed, last = word, pos
        out.append(f"G0 Z{_n(safe)}")
    out += ["M9", "M5", "G91 G28 Z0", "G28 X0 Y0", "G90", "M30", "%"]
    return "\n".join(out) + "\n"
