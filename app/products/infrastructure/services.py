import json
from ..domain.entities import Product, PartData
from app.categories.infrastructure.services import CategoryEncoder


class ProductEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Product):
            return {
                "id":
                obj.id,
                "name":
                obj.name,
                "description":
                obj.description,
                "availability":
                obj.availability,
                "quality":
                obj.quality,
                "price":
                obj.price,
                "stock":
                obj.stock,
                "manufacturer":
                obj.manufacturer,
                "part_data":
                json.loads(json.dumps(obj.part_data, cls=PartDataEncode)),
                "categories":
                json.loads(json.dumps(obj.categories, cls=CategoryEncoder))
            }

        return json.JSONEncoder.default(self, obj)


class PartDataEncode(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, PartData):
            return {
                "ref_part": obj.ref_part,
                "weight": obj.weight,
                "diameter": obj.diameter,
                "dimension": obj.dimension,
                "date_of_prod": obj.date_of_prod,
                "num_oem": obj.num_oem,
                "country_of_origin": obj.country_of_origin,
                "volume_of_part": obj.volume_of_part,
            }
        return json.JSONEncoder.default(self, obj)
