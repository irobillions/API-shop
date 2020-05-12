import random

from app.adresses.models import Address
from app.shared.serializers import get_error_response


def check_existing_address_delivery(user_id):
    user_addresses = Address.query.filter(Address.user_id == user_id).all()

    if user_addresses:
        user_address_ids = []
        for address in user_addresses:
            user_address_ids.append(address.id)
        return random.choice(user_address_ids)
    else:
        return None
