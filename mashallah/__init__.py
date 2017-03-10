from mashallah.validators import required


def validate(value, typ, *validators):
    def _validate(value):
        if value is not None and not isinstance(value, typ):
            message = "should be of type {} (is {})"
            message = message.format(typ.__name__, type(value).__name__)
            raise TypeError(message)
        return value

    for validator in validators:
        _validate = validator(_validate)
    return _validate(value)


class Input(object):

    def __init__(self, data):
        self.output, self.errors = self.process(data)

    def __repr__(self):
        items = [(key, str(value)) for key, value in self.__dict__.items()]
        items = ["=".join(item) for item in items]
        items = ", ".join(items)
        values = [self.__class__.__module__, self.__class__.__name__, items]
        return "<{}.{}({})>".format(*values)

    def process(self, data):
        output = {}
        errors = {}
        for field, typ, validators in self.fields:
            try:
                value = data[field]
            except KeyError:
                if required in validators:
                    errors[field] = "missing required value"
                continue
            try:
                output[field] = validate(value, typ, *validators)
            except Exception as exception:
                errors[field] = str(exception)
        return output, errors

    @property
    def fields(self):
        for key, value in self.__class__.__dict__.items():
            if (isinstance(value, tuple) and value
                and isinstance(value[0], type)):
                yield key, value[0], value[1:]

    @property
    def valid(self):
        return (not self.errors)


__all__ = ["Input"]
