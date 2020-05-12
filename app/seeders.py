import sys
from datetime import datetime
import random
import faker
from sqlalchemy import func
from app.adresses.models import Address
from app.categories.models import Category
from app.comments.models import Comment
from app.factory import db, create_app, bcrypt
from app.file_Uploads.models import ProductImage
from app.products.models import Product, PartData
from app.roles.models import Role
from app.authentication.models import User

create_app().app_context().push()
fake = faker.Faker()


def generate_image(model):
    # pattern = "".join([random.choice(['?', '#']) for i in range(0, 10)]) + '.png'
    filename_pattern = "".join(fake.random_choices(elements=('?', '#'),
                                                   length=fake.random_int(min=16, max=32))) + '.png'
    # file_name=fake.md5(raw_output=False) + '.png'
    return model(file_name="".join(fake.random_letters(length=16)) + '.png',
                 file_path=fake.image_url(width=None, height=None),
                 file_size=fake.random_int(min=1000, max=15000),
                 original_name=fake.bothify(text=filename_pattern))


"""user and seller seed"""


def seed_roles():
    db.session.add(Role(name="ROLE_USER", description="Role utilisateur"))
    db.session.add(Role(name="ROLE_SELLER", description="Role fournisseur"))
    db.session.commit()


seed_roles()


def seed_user():
    role_user = Role.query.filter(Role.name == 'ROLE_USER').first()
    role_seller = Role.query.filter(Role.name == 'ROLE_SELLER').first()
    user1 = User(first_name=fake.first_name(), last_name=fake.last_name(), username='user1',
                 password=bcrypt.generate_password_hash('password').decode('utf-8'), email=fake.email(),
                 roles=[role_user])
    user2 = User(first_name=fake.first_name(), last_name=fake.last_name(), username='user2',
                 password=bcrypt.generate_password_hash('password').decode('utf-8'), email=fake.email(),
                 roles=[role_user])
    user3 = User(first_name=fake.first_name(), last_name=fake.last_name(), username='user3',
                 password=bcrypt.generate_password_hash('password').decode('utf-8'), email=fake.email(),
                 roles=[role_user])
    user4 = User(first_name=fake.first_name(), last_name=fake.last_name(), username='user4',
                 password=bcrypt.generate_password_hash('password').decode('utf-8'), email=fake.email(),
                 roles=[role_user])
    seller1 = User(first_name=fake.first_name(), last_name=fake.last_name(), username='seller1',
                   password=bcrypt.generate_password_hash('password').decode('utf-8'), email=fake.email(),
                   roles=[role_seller])
    seller2 = User(first_name=fake.first_name(), last_name=fake.last_name(), username='seller2',
                   password=bcrypt.generate_password_hash('password').decode('utf-8'), email=fake.email(),
                   roles=[role_seller])
    seller3 = User(first_name=fake.first_name(), last_name=fake.last_name(), username='seller3',
                   password=bcrypt.generate_password_hash('password').decode('utf-8'), email=fake.email(),
                   roles=[role_seller])
    seller4 = User(first_name=fake.first_name(), last_name=fake.last_name(), username='seller4',
                   password=bcrypt.generate_password_hash('password').decode('utf-8'), email=fake.email(),
                   roles=[role_seller])
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(seller1)
    db.session.add(seller2)
    db.session.add(seller3)
    db.session.add(seller4)
    db.session.commit()


seed_user()
start_date = datetime(year=2017, month=1, day=1)
random_date = fake.date_between(start_date=start_date, end_date='+4y')

"""seed categories"""


def seed_categories():
    cat1 = Category(name='freins', slug=fake.slug(value='cat-01-freins'), description=fake.text(max_nb_chars=200),
                    created_at=random_date)
    cat2 = Category(name='carosserie', slug=fake.slug(value='cat-02-freins'), description=fake.text(max_nb_chars=200),
                    created_at=random_date)
    cat3 = Category(name='transmission', slug=fake.slug(value='cat-03-freins'), description=fake.text(max_nb_chars=200),
                    created_at=random_date)
    cat4 = Category(name='moteur', slug=fake.slug(value='cat-04-freins'), description=fake.text(max_nb_chars=200),
                    created_at=random_date)
    cat5 = Category(name='accessoires et equipements', slug=fake.slug(value='cat-05-freins'),
                    description=fake.text(max_nb_chars=200), created_at=random_date)
    cat6 = Category(name='eclairage', slug=fake.slug(value='cat-06-freins'), description=fake.text(max_nb_chars=200),
                    created_at=random_date)
    cat7 = Category(name='equipement interieur', slug=fake.slug(value='cat-07-freins'),
                    description=fake.text(max_nb_chars=200), created_at=random_date)
    db.session.add_all([cat1, cat2, cat3, cat4, cat5, cat6, cat7])
    db.session.commit()


"""
# product seed
# partdata_product1 = PartData(ref_part=fake.ean8(), weight=fake.random_int(min=5, max=20), diameter=fake.random_int(min=2,max=30), dimension=fake.random_int(min=2, max=30), date_of_prod=random_date, num_oem=fake.upc_a(upc_ae_mode=True, number_system_digit=1), country_of_origin=fake.country(), volume_of_part=fake.random_int(min=20,max=50), manufacturer=fake.company())
"""

seed_categories()
categories = Category.query.all()
sellers = User.query.filter(User.roles.any(name='ROLE_SELLER')).all()
sellers_id = [s.id for s in sellers]


def seed_products():
    products_count = db.session.query(func.count(Product.id)).all()[0][0]
    products_to_seed = 13
    sys.stdout.write('[+] Seeding %d products\n' % products_to_seed)
    quality = ['origine', 'adaptable']
    # tag_ids = [tag[0] for tag in db.session.query(Tag.id).all()]
    # category_ids = [categories[0] for categories in db.session.query(Category.id).all()]
    for i in range(products_count, products_to_seed):
        product = Product(name=fake.sentence(), slug=fake.slug(),
                          description=fake.text(max_nb_chars=200), availability=True, quality=random.choice(quality),
                          price=fake.random_int(min=50, max=2500), stock=fake.random_int(min=5, max=500),
                          rating=fake.random_int(min=0, max=5), seller_id=random.choice(sellers_id),
                          manufacturer=fake.sentence(),
                          publish_on=random_date)
        categories_for_product = []
        category_to_add = random.choice(categories)
        if category_to_add.id not in categories_for_product:
            product.categories.append(category_to_add)
            categories_for_product.append(category_to_add.id)
        for i in range(0, random.randint(1, 2)):
            product_image = generate_image(ProductImage)
            product.images.append(product_image)
        db.session.add(product)
        db.session.commit()


def seed_comments():
    comments_count = db.session.query(func.count(Comment.id)).scalar()
    comments_to_seed = 20
    comments_to_seed -= comments_count
    sys.stdout.write('[+] Seeding %d comments\n' % comments_to_seed)
    comments = []
    user_ids = [user[0] for user in User.query.with_entities(User.id).filter(User.roles.any(name='ROLE_USER')).all()]
    product_ids = [product[0] for product in Product.query.with_entities(Product.id)]
    # equivalent:
    # user_ids = [user[0] for user in db.session.query(User.id).all()]
    # product_ids = [product[0] for product in db.session.query(Product.id).all()]
    for i in range(comments_count, comments_to_seed):
        user_id = random.choice(user_ids)
        product_id = random.choice(product_ids)
        rating = fake.random_int(min=1, max=5) if fake.boolean(chance_of_getting_true=50) else None
        comments.append(Comment(product_id=product_id,
                                user_id=user_id, rating=rating,
                                content=fake.paragraph(nb_sentences=4, variable_nb_sentences=True, ext_word_list=None),
                                created_at=random_date))
    db.session.add_all(comments)
    db.session.commit()


def seed_addresses():
    addresses_count = db.session.query(func.count(Address.id)).scalar()
    addresses_to_seed = 8
    user_ids = [user[0] for user in User.query.with_entities(User.id).filter(User.roles.any(name='ROLE_USER')).all()]

    for i in range(addresses_count, addresses_to_seed):
        user_id = random.choice(user_ids) if fake.boolean(chance_of_getting_true=80) else None

        first_name = fake.first_name()
        last_name = fake.last_name()
        zip_code = fake.zipcode_plus4()  # postcode(), postalcode(), zipcode(), postalcode_plus4
        street_address = fake.address()
        phone_number = fake.phone_number()
        city = fake.city()
        country = fake.country()
        db.session.add(Address(user_id=user_id, first_name=first_name, last_name=last_name, zip_code=zip_code,
                               street_address=street_address, phone_number=phone_number, city=city,
                               country=country))
        db.session.commit()


if __name__ == '__main__':
    seed_products()
    seed_comments()
    seed_addresses()
