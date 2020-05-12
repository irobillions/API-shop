from app.shared.request import ValidRequest, InvalidRequest
from app.shared.validation import RequiredRule, ValidationService, MinLengthRule, EmailRule


class RegisterUserRequest(ValidRequest):
    @classmethod
    def build_from_dict(cls, adict):
        invalid_request = InvalidRequest()
        if not isinstance(adict, dict):  # demander pourquoi cette condition
            invalid_request.add_error('NoField', 'No field specified')
            return invalid_request
        # error losque le dictionaire est vide a regler
        validation_service = ValidationService(adict)
        validation_service.add_rules({
            'firstName': [RequiredRule.build()],
            'lastName': [RequiredRule.build()],
            'username': [RequiredRule.build()],
            'email': [RequiredRule.build(), EmailRule()],
            'password': [RequiredRule.build(),
                         MinLengthRule.build(6)]
        })
        invalid_request = InvalidRequest.from_dict(
            validation_service.validate())

        if invalid_request.has_errors():
            return invalid_request

        return RegisterUserRequest(adict)


class ReauthenticateUserRequest(ValidRequest):
    @classmethod
    def build_from_dict(cls, adict):
        invalid_request = InvalidRequest()
        if not isinstance(adict, dict):
            invalid_request.add_error("NoField", "No field specified")
            return invalid_request

        validation_service = ValidationService(adict)
        validation_service.add_rules({
            'user': [RequiredRule.build()],
        })
        invalid_request = InvalidRequest.from_dict(
            validation_service.validate())

        if invalid_request.has_errors():
            return invalid_request

        return ReauthenticateUserRequest(adict)


class LogInUserRequest(ValidRequest):
    @classmethod
    def build_from_dict(cls, adict):
        invalid_request = InvalidRequest()
        if not isinstance(adict, dict):
            invalid_request.add_error("NoField", "No field specified")
            return invalid_request

        validation_service = ValidationService(adict)
        validation_service.add_rules({
            'email': [RequiredRule.build(), EmailRule()],
            'password': [RequiredRule.build()]
        })
        invalid_request = InvalidRequest.from_dict(
            validation_service.validate())

        if invalid_request.has_errors():
            return invalid_request

        return LogInUserRequest(adict)


class LogoutUserRequest(ValidRequest):
    pass


class GetInfosUserRequest(ValidRequest):
    @classmethod
    def build_from_dict(cls, adict):
        invalid_request = InvalidRequest()
        if not isinstance(adict, dict):
            invalid_request.add_error('email', 'Not correct email')
            return invalid_request
        validation_service = ValidationService(adict)
        validation_service.add_rules(
            {'email': [RequiredRule.build(), EmailRule()]})
        invalid_request = InvalidRequest.from_dict(
            validation_service.validate())

        if invalid_request.has_errors():
            return invalid_request

        return GetInfosUserRequest(adict)


class EditInfosUserRequest(ValidRequest):
    pass


class ForgotPasswordRequest(ValidRequest):
    pass
