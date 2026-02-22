from sqlalchemy import Column, Integer, String, Float
from database import Base


class products_list(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    desc = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
