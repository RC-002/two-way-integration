from customers.model import Customer
from customers.repository import dbConnectivity

import uuid

class Helper():    
    def generateUUID(size=32):
        # Generate random UUID
        random_uuid = uuid.uuid4()

        # Convert UUID to hexadecimal and truncate to the desired size
        hex_uuid = format(random_uuid.int, 'x')[:size]

        return str(hex_uuid)
    
class dbService():
    def __init__(self):
        self.engine, self.session = dbConnectivity.create_engine_and_session()

    def createCustomer(self, name, email):
        try:
            id = Helper.generateUUID(32)
            new_customer = Customer(ID=id, name=name, email=email)
            self.session.add(new_customer)
            self.session.commit()
            return True
        except:
            self.session.rollback()
            return False

    def getCustomer(self, customer_id):
        try:
            return self.session.query(Customer).filter(Customer.ID == customer_id).first()
        except:
            self.session.rollback()
            return False

    def getAllCustomers(self):
        try:
            return self.session.query(Customer).all()
        except:
            return False

    def updateCustomer(self, customer_id, new_name, new_email):
        try:
            customer = self.session.query(Customer).filter(Customer.ID == customer_id).first()
            if customer:
                customer.name = new_name
                customer.email = new_email
                self.session.commit()
            return True
        except:
            self.session.rollback()
            return False

    def deleteCustomer(self, customer_id):
        try:
            customer = self.session.query(Customer).filter(Customer.ID == customer_id).first()
            if customer:
                self.session.delete(customer)
                self.session.commit()
            return True
        except:
            self.session.rollback()
            return False

    def closeConnection(self):
        self.session.close()
        self.engine.dispose()