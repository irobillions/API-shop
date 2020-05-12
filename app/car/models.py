from app.factory import db


class CarBrand(db.Model):
    __tablename__ = 'carbrands'
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(80), unique=True, index=True)

    carmodels = db.relationship('CarModel', backref='carbrand', lazy=False)
    cartypes = db.relationship('CarType', secondary='carbrand_types', backref='carbrand', lazy=False)

    def get_summary(self):
        carbrands = {
            'designation': self.designation,
            'brand_logos': [i.file_path for i in self.images]
        }
        if len(self.carmodels) > 0:
            carbrands['models'] = [{model.designation: model for model in self.carmodels}]  # a tester
            """{'modelname': [model.designation for model in self.carmodels],
                                               'typemodel': [model.type.designation for model in self.carmodels],
                                               'modeldateofprod': [model.date_of_prod for model in self.carmodels]}"""
            # ['modelname: ' + i.designation + ' | ' + 'typemodel: ' + i.type.designation for i in self.carmodels]
        return carbrands


class CarModel(db.Model):
    __tablename__ = 'carmodels'
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(300), unique=True, index=True, nullable=False)
    date_of_prod = db.Column(db.DateTime(), nullable=False)
    date_end_of_prod = db.Column(db.DateTime(), nullable=True)

    carbrand_id = db.Column(db.Integer, db.ForeignKey('carbrands.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('cartypes.id'), nullable=False)

    # carbrand = db.relationship('CarBrand', foreign_keys=[carbrand_id], lazy='dynamic')
    type = db.relationship('CarType', foreign_keys=[type_id], lazy=False)


class CarType(db.Model):
    __tablename__ = 'cartypes'
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(80), unique=True)


carbrand_types = \
    db.Table('carbrand_types',
             db.Column('carbran_id', db.Integer, db.ForeignKey('carbrands.id')),
             db.Column('cartype_id', db.Integer, db.ForeignKey('cartypes.id')))
