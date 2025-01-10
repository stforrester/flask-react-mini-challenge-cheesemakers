from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

db = SQLAlchemy()


class Producer(db.Model, SerializerMixin):
    __tablename__ = "producers"

    id = db.Column(db.Integer, primary_key=True)
    founding_year = db.Column(db.Integer)
    name = db.Column(db.String)
    region = db.Column(db.String)
    operation_size = db.Column(db.String)
    image = db.Column(db.String)

    # Relationship mapping the producer to related cheeses
    cheeses = db.relationship(
        'Cheese', back_populates="producer", cascade='all, delete-orphan')


    def __repr__(self):
        return f"<Producer {self.id}>"

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Must have a name")
        return name

    @validates('founding_year')
    def validate_founding_year(self, key, year):
        if not (1900 <= year <= datetime.now().year):
            raise ValueError("Must be between 1900 and present")
        return year
    
    @validates('operation_size')
    def validate_operation_size(self, key, size):
        size_options = ["small", "medium", "large", "family", "corporate"]
        if size not in size_options:
            raise ValueError("Must be one of the following:", size_options)
        return size

class Cheese(db.Model, SerializerMixin):
    __tablename__ = "cheeses"

    id = db.Column(db.Integer, primary_key=True)
    production_date = db.Column(db.DateTime)
    price = db.Column(db.Float)
    kind = db.Column(db.String)
    image = db.Column(db.String)
    is_raw_milk = db.Column(db.Boolean)

    producer_id = db.Column(db.Integer, db.ForeignKey('producers.id'))
    producer = db.relationship('Producer', back_populates="cheeses")

    def __repr__(self):
        return f"<Cheese {self.id}>"
    
    @validates('production_date')
    def validate_production_date(self, key, date):
        date = datetime.strptime(date, "%Y-%m-%d")
        if date >= datetime.now():
            raise ValueError("Date must be before today")
        return date
    
    @validates('price')
    def validate_price(self, key, price):
        if not (1.00 <= price <= 45.00):
            raise ValueError("Price must be between 1.00 and 45.00")
        return price
