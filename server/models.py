from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationship with Review
    reviews = db.relationship('Review', back_populates='customer')
    
    # Add association proxy to get items through reviews
    items = association_proxy('reviews', 'item',
                            creator=lambda item_obj: Review(item=item_obj))
    
    # Add serialization rules to avoid recursion
    serialize_rules = ('-reviews.customer',)

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # Add relationship with Review
    reviews = db.relationship('Review', back_populates='item')
    
    # Add serialization rules to avoid recursion
    serialize_rules = ('-reviews.item',)

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    
    # Add foreign keys
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    
    # Add relationships with back_populates
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')
    
    # Add serialization rules to avoid recursion
    serialize_rules = ('-customer.reviews', '-item.reviews',)

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}, Customer: {self.customer_id}, Item: {self.item_id}>'