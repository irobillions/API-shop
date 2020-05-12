from app.shared.request import InvalidRequest, ValidRequest
from app.shared.validation import ValidationService, RequiredRule


class AddCategoryRequest(ValidRequest):
    @classmethod
    def build_from_dict(cls, adict):
        invalid_request = InvalidRequest()
        if not isinstance(adict, dict):
            invalid_request.add_error("No Field", "No parameter given")

        validation_service = ValidationService(adict)
        validation_service.add_rules({"name": [RequiredRule.build()]})
        invalid_request = InvalidRequest.from_dict(
            validation_service.validate())

        if invalid_request.has_errors():
            return invalid_request

        return cls(adict)


class ListCategoriesRequest(ValidRequest):
    pass
