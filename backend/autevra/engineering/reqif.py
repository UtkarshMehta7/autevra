"""ReqIF 1.2 (OMG, namespace .../ReqIF/20110401/reqif.xsd) export and import.

Export writes one SPEC-OBJECT-TYPE whose attributes are the standard ``ReqIF.ForeignID``,
``ReqIF.Name``, ``ReqIF.Text`` plus ``Autevra.*`` attributes for the machine-checkable
part (kind, quantity or metric, comparator, limit, unit, test, target, scenario). The
specification hierarchy carries parent/child refinement.

Import accepts any ReqIF: objects with Autevra attributes round-trip exactly; other objects
become ``text`` requirements (tracked, verified manually). Documents with a DOCTYPE or
entity declarations are rejected (no entity expansion), as are files over 5 MB.

Note: ``ReqIF.Text`` is written as a plain string attribute; the ReqIF Implementation Guide
recommends XHTML for rich text, which other tools may prefer. Import reads both.
"""

import xml.etree.ElementTree as ET
from datetime import UTC, datetime

from pydantic import ValidationError

from autevra.engineering.requirements import Requirement

NS = "http://www.omg.org/spec/ReqIF/20110401/reqif.xsd"
XHTML = "http://www.w3.org/1999/xhtml"
MAX_BYTES = 5 * 1024 * 1024

# Requirement field -> (attribute long name, datatype)
FIELDS: dict[str, tuple[str, str]] = {
    "key": ("ReqIF.ForeignID", "STRING"),
    "title": ("ReqIF.Name", "STRING"),
    "text": ("ReqIF.Text", "STRING"),
    "rationale": ("Autevra.Rationale", "STRING"),
    "kind": ("Autevra.Kind", "STRING"),
    "verification": ("Autevra.Verification", "STRING"),
    "priority": ("Autevra.Priority", "STRING"),
    "approved": ("Autevra.Approved", "STRING"),
    "test_id": ("Autevra.Test", "STRING"),
    "target": ("Autevra.Target", "STRING"),
    "scenario_id": ("Autevra.Scenario", "STRING"),
    "metric": ("Autevra.Metric", "STRING"),
    "quantity": ("Autevra.Quantity", "STRING"),
    "comparator": ("Autevra.Comparator", "STRING"),
    "limit": ("Autevra.Limit", "REAL"),
    "unit": ("Autevra.Unit", "STRING"),
}


class ReqIFError(ValueError):
    pass


def _q(tag: str) -> str:
    return f"{{{NS}}}{tag}"


def _sub(parent: ET.Element, tag: str, text: str | None = None, **attrs: str) -> ET.Element:
    el = ET.SubElement(parent, _q(tag), {k.replace("_", "-"): v for k, v in attrs.items()})
    if text is not None:
        el.text = text
    return el


def export(records: list[Requirement], title: str) -> str:
    now = datetime.now(UTC).isoformat(timespec="seconds")
    ET.register_namespace("", NS)
    root = ET.Element(_q("REQ-IF"))
    header = _sub(_sub(root, "THE-HEADER"), "REQ-IF-HEADER", IDENTIFIER="autevra-header")
    _sub(header, "CREATION-TIME", now)
    _sub(header, "REQ-IF-TOOL-ID", "Autevra")
    _sub(header, "REQ-IF-VERSION", "1.0")
    _sub(header, "SOURCE-TOOL-ID", "Autevra")
    _sub(header, "TITLE", title)
    content = _sub(_sub(root, "CORE-CONTENT"), "REQ-IF-CONTENT")
    types = _sub(content, "DATATYPES")
    _sub(
        types,
        "DATATYPE-DEFINITION-STRING",
        IDENTIFIER="DT-STRING",
        LAST_CHANGE=now,
        LONG_NAME="String",
        MAX_LENGTH="100000",
    )
    _sub(
        types,
        "DATATYPE-DEFINITION-REAL",
        IDENTIFIER="DT-REAL",
        LAST_CHANGE=now,
        LONG_NAME="Real",
        ACCURACY="12",
        MIN="-1.0E308",
        MAX="1.0E308",
    )
    spec_types = _sub(content, "SPEC-TYPES")
    sot = _sub(
        spec_types,
        "SPEC-OBJECT-TYPE",
        IDENTIFIER="SOT-REQUIREMENT",
        LAST_CHANGE=now,
        LONG_NAME="Autevra requirement",
    )
    attrs = _sub(sot, "SPEC-ATTRIBUTES")
    for field, (name, dtype) in FIELDS.items():
        ad = _sub(
            attrs,
            f"ATTRIBUTE-DEFINITION-{dtype}",
            IDENTIFIER=f"AD-{field}",
            LAST_CHANGE=now,
            LONG_NAME=name,
        )
        _sub(_sub(ad, "TYPE"), f"DATATYPE-DEFINITION-{dtype}-REF", f"DT-{dtype}")
    _sub(
        spec_types,
        "SPECIFICATION-TYPE",
        IDENTIFIER="ST-SPECIFICATION",
        LAST_CHANGE=now,
        LONG_NAME="Autevra specification",
    )

    objects = _sub(content, "SPEC-OBJECTS")
    for r in records:
        obj = _sub(
            objects,
            "SPEC-OBJECT",
            IDENTIFIER=f"REQ-{r.id}",
            LAST_CHANGE=r.created_at.isoformat(timespec="seconds"),
        )
        _sub(_sub(obj, "TYPE"), "SPEC-OBJECT-TYPE-REF", "SOT-REQUIREMENT")
        vals = _sub(obj, "VALUES")
        for field, (_, dtype) in FIELDS.items():
            value = getattr(r, field)
            if value is None or value == "":
                continue
            text = str(value).lower() if isinstance(value, bool) else str(value)
            av = _sub(vals, f"ATTRIBUTE-VALUE-{dtype}", THE_VALUE=text)
            _sub(_sub(av, "DEFINITION"), f"ATTRIBUTE-DEFINITION-{dtype}-REF", f"AD-{field}")
    _sub(content, "SPEC-RELATIONS")
    specs = _sub(content, "SPECIFICATIONS")
    spec = _sub(specs, "SPECIFICATION", IDENTIFIER="SPEC-autevra", LAST_CHANGE=now, LONG_NAME=title)
    _sub(_sub(spec, "TYPE"), "SPECIFICATION-TYPE-REF", "ST-SPECIFICATION")
    by_id = {r.id: r for r in records}
    children: dict[str | None, list[Requirement]] = {}
    for r in records:
        parent = r.parent if r.parent in by_id else None
        children.setdefault(parent, []).append(r)

    def hierarchy(parent_el: ET.Element, parent: str | None) -> None:
        kids = children.get(parent, [])
        if not kids:
            return
        box = _sub(parent_el, "CHILDREN")
        for r in kids:
            h = _sub(box, "SPEC-HIERARCHY", IDENTIFIER=f"H-{r.id}", LAST_CHANGE=now)
            _sub(_sub(h, "OBJECT"), "SPEC-OBJECT-REF", f"REQ-{r.id}")
            hierarchy(h, r.id)

    hierarchy(spec, None)
    ET.indent(root)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="unicode")


def _text_of(av: ET.Element) -> str:
    if "THE-VALUE" in av.attrib:
        return av.attrib["THE-VALUE"]
    value = av.find(_q("THE-VALUE"))  # XHTML content
    return "".join(value.itertext()).strip() if value is not None else ""


def parse(xml: str | bytes) -> list[Requirement]:
    raw = xml.encode() if isinstance(xml, str) else xml
    if len(raw) > MAX_BYTES:
        raise ReqIFError("ReqIF file is larger than 5 MB")
    head = raw[:4096].upper()
    if b"<!DOCTYPE" in head or b"<!ENTITY" in raw.upper():
        raise ReqIFError("DOCTYPE and entity declarations are not accepted")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        raise ReqIFError(f"not well-formed XML: {exc}") from None
    if root.tag != _q("REQ-IF"):
        raise ReqIFError("not a ReqIF document (root element REQ-IF in the ReqIF namespace)")

    names: dict[str, str] = {}
    for ad in root.iter():
        if ad.tag.startswith(_q("ATTRIBUTE-DEFINITION-")) and "IDENTIFIER" in ad.attrib:
            names[ad.attrib["IDENTIFIER"]] = ad.attrib.get("LONG-NAME", ad.attrib["IDENTIFIER"])
    by_name = {name: field for field, (name, _) in FIELDS.items()}

    parents: dict[str, str] = {}
    for h in root.iter(_q("SPEC-HIERARCHY")):
        ref = h.find(f"{_q('OBJECT')}/{_q('SPEC-OBJECT-REF')}")
        box = h.find(_q("CHILDREN"))
        if ref is None or box is None:
            continue
        for child in box.findall(_q("SPEC-HIERARCHY")):
            cref = child.find(f"{_q('OBJECT')}/{_q('SPEC-OBJECT-REF')}")
            if cref is not None and cref.text and ref.text:
                parents[cref.text.strip()] = ref.text.strip()

    out: list[Requirement] = []
    identifiers: dict[str, str] = {}
    for obj in root.iter(_q("SPEC-OBJECT")):
        ident = obj.attrib.get("IDENTIFIER", "")
        data: dict[str, object] = {}
        for av in obj.iterfind(f"{_q('VALUES')}/*"):
            ref = av.find(f"{_q('DEFINITION')}/*")
            if ref is None or ref.text is None:
                continue
            name = names.get(ref.text.strip(), ref.text.strip())
            field = by_name.get(name)
            if field is not None:
                data[field] = _text_of(av)
        if "approved" in data:
            data["approved"] = str(data["approved"]).lower() == "true"
        if "limit" in data:
            data["limit"] = float(str(data["limit"]))
        if "kind" not in data:  # a requirement from another tool
            data = {
                "kind": "text",
                "verification": "inspection",
                "key": data.get("key", "") or ident,
                "title": data.get("title", ""),
                "text": data.get("text") or data.get("title", ""),
            }
        data = {k: v for k, v in data.items() if v != ""}
        data["source"] = "reqif"
        try:
            record = Requirement.model_validate(data)
        except ValidationError as exc:
            raise ReqIFError(f"{ident}: {exc.errors()[0]['msg']}") from None
        identifiers[ident] = record.id
        out.append(record)
    for i, r in enumerate(out):
        ident = next(k for k, v in identifiers.items() if v == r.id)
        if ident in parents and parents[ident] in identifiers:
            out[i] = r.model_copy(update={"parent": identifiers[parents[ident]]})
    return out
