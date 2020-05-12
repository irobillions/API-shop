import os
import json
from pprint import pprint
from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity
from sqlalchemy import desc
from werkzeug.utils import secure_filename
from app.factory import create_app
from app.products.models import Product, db
from app.products.serializer import ProductListSerializer
from app.products.serializer import to_json_serializable
from app.shared.decorators import has_role
from app.shared.security import validate_file_upload
from app.shared.serializers import get_success_response, get_error_response
from app.products.shared.request import AddProductRequest
from app.products.infrastructure.repositories import FlaskProductRepository
from app.products.domain.use_cases import AddProductUseCase
from app.shared.serializers import STATUS_CODE
from app.products.infrastructure.services import ProductEncoder
from app.categories.infrastructure.repositories import FlaskCategoryRepository

products = Blueprint('product', __name__, url_prefix='/products')

app = create_app()


# client
@products.route('/products-list', methods=['GET'])
def list_product():
    products = Product.query.order_by(desc(Product.publish_on)).paginate(
        error_out=False, per_page=3)
    if not products:
        return get_error_response('server error')

    results = [ProductListSerializer(data).data for data in products.items]

    return jsonify({
        'success': True,
        'data': {
            "items": results,
            "current_page": products.page,
            "total_pages": products.pages
        }
    }), 200


@products.route('/', methods=['POST'])
@jwt_required
def create_product():
    seller_id = get_jwt_identity()
    data = request.json
    data.update({"seller": seller_id})
    product_save_use_case = AddProductUseCase(
        FlaskProductRepository(FlaskCategoryRepository()))
    result = product_save_use_case(AddProductRequest.build_from_dict(data))
    return Response(json.dumps(result.value, cls=ProductEncoder),
                    mimetype="application/json",
                    status=STATUS_CODE[result.type])
    # seller_id = get_jwt_identity()
    # product = Product(name=request.json['name'],
    # description=request.json['description'],
    # availability=request.json['availability'],
    # quality=request.json['quality'],
    # price=request.json['price'],
    # stock=request.json['stock'],
    # seller_id=seller_id,
    # manufacturer=request.json['manufacturer'])
    # product.slug_generator_for_product(product.seller_id, product.name)
    # db.session.add(product)
    # db.session.commit()
    # return {
    # "id": product.id,
    # "name": product.name,
    # "slug": product.slug,
    # "description": product.description,
    # "availability": product.availability,
    # "quality": product.quality,
    # "price": product.price,
    # "stock": product.stock,
    # "seller_id": seller_id,
    # "manufacturer": product.manufacturer
    # }


@products.route('/product/<slug_product>', methods=['GET'])
@jwt_required
@has_role('ROLE_USER')
def get_detail_product_by_slug(slug_product):
    specific_product = Product.query.filter(
        Product.slug == slug_product).first()

    if not specific_product:
        return get_error_response('product not found', 404)

    return jsonify({'product': specific_product.get_summary()}), 200


@products.route('/product/by_id/<product_id>', methods=['GET'])
@jwt_required
@has_role('ROLE_USER')
def get_detail_product_by_id(product_id):
    prdt = Product.query.filter_by(id=product_id).first()
    print(prdt)
    if prdt is None:
        return get_error_response('product not found', 404)
    return jsonify({'product': prdt.get_summary()}), 200


# seller
@products.route('/list-all-products', methods=['GET'])
@jwt_required
@has_role('ROLE_SELLER')
def get_all_specific_seller_products():
    user = current_user

    seller_product = Product.query.order_by(desc(
        Product.publish_on)).filter(Product.seller_id == user.id).all()
    list_seller_product = to_json_serializable(seller_product)
    return jsonify({
        'seller_id': user.id,
        'products': list_seller_product
    }), 200


@products.route('/product/seller/<slug_product>', methods=['GET'])
@jwt_required
@has_role('ROLE_SELLER')
def get_seller_detail_product_by_slug(slug_product):
    user = current_user
    specific_product = Product.query.filter(
        Product.slug == slug_product).filter(
        Product.seller_id == user.id).first()

    if not specific_product:
        return get_error_response('product not found', 404)

    return jsonify({
        'seller_id': user.id,
        'product': specific_product.get_summary()
    }), 200


"""
@products.route('/add-new-product', methods=['POST'])
@jwt_required
@has_role('ROLE_SELLER')
def add_product():
    user = current_user

    product_name = request.json.get('name', None)
    description = request.json.get('description', None)
    availability = request.json.get('availability', 1)
    quality = request.json.get('quality', None)
    price = request.json.get('price', None)
    stock = request.json.get('stock', None)
    manufacturer = request.json.get('manufacturer', None)
    is_a_part = request.json.get('is_a_part', False)

    if is_a_part:
        ref_part = request.json.get('ref_num_part', None)
        weight = request.json.get('weight', None)
        diameter = request.json.get('diameter', None)
        dimension = request.json.get('dimension', None)
        date_of_prod = request.json.get('date_of_prod', None)
        num_oem = request.json.get('num_oem', None)
        country_of_origin = request.json.get('country_of_origin', None)
        volume_of_part = request.json.get('volume_of_part', None)
        car_compt_ids = request.json.get('car_compts_id', None)

    category_id = request.json.get('category', None)

    if category_id is None:
        new_category_name = request.json.get('new_category', None)
        cat_description = request.json.get('cat_description', None)

    product = Product(name=product_name, description=description, price=price, stock=stock,
                      tags=tags, categories=categories)
    if 'images[]' in request.files:
        for image in request.files.getlist('images[]'):
            if image and validate_file_upload(image.filename):
                filename = secure_filename(image.filename)
                dir_path = app.config['IMAGES_LOCATION']
                dir_path = os.path.join((os.path.join(dir_path, 'products')))

                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)

                file_path = os.path.join(dir_path, filename)
                image.save(file_path)

                file_path = file_path.replace(app.config['IMAGES_LOCATION'].rsplit(os.sep, 2)[0], '')
                if image.content_length == 0:
                    file_size = image.content_length
                else:
                    file_size = os.stat(file_path).st_size

                product_image = ProductImage(file_path=file_path, file_name=filename, original_name=image.filename,
                                             file_size=file_size)
                product.images.append(product_image)

    db.session.add(product)
    db.session.commit()

    response = {'full_messages': ['Product created successfully']}
    response.update(product.get_summary())
    return jsonify(response)
     return 'cc'
    """
