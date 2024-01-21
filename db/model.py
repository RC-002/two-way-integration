from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'

    ID = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

class ID_Mapping(Base):
    __tablename__ = 'id_mapping'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String, ForeignKey('customer.ID'), unique=True, nullable=False)
    stripe_id = Column(String, unique=True, nullable=True)


# Unique constraint to ensure that customer_id and stripe_id are unique together
UniqueConstraint('customer_id', 'stripe_id', name='uq_id_mapping_customer_stripe_id')
