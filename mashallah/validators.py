def length(min=None, max=None):
    def validator(function):
        def validate(value):
            output, errors = function(value)
            if (value is not None
                and (min is not None and len(value) < min
                     or max is not None and len(value) > max)):
                message = "should have a length between {} and {} (is {})"
                message = message.format(min, max, len(value))
                errors.append(message)
            return output, errors
        return validate
    return validator


def nonempty(function):
    def validate(value):
        output, errors = function(value)
        if value is not None and not value:
            errors.append("shouldn't be empty")
        return output, errors
    return validate


def nullable(function):
    def validate(value):
        output, errors = function(value)
        if value is None:
            errors.pop(0)
        return output, errors
    return validate


def required(function):
    return function


__all__ = ["length", "nonempty", "nullable", "required"]
