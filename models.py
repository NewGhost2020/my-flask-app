from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


def utc_now():
    return datetime.now(timezone.utc)


class Store(Base):
    __tablename__ = 'stores'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    url = Column(String(500), nullable=False)
    last_parsed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utc_now)
    
    products = relationship('Product', back_populates='store', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Store(id={self.id}, name='{self.name}')>"


class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(500), nullable=False)
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)
    url = Column(String(1000), nullable=False)
    image_url = Column(String(1000), nullable=True)
    original_price = Column(Float, nullable=True)
    current_price = Column(Float, nullable=False)
    is_on_sale = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    category = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    
    store = relationship('Store', back_populates='products')
    promotions = relationship('Promotion', back_populates='product', cascade='all, delete-orphan')
    price_history = relationship('PriceHistory', back_populates='product', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', current_price={self.current_price})>"


class Promotion(Base):
    __tablename__ = 'promotions'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    discount_percentage = Column(Float, nullable=False)
    sale_start = Column(DateTime, nullable=True)
    sale_end = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utc_now)
    
    product = relationship('Product', back_populates='promotions')
    
    def __repr__(self):
        return f"<Promotion(id={self.id}, product_id={self.product_id}, discount={self.discount_percentage}%)>"


class PriceHistory(Base):
    __tablename__ = 'price_history'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=utc_now)
    
    product = relationship('Product', back_populates='price_history')
    
    def __repr__(self):
        return f"<PriceHistory(id={self.id}, product_id={self.product_id}, price={self.price})>"
