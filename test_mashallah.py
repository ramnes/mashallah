from mashallah import Input
from mashallah.validators import length, nonempty, nonnull, required


def test_repr():
    input = Input({})

    assert repr(input).startswith("<mashallah.Input(")
    assert repr(input).endswith(")>")
    for key in input.__dict__.keys():
        assert key in repr(input)

    input.errors["foo"] = "an error message"
    assert "foo" in repr(input)
    assert "an error message" in repr(input)


class DumbInput(Input):
    foo = int, nonnull, required
    bar = str, nonempty, length(min=5, max=10)


def test_type_validation():
    input = DumbInput({"foo": "3", "bar": "bazqux"})
    assert not input.valid
    assert "foo" in input.errors
    assert not "bar" in input.errors


def test_length():
    assert DumbInput({"foo": 3, "bar": "bazqux"}).valid
    assert not DumbInput({"foo": 3, "bar": "baz"}).valid
    assert not DumbInput({"foo": 3, "bar": "bazquxbazqux"}).valid


def test_nonempty():
    input = DumbInput({"foo": 3, "bar": ""})
    assert not input.valid
    assert "bar" in input.errors
    assert not "foo" in input.errors


def test_nonnull():
    input = DumbInput({"foo": None, "bar": None})
    assert not input.valid
    assert "foo" in input.errors
    assert not "bar" in input.errors


def test_required():
    input = DumbInput({})
    assert not input.valid
    assert "foo" in input.errors
    assert not "bar" in input.errors