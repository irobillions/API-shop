from copy import deepcopy
from collections import defaultdict
from pprint import pprint

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_claims, current_user

from app.adresses.models import Address
from app.adresses.utils import check_existing_address_delivery
from app.orders.models import Order, OrderItem
from app.factory import db, jwt
from sqlalchemy import desc, text

from app.orders.serializer import OrderListSerializer
from app.orders.serializer import check_product_availability, show_order_detail_by_role
from app.products.models import Product
from app.shared import security
from app.shared.decorators import has_role
from app.shared.serializers import get_error_response, get_success_response
from app.authentication.models import User

order = Blueprint('orders', __name__, url_prefix='/orders')


# client order operation
@order.route('/client-orders', methods=['GET'])
@jwt_required
@has_role('ROLE_USER')
def get_all_client_orders():
    claims_data = get_jwt_claims()
    user_id = claims_data.get('user_id')

    if not user_id:
        return get_error_response('UNAUTHORIZED', 401)

    orders = Order.query.filter_by(user_id=user_id).order_by(desc(Order.created_at)).paginate()
    return jsonify(OrderListSerializer(orders).get_data()), 200


@order.route('/user-orders/<order_id>', methods=['GET'])
@jwt_required
def get_order_details(order_id):
    user = current_user

    single_order = Order.query.filter(Order.id == order_id).first()

    if single_order is None:
        return get_error_response('ERROR ORDER DOES NOT EXIST IN DATABASE', 400)

    return show_order_detail_by_role(user, single_order)


@order.route('/client-orders/create-order', methods=['POST'])
@jwt_required
@has_role('ROLE_USER')
def create_order():
    user = current_user  # demander a yoa si ce n'est pas dangereux de recuperer tous l'utilisateur
    # print(user.id)
    # print(request.get_json())
    address_id = request.json.get('address_id', None)
    # print(address_id)
    import faker
    fake = faker.Faker()
    if address_id is None:
        if check_existing_address_delivery(user.id) is None:
            return get_error_response('you address is required for delivery', 400)
        address_id = check_existing_address_delivery(user.id)

    check_address = Address.query.filter(Address.user_id == user.id).filter(Address.id == address_id).first()
    # print(check_address)
    if check_address is None:
        return get_error_response('unauthorized address', 401)

    cart_items = request.json.get('cart_items', None)
    print(len(cart_items))
    # print(cart_items)
    if not cart_items:
        return get_error_response('YOU CAN\'T SUBMIT AN ORDER WITH NO ITEM', 400)

    delivery_mode = request.json.get('delivery_mode', 0)
    paiement_method = request.json.get('paiement_method', 0)
    product_ids = [ci['product_id'] for ci in cart_items]
    products_ordered = Product.query.filter(Product.id.in_(product_ids)).all()
    print(len(products_ordered))
    checking_avl = check_product_availability(products_ordered)  # voir si c'est pas mieux dans un middleware

    if type(checking_avl) == dict:
        return jsonify({'message': checking_avl['message'], 'product_ids': checking_avl['product_ids']})

    if len(products_ordered) != len(cart_items):
        return get_error_response('make sure that all product you want to order is available', 400)

    final_products = list(map(lambda x: {"prdt": x, "quantity": list(filter(lambda y: y["product_id"] == x.id,
                                                                            cart_items))[0]["quantity"],
                                         "seller_id": x.seller_id}, products_ordered))
    f = defaultdict(list)
    for v in final_products:
        f[v["seller_id"]].append(v)

    test_tuple = ("seller_id", "products")
    result = [{test_tuple[i]: fitem[i] for i, _ in enumerate(fitem)} for fitem in f.items()]
    pprint(result)
    all_orders = []
    for order_from_client in result:
        new_order = Order(order_status=5,
                          tracking_number=fake.uuid4(),
                          address_id=address_id,
                          delivery_mode=delivery_mode,
                          user_id=user.id,
                          seller_id=order_from_client['seller_id'],
                          paiement_method=paiement_method)
        all_orders.append(new_order)

    print(all_orders)

    for index, s_order in enumerate(all_orders):
        for order_item in result[index]['products']:
            s_order.order_items.append(OrderItem(price=order_item['prdt'].price,
                                                 quantity=order_item['quantity'],
                                                 product_id=order_item['prdt'].id,
                                                 product=order_item['prdt'],
                                                 name=order_item['prdt'].name))

    for o in all_orders:
        o.get_total_amount()
        for item in o.order_items:
            item.slug_generator_for_item(prdt_name=item.name, username=user.username)

    db.session.add_all(all_orders)
    db.session.commit()
    n_orders = Order.query.filter(Order.tracking_number.in_([o.tracking_number for o in all_orders])).all()
    print(n_orders)
    return get_success_response('Order created successfully', data=[o.get_summary() for o in n_orders], status_code=201)


# seller order operation
@order.route('/seller-orders', methods=['GET'])
@jwt_required
@has_role('ROLE_SELLER')
def get_all_orders_of_seller_concerned_with():
    user = current_user

    seller_orders = Order.query.order_by(desc(Order.created_at)).filter(Order.seller_id == user.id).paginate()

    return jsonify(OrderListSerializer(seller_orders).get_data()), 200


@order.route('/edit-order/<tracking_number>', methods=['PUT'])
@jwt_required
@has_role('ROLE_USER')
def edit_order(tracking_number):
    user = current_user
    order_to_edit = Order.query.filter(Order.tracking_number == tracking_number).first()
    print(order_to_edit)

    if not order_to_edit:
        return get_error_response('not found', 404)

    if order_to_edit.user_id != user.id:  # demander a yoa si ce n'est pas mieux de coupler avec la requet precedente
        return get_error_response('unauthorized, this not belong to you', 401)

    if order_to_edit.order_status == 1 or order_to_edit.order_status == 2 or order_to_edit.order_status == 3 or order_to_edit.order_status == 4:  # demander a yoa une facon plus professionell de faire
        return get_error_response('you can not edit this order because it is already delivered or in transit either '
                                  'canceled', 401)
    order_items_to_edit = request.json.get('order_item', None)

    if not order_items_to_edit or len(order_items_to_edit) == 0:
        return get_error_response('you can not submit no editing data', 400)

    for item in order_items_to_edit:

        if not item['is_deleting']:
            try:
                if not item['quantity']:
                    return get_error_response('you must supply a quantity to edit item', 400)
            except KeyError:
                return get_error_response('you must supply a quantity to edit item', 400)
            try:
                order_item_to_edit = OrderItem.query.filter(OrderItem.slug == item['slug']).filter(
                    OrderItem.order_id == order_to_edit.id).first()

                order_item_to_edit.quantity = item['quantity']
                db.session.commit()
                print('editing ok', item['slug'])
            except Exception as e:
                print(e)
                return get_error_response('server error' + str(e))
        if item['is_deleting']:
            try:
                order_item_to_delele = OrderItem.query.filter(OrderItem.slug == item['slug']).filter(
                    OrderItem.order_id == order_to_edit.id).first()
                db.session.delete(order_item_to_delele)
                db.session.commit()
                print('deleting ok', item['slug'])
            except Exception as e:
                print(e)
                return get_error_response('server error' + str(e))

    order_to_edit.get_total_amount()
    db.session.commit()

    return get_success_response('operation did successfully', 200)


@order.route('/cancel-order/<tracking_number>', methods=['DELETE'])
@jwt_required
@has_role('ROLE_USER')
def cancel_specific_order(tracking_number):
    user = current_user
    order_to_cancel = Order.query.filter(Order.tracking_number == tracking_number).first()

    if not order_to_cancel:
        return get_error_response('not found', 404)

    if order_to_cancel.user_id != user.id:
        return get_error_response('unauthorized, this not belong to you', 401)

    if order_to_cancel.order_status == 1 or order_to_cancel.order_status == 2 or order_to_cancel.order_status == 3 or order_to_cancel.order_status == 4:  # demander a yoa une facon plus professionell de faire
        return get_error_response('you can not edit this order because it is already delivered or in transit either '
                                  'canceled', 401)

    order_to_cancel.order_status = 4
    db.session.commit()

    return get_success_response('order was canceled', 200)


@order.route('/processing-orders', methods=['PUT'])
@jwt_required
@has_role('ROLE_SELLER')
def process_order():
    pass
