class ResponseSuccess(object):
    SUCCESS = 'SUCCESS'

    def __init__(self, value=None):
        self.value = value

    def __nonzero__(self):
        return True

    @property
    def type(self):
        return self.SUCCESS

    __bool__ = __nonzero__


class ResponseFailure(object):
    VALIDATION_ERROR = 'VALIDATION_ERROR'
    SYSTEM_ERROR = 'SYSTEM_ERROR'

    def __init__(self, _type, message: str):
        self.type = _type
        self.message = message

    def __repr__(self):
        return "{} : {}".format(self.type, self.message)

    def __nonzero__(self):
        return False

    __bool__ = __nonzero__

    @classmethod
    def build_from_invalid_request(cls, request):
        result = {err['parameter']: err['message'] for err in request.errors}
        return cls(cls.VALIDATION_ERROR, result)

    @classmethod
    def build_from_system_error(cls, error):
        if isinstance(error, Exception):
            return cls(cls.SYSTEM_ERROR, "{} : {}".format(error.__class__.__name__, str(error)))
        return None

    @classmethod
    def build_from_error_dict(cls, adict):
        if isinstance(adict, dict):
            return cls(cls.VALIDATION_ERROR, adict)
        return None

    @property
    def value(self):
        return {'type': self.type, 'message': self.message}
