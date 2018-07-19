from mashallah import Input
from mashallah.validators import length, nonempty, nullable, required


def test_repr():
    input = Input({})

    for key in input.__dict__.keys():
        assert key in repr(input)

    input.errors["foo"] = "an error message"
    assert "foo" in repr(input)
    assert "an error message" in repr(input)


class DumbInput(Input):
    foo = int, required
    bar = str, nullable, nonempty, length(min=5, max=10)


def test_type_validation():
    input = DumbInput({"foo": "3", "bar": "bazqux"})
    assert not input.valid
    assert "foo" in input.errors
    assert "bar" not in input.errors


def test_length():
    assert DumbInput({"foo": 3, "bar": "bazqux"}).valid
    assert not DumbInput({"foo": 3, "bar": "baz"}).valid
    assert not DumbInput({"foo": 3, "bar": "bazquxbazqux"}).valid


def test_nonempty():
    input = DumbInput({"foo": 3, "bar": ""})
    assert not input.valid
    assert "bar" in input.errors
    assert "foo" not in input.errors


def test_nullable():
    input = DumbInput({"foo": None, "bar": None})
    assert not input.valid
    assert "foo" in input.errors
    assert "bar" not in input.errors


def test_errors_format():
    input = DumbInput({"bar": ""})
    assert input.errors["foo"] == "missing required value"
    assert isinstance(input.errors["bar"], list)
    assert len(input.errors["bar"]) == 2


def test_required():
    input = DumbInput({})
    assert not input.valid
    assert "foo" in input.errors
    assert "bar" not in input.errors


class NestedInput(Input):
    bar = str, required, nonempty, length(min=5, max=10)


class DumbInput2(Input):
    foo = NestedInput, nullable, required


def test_nested():
    assert DumbInput2({"foo": {"bar": "bazqux"}}).valid
    assert DumbInput2({"foo": None}).valid
    assert not DumbInput2({"foo": {"bar": "baz"}}).valid
    assert not DumbInput2({"foo": {}}).valid
