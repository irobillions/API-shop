import json

from flask import Blueprint, request, Response
from flask_jwt_extended import jwt_required

from app.shared.serializers import STATUS_CODE
from app.categories.infrastructure.services import CategoryEncoder
from app.categories.shared.request import AddCategoryRequest, ListCategoriesRequest
from app.shared.decorators import has_role
from .domain.use_cases import AddCategoryUseCase, ListCategoriesUseCase
from .infrastructure.repositories import FlaskCategoryRepository

category = Blueprint('category', __name__, url_prefix='/categories')


@category.route('/', methods=['POST'])
@jwt_required
@has_role("ROLE_SELLER")
def create_category():
    add_category_use_case = AddCategoryUseCase(FlaskCategoryRepository())
    result = add_category_use_case(
        AddCategoryRequest.build_from_dict(request.json))
    return Response(json.dumps(result.value, cls=CategoryEncoder),
                    content_type="application/json",
                    status=STATUS_CODE[result.type])


@category.route('/', methods=['GET'])
def list_categories():
    list_categories_use_case = ListCategoriesUseCase(FlaskCategoryRepository())
    result = list_categories_use_case(ListCategoriesRequest())
    return Response(json.dumps(result.value, cls=CategoryEncoder),
                    content_type="application/json",
                    status=STATUS_CODE[result.type])
