from app.factory import db


class WishList(db.Model):
    __tablename__ = 'wishlists'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('User', db.Integer, db.ForeignKey('users.id'), nullable=False)
    product = db.relationship('Product', secondary='wishlistitems', lazy=False)


wishListItem = db.Table('wishlistitems',
                        db.Model.metadata,
                        db.Column('wishlist_id', db.Integer, db.ForeignKey('wishlists.id')),
                        db.Column('product_id', db.Integer, db.ForeignKey('products.id')))
