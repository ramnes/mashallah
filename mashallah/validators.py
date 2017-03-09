def length(min=None, max=None):
    def validator(function):
        def validate(value):
            output = function(value)
            if (output is not None
                and (min is not None and len(output) < min
                     or max is not None and len(output) > max)):
                message = "should have a length between {} and {} (is {})"
                message = message.format(min, max, len(output))
                raise ValueError(message)
            return output
        return validate
    return validator


def nonempty(function):
    def validate(value):
        output = function(value)
        if output is not None and not output:
            raise TypeError("shouldn't be empty")
        return output
    return validate


def nonnull(function):
    def validate(value):
        output = function(value)
        if output is None:
            raise TypeError("shouldn't be null")
        return output
    return validate


def required(function):
    return function


__all__ = ["length", "nonempty", "nonnull", "required"]
