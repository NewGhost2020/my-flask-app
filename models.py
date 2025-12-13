"""
Database models for promotions scraper
Uses SQLAlchemy ORM for database operations
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class Promotion(Base):
    """Promotion model for storing promotional products"""
    __tablename__ = 'promotions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    store_name = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    
    __table_args__ = (
        UniqueConstraint('store_name', 'product_name', 'date', name='unique_promotion'),
    )
    
    def __repr__(self):
        return f"<Promotion(id={self.id}, store={self.store_name}, product={self.product_name}, price={self.price})>"
    
    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            'id': self.id,
            'store_name': self.store_name,
            'product_name': self.product_name,
            'price': self.price,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S') if isinstance(self.date, datetime) else self.date
        }


class DatabaseManager:
    """Manages database connections and sessions"""
    
    def __init__(self, db_name='promotions.db'):
        """Initialize database manager"""
        self.db_name = db_name
        self.engine = create_engine(f'sqlite:///{db_name}', echo=False)
        self.Session = sessionmaker(bind=self.engine)
    
    def init_database(self):
        """Create all tables if they don't exist"""
        Base.metadata.create_all(self.engine)
    
    def get_session(self):
        """Get a new database session"""
        return self.Session()
    
    def close(self):
        """Close database connection"""
        self.engine.dispose()
