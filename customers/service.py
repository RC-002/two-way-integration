from customers.model import Customer, ID_Mapping
from customers.repository import dbConnectivity
import stripe
import uuid

class Helper():    
    def generateUUID(size=32):
        random_uuid = uuid.uuid4()
        hex_uuid = format(random_uuid.int, 'x')[:size]
        return str(hex_uuid)
    
    def getStripeID(stripeCustomer):
        id = str(stripeCustomer.get("id"))
        return id

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

    def closeConnection(self):
        self.session.close()
        self.engine.dispose()


class stripeService:
    stripe.api_key = "<>"

    # Created a customer locally, now create a customer in Stripe
    def createCustomer(self, email, name):
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
            )
            stripeId = Helper.getStripeID(customer)
            dbService().addCustomerMapping(email, stripeId)
            return Customer(ID=customer.id, name=customer.name, email=customer.email)
        except:
            return None

    # Created a customer in Stripe, now create a customer locally
    def createCustomerLocally(self, stripe_id, email, name):
        try:
            localCustomer = dbService().createCustomer(name, email)
            if localCustomer is not None:
                dbService().addCustomerMapping(email, stripe_id)
                print("THis is done as well")
                return localCustomer
            return None            
        except:
            return None

    # Get all customers from Stripe
    def getCustomer(self, customer_id):
        try:
            customer = stripe.Customer.retrieve(customer_id)
            return Customer(ID=customer.id, name=customer.name, email=customer.email)
        except stripe.error.StripeError as e:
            return None
        
    # Update customer locally, then update customer in Stripe
    def updateCustomer(self, customer_id, new_email=None, new_name=None):
        try:
            stripe.Customer.modify(
                customer_id,
                email=new_email,
                name=new_name,
            )
            return Customer(ID=customer_id, name=new_name, email=new_email)        
        except:
            return None

    # Update customer in Stripe, then update customer locally
    def updateCustomerLocally(self, stripe_id, new_email=None, new_name=None):
        try:
            localID = dbService().findCustomerID(stripe_id)
            if localID is not None:
                localCustomer = dbService().updateCustomer(localID, new_name, new_email)
                if localCustomer is not None:
                    return localCustomer 
            return None   
        except:
            return None

    # Delete customer locally, then delete customer in Stripe 
    def deleteCustomer(self, stripe_id):
        try:
            customer_id = dbService().findCustomerID(stripe_id)
            stripe.Customer.delete(stripe_id)
            if(dbService().deleteIDMapping(customer_id)):
                return True
            return False
        except:
            return False
    
    # Delete customer in Stripe, then delete customer locally
    def deleteCustomerLocally(self, stripe_id):
        try:
            customer_id = dbService().findCustomerID(stripe_id)
            if customer_id is not None:
                if dbService().deleteIDMapping(customer_id):
                    if dbService().deleteCustomer(customer_id):
                        return True
            return False
        except:
            return False