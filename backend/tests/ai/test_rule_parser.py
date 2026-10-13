import pytest

from autevra.ai import lexicon
from autevra.ai.rule_parser import Kind, Reason, normalise, parse
from autevra.domain.commands import Operation, Source
from autevra.domain.units import Unit

INC, DEC, SET, SCALE = Operation.INCREASE, Operation.DECREASE, Operation.SET, Operation.SCALE


def _changes(text: str) -> list[tuple[str, Operation, float, Unit | None]]:
    result = parse(text)
    assert result.kind is Kind.COMMAND, (text, result.question)
    assert result.command is not None
    return [(c.parameter, c.operation, c.value, c.unit) for c in result.command.changes]


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("increase the wheelbase by 100 mm", [("wheelbase", INC, 100, Unit.MM)]),
        ("Increase the wheelbase by 100mm.", [("wheelbase", INC, 100, Unit.MM)]),
        ("extend the wheel base by 10 cm", [("wheelbase", INC, 10, Unit.CM)]),
        ("lengthen the wheelbase by 0.1 m", [("wheelbase", INC, 0.1, Unit.M)]),
        ("set the wheelbase to 2.8 metres", [("wheelbase", SET, 2.8, Unit.M)]),
        ("increase the wheelbase to 2800 mm", [("wheelbase", SET, 2800, Unit.MM)]),
        ("wheelbase = 2750", [("wheelbase", SET, 2750, None)]),
        ("reduce the front overhang by 50 mm", [("front_overhang", DEC, 50, Unit.MM)]),
        ("shorten the rear overhang by 30 mm", [("rear_overhang", DEC, 30, Unit.MM)]),
        ("lower the car by 20 mm", [("ground_clearance", DEC, 20, Unit.MM)]),
        ("lower the vehicle by 2 cm", [("ground_clearance", DEC, 2, Unit.CM)]),
        ("raise the ride height by 15 mm", [("ground_clearance", INC, 15, Unit.MM)]),
        ("make it wider by 50 mm", [("body_width", INC, 50, Unit.MM)]),
        ("make the car 1.9 m wide", [("body_width", SET, 1.9, Unit.M)]),
        ("make it 1500 mm tall", [("overall_height", SET, 1500, Unit.MM)]),
        ("lower the roof by 30 mm", [("overall_height", DEC, 30, Unit.MM)]),
        ("set the rims to 18 inch", [("rim_diameter", SET, 18, Unit.IN)]),
        ('fit 19" rims', [("rim_diameter", SET, 19, Unit.IN)]),
        ("go from 17s to 18s on the rims", [("rim_diameter", SET, 18, None)]),
        ("use 20 inch wheels", [("rim_diameter", SET, 20, Unit.IN)]),
        ("set the tire width to 245 mm", [("tyre_width", SET, 245, Unit.MM)]),
        ("reduce the tyre aspect ratio by 5%", [("tyre_aspect_ratio", DEC, 5, Unit.PERCENT)]),
        ("increase the wheelbase by 5%", [("wheelbase", INC, 5, Unit.PERCENT)]),
        ("increase the wheelbase by 5 percent", [("wheelbase", INC, 5, Unit.PERCENT)]),
        ("scale the body width by a factor of 1.02", [("body_width", SCALE, 1.02, None)]),
        ("set the steering lock to 38 degrees", [("max_steer_angle", SET, 38, Unit.DEG)]),
        ("set the max steer angle to 40°", [("max_steer_angle", SET, 40, Unit.DEG)]),
        ("increase the rail wall thickness by 1 mm", [("rail_wall", INC, 1, Unit.MM)]),
        ("widen the frame rail spacing by 20 mm", [("rail_spacing", INC, 20, Unit.MM)]),
        ("increase the wheelbase by -50 mm", [("wheelbase", DEC, 50, Unit.MM)]),
    ],
)
def test_single_instructions(text: str, expected: list) -> None:
    assert _changes(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (
            "increase the wheelbase by 100 mm and the front overhang by 20 mm",
            [("wheelbase", INC, 100, Unit.MM), ("front_overhang", INC, 20, Unit.MM)],
        ),
        (
            "set the rims to 18 inch, lower the car by 20 mm",
            [("rim_diameter", SET, 18, Unit.IN), ("ground_clearance", DEC, 20, Unit.MM)],
        ),
        (
            "raise the ride height to 200 mm and then reduce the rear overhang by 50 mm",
            [("ground_clearance", SET, 200, Unit.MM), ("rear_overhang", DEC, 50, Unit.MM)],
        ),
        (
            "widen the track by 10 mm",
            [("track_front", INC, 10, Unit.MM), ("track_rear", INC, 10, Unit.MM)],
        ),
        (
            "widen the front and rear track by 10 mm",
            [("track_front", INC, 10, Unit.MM), ("track_rear", INC, 10, Unit.MM)],
        ),
        ("increase the front track by 20 mm", [("track_front", INC, 20, Unit.MM)]),
    ],
)
def test_compound_and_group_instructions(text: str, expected: list) -> None:
    assert _changes(text) == expected


def test_command_records_source_and_instruction() -> None:
    result = parse("increase the wheelbase by 100 mm")
    assert result.command is not None
    assert result.command.source is Source.RULES
    assert result.command.instruction == "increase the wheelbase by 100 mm"
    assert result.assumptions == []


def test_bare_number_records_assumed_unit() -> None:
    result = parse("increase the wheelbase by 100")
    assert result.assumptions == ["assumed 100 mm for the wheelbase"]


@pytest.mark.parametrize("text", ["undo", "Undo that", "go back", "revert"])
def test_undo(text: str) -> None:
    assert parse(text).kind is Kind.UNDO


@pytest.mark.parametrize("text", ["redo", "Redo it"])
def test_redo(text: str) -> None:
    assert parse(text).kind is Kind.REDO


@pytest.mark.parametrize(
    ("text", "ids"),
    [
        ("what is the wheelbase?", ("wheelbase",)),
        ("What's the ground clearance", ("ground_clearance",)),
        ("how long is the car?", ("overall_length",)),
        ("how wide is it?", ("body_width",)),
        ("what is the overall length?", ("overall_length",)),
        ("what is the track?", ("track_front", "track_rear")),
        ("show the tyre diameter", ("tyre_diameter",)),
    ],
)
def test_queries(text: str, ids: tuple[str, ...]) -> None:
    result = parse(text)
    assert result.kind is Kind.QUERY
    assert result.query == ids


@pytest.mark.parametrize(
    ("text", "fragment"),
    [
        ("make it longer", "derived from the front overhang, wheelbase, rear overhang"),
        ("increase the overall length by 100 mm", "derived from"),
        ("lower the car", "By how much"),
        ("increase the wheelbase", "By how much"),
        ("set the wheelbase", "What value"),
        ("increase the wheelbse by 100 mm", "Did you mean"),
        ("paint it red", "could not find a design parameter"),
        ("", "What would you like"),
    ],
)
def test_clarifications(text: str, fragment: str) -> None:
    result = parse(text)
    assert result.kind is Kind.CLARIFICATION
    assert result.question is not None and fragment in result.question


def test_longer_offers_concrete_suggestions() -> None:
    result = parse("make it longer")
    assert "increase the wheelbase by 100 mm" in result.suggestions


def test_typo_suggests_the_right_parameter() -> None:
    assert "wheelbase" in parse("increase the wheelbse by 100 mm").suggestions


def test_normalise() -> None:
    assert normalise("Lower THE CAR by 20mm!") == "lower it by 20mm"
    assert normalise("17s to 18s") == "17 to 18"


def test_aliases_are_unambiguous() -> None:
    # Building the table raises on a conflicting alias; also check lookup order.
    assert lexicon.ALIASES_BY_LENGTH.index("front track") < lexicon.ALIASES_BY_LENGTH.index("track")


@pytest.mark.parametrize(
    "text",
    [
        "slide the cabin 100 mm forward",  # once misread as "set cabin length to 100 mm"
        "drop the window line by 40 mm",  # once misread as "lower the car by 40 mm"
        "push the rear axle back 10 cm",
        "make the glasshouse 200 mm longer",
    ],
)
def test_unknown_words_prevent_a_guess(text: str) -> None:
    result = parse(text)
    assert result.kind is Kind.CLARIFICATION
    assert result.reason is Reason.NO_TARGET  # escalated to the LLM when one is available


@pytest.mark.parametrize(
    ("text", "target", "scenario", "test_id"),
    [
        ("run a quarter-car suspension test", None, None, "quarter_car"),
        ("test the rear suspension over a pothole", "rear", "pothole_50", "quarter_car"),
        ("simulate a speed bump on the front", "front", "hump_75", "quarter_car"),
        ("run the ride modes test", None, None, "ride_modes"),
        ("test it", None, None, "quarter_car"),
    ],
)
def test_test_requests(text: str, target: str | None, scenario: str | None, test_id: str) -> None:
    r = parse(text)
    assert r.kind is Kind.TEST and r.tests is not None
    assert (r.tests.target, r.tests.scenario_id, r.tests.test_id) == (target, scenario, test_id)


def test_change_then_test() -> None:
    r = parse("Increase the rear shock absorber damping by 10% and test its response.")
    assert r.kind is Kind.COMMAND and r.command is not None and r.tests is not None
    assert {c.parameter for c in r.command.changes} == {"rear_damping_bump", "rear_damping_rebound"}
    assert all(c.unit == "%" and c.value == 10 for c in r.command.changes)
    assert parse("increase the wheelbase by 100 mm").tests is None


@pytest.mark.parametrize(
    ("text", "values"),
    [
        ("set the rear spring rate to 30 kN/m", {"rear_spring_rate": 30}),
        ("set the front bump damping to 1.8 kN·s/m", {"front_damping_bump": 1800}),
        ("set the rear spring rate to 150 lbf/in", {"rear_spring_rate": 26.269025}),
        ("make the car 100 kg heavier", {"vehicle_mass": 1700}),
        ("set the vehicle mass to 3500 lb", {"vehicle_mass": 1587.573295}),
    ],
)
def test_engineering_units_convert(text: str, values: dict) -> None:
    from autevra.domain.commands import resolve
    from autevra.domain.parameters import default_values

    r = parse(text)
    assert r.command is not None
    assert resolve(r.command, default_values()) == pytest.approx(values)


def test_what_if_is_a_preview_not_a_command() -> None:
    r = parse("what if I increase the wheelbase by 100 mm?")
    assert r.kind is Kind.PREVIEW and r.command is not None
    assert parse("what is the wheelbase?").kind is Kind.QUERY


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("require the ground clearance to be at least 15 cm",
         {"kind": "design", "quantity": "ground_clearance", "comparator": ">=", "limit": 15,
          "unit": "cm"}),
        ("require the rear peak body acceleration to stay below 6 m/s² over the hump",
         {"kind": "performance", "metric": "peak_body_acceleration", "target": "rear",
          "scenario_id": "hump_75", "comparator": "<=", "limit": 6}),
        ("add a requirement: bump travel below 35 mm in every test",
         {"metric": "max_bump_travel", "scenario_id": "*", "comparator": "<="}),
    ],
)  # fmt: skip
def test_requirement_statements(text: str, expected: dict) -> None:
    r = parse(text)
    assert r.kind is Kind.REQUIREMENT and r.requirement is not None
    assert {k: r.requirement[k] for k in expected} == expected


def test_ambiguous_requirements_ask() -> None:
    assert parse("require the body acceleration to be below 5").kind is Kind.CLARIFICATION
    assert parse("require the spring rate to be at least 20 N/mm").kind is Kind.CLARIFICATION
    assert parse("verify the requirements").kind is Kind.VERIFY
