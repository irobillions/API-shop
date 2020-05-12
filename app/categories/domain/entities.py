# we use clean architecture so here is the domain part of auth each great module of our app need different part
# we put here only the python code without relation with application
# that's why there is not id here because id are in application part and infrastructure


class Category:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @classmethod
    def from_dict(cls, adict):
        return cls(name=adict.get('name'),
                   description=adict.get('description'))