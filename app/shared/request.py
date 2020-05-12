# request definition
class ValidRequest(object):
    def __init__(self, adict=None):
        self.attributes = adict

    @classmethod
    def from_dict(cls, adict):
        return cls(adict)

    def __getattr__(self, value):
        if value in self.attributes:
            return self.attributes[value]
        raise AttributeError(
            f'the {value} attribute does not exist on the object')

    def __nonzero__(self):
        return True


class InvalidRequest(object):
    def __init__(self, errors=[]):
        self.errors = errors

    def has_errors(self):
        return len(self.errors) > 0

    def add_error(self, parameter: str, message: str):
        self.errors.append({'parameter': parameter, 'message': message})

    @classmethod
    def from_dict(cls, errors):
        cls_errors = []
        for parameter, messages in errors.items():
            cls_errors.append({'parameter': parameter, 'message': messages})
        return cls(cls_errors)

    def __nonzero__(self):
        return False

    __bool__ = __nonzero__
