from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from src.database import Base



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    # Дополнительные поля о пользователе, например, имя, фамилия, адрес и т. д.
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)

    # Связь с заказами пользователя
    orders = relationship("Order", back_populates="user")
    ratings = relationship("Rating", back_populates="user")


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey('categories.id'))

    # Добавьте связь с товарами в этой категории
    products = relationship("Product", back_populates="category")

    # Добавьте связь с подкатегориями
    subcategories = relationship("Category", back_populates="parent", remote_side=[id])
    parent = relationship("Category", back_populates="subcategories")


class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rating = Column(Float, nullable=False)

    # Добавьте связи с пользователями и товарами
    user = relationship("User", back_populates="ratings")
    product = relationship("Product", back_populates="ratings")
