import app.shared.response as res
from app.shared.use_case import UseCase
from .entities import Category


# this is all authentication use case we put it in the domain because it is pure python code
# and do not communicate with database directly et do not depend from another module
# for each use case we use a request which is sent from the client side and we process it
class AddCategoryUseCase(UseCase):
    def __init__(self, category_repo):
        self.category_repo = category_repo

    def process_request(self, request):
        category = Category.from_dict(request.attributes)
        response = self.category_repo.save(category)
        return res.ResponseSuccess(response)


class ListCategoriesUseCase(UseCase):
    def __init__(self, category_repo):
        self.category_repo = category_repo

    def process_request(self, request):
        categories = self.category_repo.get_all()
        return res.ResponseSuccess({"items": categories})
