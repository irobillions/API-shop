from ..domain.repository import ProductRepository
from ..models import Product, db, PartData
from datetime import datetime


class FlaskProductRepository(ProductRepository):
    def __init__(self, category_repo):
        self.category_repo = category_repo

    def save(self, product):
        part_data_to_save = None
        if product.part_data:
            part_data_to_save = PartData(
                ref_part=product.part_data.ref_part,
                weight=product.part_data.weight,
                diameter=product.part_data.diameter,
                dimension=product.part_data.dimension,
                date_of_prod=datetime.strptime(product.part_data.date_of_prod,
                                               "%Y-%m-%d %H:%M:%S"),
                num_oem=product.part_data.num_oem,
                country_of_origin=product.part_data.country_of_origin,
                volume_of_part=product.part_data.volume_of_part,
            )
        product_to_save = Product(name=product.name,
                                  description=product.description,
                                  availability=product.availability,
                                  quality=product.quality,
                                  price=product.price,
                                  stock=product.stock,
                                  seller_id=product.seller,
                                  manufacturer=product.manufacturer,
                                  partdata=part_data_to_save)
        product_to_save.categories = self.category_repo.get_in_list(
            product.categories)

        db.session.add(product_to_save)
        db.session.commit()
        product.id = product_to_save.id
        product.categories = product_to_save.categories
        return product
