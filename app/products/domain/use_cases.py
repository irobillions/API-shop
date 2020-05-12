from .entities import Product
from app.shared.use_case import UseCase
import app.shared.response as res


class AddProductUseCase(UseCase):
    def __init__(self, product_repo):
        self.product_repo = product_repo

    def process_request(self, request):
        product = Product.from_dict(request.attributes)
        saved_product = self.product_repo.save(product)
        return res.ResponseSuccess(saved_product)
