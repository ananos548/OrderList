from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship

from src.database import Base


class Shelf(Base):
    __tablename__ = 'shelves'

    id = Column(Integer, primary_key=True)
    shelf_name = Column(String, nullable=False)
    products = relationship("Product", secondary="product_shelf_association", back_populates="shelves")


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer)
    shelves = relationship("Shelf", secondary="product_shelf_association", back_populates="products")


class ProductShelfAssociation(Base):
    __tablename__ = 'product_shelf_association'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    shelf_id = Column(Integer, ForeignKey('shelves.id'))
    is_main = Column(Boolean, default=False)


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    order_number = Column(String, unique=True, nullable=False)
    order_date = Column(DateTime, nullable=False)


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
