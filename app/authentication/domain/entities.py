# we use clean architecture so here is the domain part of auth each great module of our app need different part
# we put here only the python code without relation with application
# that's why there is not id here because id are in application part and infrastructure


class User:
    def __init__(self, first_name: str, last_name: str, username: str, email: str, password: str, roles: str):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password
        self.roles = roles

    # to build an user object from dictionary
    @classmethod
    def from_dict(cls, adict):
        return cls(first_name=adict['firstName'],
                   last_name=adict['lastName'],
                   username=adict['username'],
                   email=adict['email'],
                   password=adict['password'],
                   roles=adict['roles'])
