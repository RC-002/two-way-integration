from customers.model import Customer
from customers.repository import dbConnectivity

class customerService():
    def __init__(self):
        self.engine, self.session = dbConnectivity.create_engine_and_session()

    def createCustomer(self, id, name, email):
        try:
            new_customer = Customer(ID=id, name=name, email=email)
            self.session.add(new_customer)
            self.session.commit()
            return True
        except:
            return False

    def getCustomer(self, customer_id):
        try:
            return self.session.query(Customer).filter(Customer.ID == customer_id).first()
        except:
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
            return False

    def deleteCustomer(self, customer_id):
        try:
            customer = self.session.query(Customer).filter(Customer.ID == customer_id).first()
            if customer:
                self.session.delete(customer)
                self.session.commit()
            return True
        except:
            return False

    def closeConnection(self):
        self.session.close()
        self.engine.dispose()