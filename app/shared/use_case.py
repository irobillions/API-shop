from .response import ResponseFailure


class UseCase:
    def __call__(self, request):
        if not request:
            return ResponseFailure.build_from_invalid_request(request)
        try:
            return self.process_request(request)
        except Exception as e:
            return ResponseFailure.build_from_system_error(e)

    # to process request
    def process_request(self, request):
        raise NotImplementedError
