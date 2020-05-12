from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import DevelopmentConfig, TestingConfig
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
import os
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
mail = Mail()
bcrypt = Bcrypt()
cors = CORS()
migrate = Migrate()
jwt = JWTManager()


def create_app(testing=False):
    app = Flask(__name__, root_path=os.getcwd())
    if not testing:
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(TestingConfig)
    app.config['JWT_SECRET_KEY'] = os.urandom(35)
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

    db.init_app(app)
    mail.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.authentication import models
    from app.orders import models
    from app.products import models
    from app.adresses import models
    from app.comments import models
    from app.car import models
    from app.categories import models
    from app.quote import models
    from app.message import models
    from app.wishlist import models
    from app.files_Uploads import models
    from app.roles import models

    from app.authentication.views import users
    from app.orders.views import order
    from app.products.views import products
    from app.categories.views import category

    with app.app_context():
        app.register_blueprint(order)
        app.register_blueprint(users)
        app.register_blueprint(products)
        app.register_blueprint(category)

    return app
