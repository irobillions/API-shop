from .entities import Category


# the category repository for communicate the domain with data but here we only put an interface because
# it must have an abstraction between data , the application shouldn't access directly to data it's like a contract
class CategoryRepository:
    def save(self, category: Category) -> Category:
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError
