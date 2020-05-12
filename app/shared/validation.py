from dateutil.parser import parse


class ValidationError(AttributeError):
    def __init__(self, message):
        super().__init__(message)


class ValidationService:
    def __init__(self, attributes):
        self.rules = {}
        self.attributes = attributes

    def add_rules(self, rules):
        if not isinstance(rules, dict):
            raise NotImplementedError
        self.rules = rules
        self.create_rules()

    def create_rules(self):
        for attribute, rules in self.rules.items():
            for i, _ in enumerate(rules):
                self.rules[attribute][i].attribute = attribute
                self.rules[attribute][i].value = self.attributes.get(attribute)

    def validate(self):
        errors = {}
        for attribute, rules in self.rules.items():
            for rule in rules:
                try:
                    rule.validate()
                except ValidationError as e:
                    if not errors.get(attribute):
                        errors[attribute] = []
                    errors[attribute].append(str(e))
        return errors


class Rule(object):
    def __init__(self, attribute=None, value=None):
        self.attribute = attribute
        self.value = value

    def validate(self):
        raise NotImplementedError


class RequiredRule(Rule):
    def validate(self):
        if self.value is None or len(str(self.value)) == 0:
            raise ValidationError(
                f"The attribute {self.attribute} shouldn't be empty")

    @classmethod
    def build(cls):
        return cls()


class EmailRule(Rule):
    def validate(self):
        if '@' not in self.value:
            raise ValidationError(
                f"The attribute {self.attribute} is not a valid email")

    @classmethod
    def build(cls):
        return cls()


class MinLengthRule(Rule):
    def __init__(self, attribute=None, value=None, threshold=6):
        super().__init__(attribute, value)
        self.threshold = threshold

    def validate(self):
        if len(str(self.value)) < self.threshold:
            raise ValidationError(
                f"The attribute {self.attribute} should be at least {self.threshold}"
            )

    @classmethod
    def build(cls, threshold):
        return cls(threshold=threshold)


class BooleanRule(Rule):
    def validate(self):
        if type(self.value) is not bool:
            raise ValidationError(
                f"The attribute {self.attribute} should be a boolean")

    @classmethod
    def build(cls):
        return cls()


class FloatRule(Rule):
    def validate(self):
        if type(self.value) is not float:
            raise ValidationError(
                f"The attribute {self.attribute} should be a float")

    @classmethod
    def build(cls):
        return cls()


class IntegerRule(Rule):
    def validate(self):
        if type(self.value) is not int:
            raise ValidationError(
                f"The attribute {self.attribute} should be a integer")

    @classmethod
    def build(cls):
        return cls()


class DateTimeRule(Rule):
    def validate(self):
        try:
            parse(self.value)
        except Exception as e:
            raise ValidationError(
                f"{e}: The attribute {self.attribute} should be a datetime")

    @classmethod
    def build(cls):
        return cls()
