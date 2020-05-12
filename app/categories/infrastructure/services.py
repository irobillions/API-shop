import json
from app.categories.models import Category


class CategoryEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Category):
            return {"id": o.id, "name": o.name, "description": o.description}
        return json.JSONEncoder.default(self, o)
