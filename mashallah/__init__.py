from types import SimpleNamespace
from mashallah.validators import required


def validate(value, typ, *validators):
    def _validate(value):
        errors = []
        if issubclass(typ, Input) and isinstance(value, dict):
            value, errors = typ.process(value)
        elif not isinstance(value, typ):
            message = "should be of type {} (is {})"
            typ_name = "dict" if issubclass(typ, Input) else typ.__name__
            message = message.format(typ_name, type(value).__name__)
            errors.append(message)
        return value, errors

    for validator in validators:
        _validate = validator(_validate)
    return _validate(value)


class Input(SimpleNamespace):

    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.output, self.errors = self.process(data)

    @classmethod
    def process(cls, data):
        output = {}
        errors = {}
        for field, typ, validators in cls.iterfields():
            try:
                value = data[field]
            except KeyError:
                if required in validators:
                    errors[field] = "missing required value"
                continue
            field_output, field_errors = validate(value, typ, *validators)
            if field_errors:
                errors[field] = field_errors
            else:
                output[field] = field_output
        return output, errors

    @classmethod
    def iterfields(cls):
        for key, value in cls.__dict__.items():
            if (isinstance(value, tuple) and value
                and isinstance(value[0], type)):
                yield key, value[0], value[1:]

    @property
    def valid(self):
        return (not self.errors)


__all__ = ["Input"]
