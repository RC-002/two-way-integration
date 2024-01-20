from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'

    ID = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

def create_engine_and_session():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return engine, session

# Create Customer
def createCustomer(session, id, name, email):
    try:
        newCustomer = Customer(ID=id, name=name, email=email)
        session.add(newCustomer)
        session.commit()
        return True
    except:
        return False

# Get Customer
def getCustomer(session, customer_id):
    try:
        return session.query(Customer).filter(Customer.ID == customer_id).first()
    except:
        return False

def getAllCustomers(session):
    try:
        return session.query(Customer).all()
    except:
        return False
    
def updateCustomer(session, customer_id, new_name, new_email):
    try:
        customer = session.query(Customer).filter(Customer.ID == customer_id).first()
        if customer:
            customer.name = new_name
            customer.email = new_email
            session.commit()
        return True
    except:
        return False

def deleteCustomer(session, customer_id):
    try:
        customer = session.query(Customer).filter(Customer.ID == customer_id).first()
        if customer:
            session.delete(customer)
            session.commit()
        return True
    except:
        return False

def closeConnection(engine, session):
    session.close()
    engine.dispose()

if __name__ == "__main__":
    engine, session = create_engine_and_session()