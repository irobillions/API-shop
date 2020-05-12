from app.shared.serializers import PageSerializer
from flask import jsonify

from app.shared.serializers import get_error_response


class OrderListSerializer(PageSerializer):
    resource_name = 'orders'


def check_product_availability(products_ordered):
    not_available_product = []
    for prdt in products_ordered:
        if prdt.stock <= 0:
            not_available_product.append(prdt.id)

    if len(not_available_product) > 0:
        msg = 'products ' + ' '.join(list(map(str, not_available_product))) + ' are not available for the moment'
        return {'message': msg, 'product_ids': not_available_product}
    return None


def show_order_detail_by_role(user, order):
    if 'ROLE_USER' in [r.name for r in user.roles]:
        if order.user_id == user.id:
            return jsonify({'order': order.get_summary(include_order_item=True)}), 200
        else:
            return get_error_response('ACCESS DENIED, THIS NOT BELONG TO YOU', 401)

    elif 'ROLE_SELLER' in [r.name for r in user.roles]:  # revoir cela avec yoa
        if order.seller_id == user.id:
            return jsonify({'order': order.get_summary(include_order_item=True)}), 200
        else:
            return get_error_response('ACCESS DENIED, THIS NOT BELONG TO YOU', 401)
    else:
        return get_error_response('UNAUTHORIZED', 401)
