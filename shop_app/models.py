from .app import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image1 = db.Column(db.LargeBinary)
    image2 = db.Column(db.LargeBinary)
    image3 = db.Column(db.LargeBinary)
    image4 = db.Column(db.LargeBinary)

    def __repr__(self):
        return f'{self.name} {self.id}'

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'{self.category}'

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'{self.name} {self.email}'