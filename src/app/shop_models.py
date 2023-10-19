from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from src.app.models import *

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
    category_id = Column(Integer, ForeignKey('categories.id'))  # Добавлен внешний ключ
    shelves = relationship("Shelf", secondary="product_shelf_association", back_populates="products")
    category = relationship("Category", back_populates="products")  # Добавлено отношение к категории
    ratings = relationship("Rating", back_populates="product")

class ProductShelfAssociation(Base):
    __tablename__ = 'product_shelf_association'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    shelf_id = Column(Integer, ForeignKey('shelves.id'))
    is_main = Column(Boolean, default=False)


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    order_number = Column(Integer, unique=True, nullable=False)
    order_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="orders", primaryjoin="Order.user_id == User.id")


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

