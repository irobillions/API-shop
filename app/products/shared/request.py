from app.shared.request import ValidRequest, InvalidRequest
from app.shared.validation import ValidationService, RequiredRule, BooleanRule, FloatRule, IntegerRule, DateTimeRule


class AddProductRequest(ValidRequest):
    @classmethod
    def build_from_dict(cls, adict):
        invalid_request = InvalidRequest()
        if not isinstance(adict, dict):
            invalid_request.add_error('No Field', 'Not correct email')
            return invalid_request
        validation_service = ValidationService(adict)
        validation_service.add_rules({
            'name': [RequiredRule.build()],
            'description': [RequiredRule.build()],
            'availability': [RequiredRule.build(),
                             BooleanRule.build()],
            'quality': [RequiredRule.build()],
            'price': [RequiredRule.build(),
                      FloatRule.build()],
            'stock': [RequiredRule.build(),
                      IntegerRule.build()],
            'manufacturer': [RequiredRule.build()],
            'categories': [RequiredRule.build()],
        })
        validation_part_data = None
        if adict.get('part_data'):
            validation_part_data = ValidationService(adict['part_data'])
            validation_part_data.add_rules({
                'ref_part': [RequiredRule.build()],
                'weight': [RequiredRule.build(),
                           IntegerRule.build()],
                'diameter': [RequiredRule.build(),
                             IntegerRule.build()],
                'dimension': [RequiredRule.build()],
                'date_of_prod': [RequiredRule.build(),
                                 DateTimeRule.build()],
                'num_oem': [RequiredRule.build()],
                'country_of_origin': [RequiredRule.build()],
                'volume_of_part': [RequiredRule.build(),
                                   IntegerRule.build()],
            })

        if adict.get('part_data'):
            invalid_request = InvalidRequest.from_dict({
                **validation_service.validate(),
                **validation_part_data.validate()
            })
        else:
            invalid_request = InvalidRequest.from_dict(
                {**validation_service.validate()})

        if invalid_request.has_errors():
            return invalid_request

        return AddProductRequest(adict)
