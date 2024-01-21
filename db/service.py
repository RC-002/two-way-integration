from db.model import Customer, ID_Mapping
from db.repository import dbConnectivity
import uuid

class Helper():    
    def generateUUID(size=32):
        random_uuid = uuid.uuid4()
        hex_uuid = format(random_uuid.int, 'x')[:size]
        return str(hex_uuid)

class dbService():
    def __init__(self):
        self.engine, self.session = dbConnectivity.create_engine_and_session()
    
    # Customer Methods
    def createCustomer(self, name, email):
        try:
            id = Helper.generateUUID(32)
            new_customer = Customer(ID=id, name=name, email=email)
            self.session.add(new_customer)
            self.session.commit()
            return new_customer
        except:
            self.session.rollback()
            return None

    def getCustomer(self, customer_id):
        try:
            return self.session.query(Customer).filter(Customer.ID == customer_id).first()
        except:
            self.session.rollback()
            return None

    def getAllCustomers(self):
        try:
            return self.session.query(Customer).all()
        except:
            return None

    def updateCustomer(self, customer_id, new_name, new_email):
        try:
            customer = self.session.query(Customer).filter(Customer.ID == customer_id).first()
            if customer:
                customer.name = new_name
                customer.email = new_email
                self.session.commit()
            return customer
        except:
            self.session.rollback()
            return None

    def deleteCustomer(self, customer_id):
        try:
            customer = self.session.query(Customer).filter(Customer.ID == customer_id).first()
            if customer:
                self.session.delete(customer)
                self.session.commit()
                return True
            return False
        except:
            self.session.rollback()
            return False

    # ID_Mapping Methods
    def addCustomerMapping(self, email, stripe_id):
        try:
            customerId = self.session.query(Customer).filter(Customer.email == email).first().ID
            new_mapping = ID_Mapping(customer_id=customerId, stripe_id=stripe_id)
            self.session.add(new_mapping)
            self.session.commit()
            return True
        except:
            self.session.rollback()
            return False
    
    def findStripeID(self, customer_id):
        try:
            mapping = self.session.query(ID_Mapping).filter(ID_Mapping.customer_id == customer_id).first()
            if mapping:
                return mapping.stripe_id
            return None
        except:
            self.session.rollback()
            return None
    
    def findCustomerID(self, stripe_id):
        try:
            mapping = self.session.query(ID_Mapping).filter(ID_Mapping.stripe_id == stripe_id).first()
            if mapping:
                return mapping.customer_id
            return None
        except:
            self.session.rollback()
            return None
    
    def deleteIDMapping(self, customer_id):
        try:
            mapping = self.session.query(ID_Mapping).filter(ID_Mapping.customer_id == customer_id).first()
            if mapping:
                self.session.delete(mapping)
                self.session.commit()                
                return True
            return False
        except:
            self.session.rollback()
            return False
    
    def deleteIDMappingFromIntegrationID(self, integrationID):
        try:
            mapping = self.session.query(ID_Mapping).filter(ID_Mapping.stripe_id == integrationID).first()
            if mapping:
                self.session.delete(mapping)
                self.session.commit()                
                return True
            return False
        except:
            self.session.rollback()
            return False
    
    # Kafka Event Methods
    def createCustomerFromEvent(self, integrationID, name, email):
        customer = self.session.query(Customer).filter(Customer.email == email).first()
        print(customer)
        if customer is None:        
            customer = self.createCustomer(name, email)
            print("Customer created:", customer)
        mapping = self.addCustomerMapping(email, integrationID)
        print("Mapping created:", mapping)
        return customer

    def updateCustomerFromEvent(self, integrationID, new_name=None, new_email=None):
        customerId = self.findCustomerID(integrationID)
        if customerId is not None:
            return self.updateCustomer(customerId, new_name, new_email)
        return None
    
    def deleteCustomerFromEvent(self, integrationID):    
        customerId = self.findCustomerID(integrationID)
        if self.deleteIDMappingFromIntegrationID(integrationID): 
            return self.deleteCustomer(customerId)
        return False

    # Close connection
    def closeConnection(self):
        self.session.close()
        self.engine.dispose()