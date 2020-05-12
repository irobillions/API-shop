class ProductListSerializer:
    def __init__(self, product):
        self.data = {
            'success': True,
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'slug': product.slug,
            'marque': product.manufacturer,
            'quality': product.quality,
            'rating': product.rating,
            'comments': len(product.comments),
            'availability': product.availability,
            'image_urls': [image.file_path.replace('\\', '/') for image in product.images]
        }


def to_json_serializable(lists):
    list_products = []
    if lists:
        for p in lists:
            list_products.append(ProductListSerializer(p).data)

    return list_products
