import stripe
from db.model import Customer
import configparser

class Helper():        
    def getStripeID(stripeCustomer):
        id = str(stripeCustomer.get("id"))
        return id


class stripeService:

    def __init__(self):
        # read config file
        config = configparser.ConfigParser()
        config.read('config.ini')
        stripe.api_key = config.get('Keys', 'api_key')

    # Create a customer
    def createCustomer(self, email, name):
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
            )
            return Customer(ID=Helper.getStripeID(customer), name=customer.name, email=customer.email)
        except:
            return None
        
    # Get customer
    def getCustomer(self, customer_id):
        try:
            customer = stripe.Customer.retrieve(customer_id)
            return Customer(ID=customer.id, name=customer.name, email=customer.email)
        except stripe.error.StripeError as e:
            return None
        
    # Update customer
    def updateCustomer(self, stripe_id, new_email=None, new_name=None):
        try:
            stripe.Customer.modify(
                stripe_id,
                email=new_email,
                name=new_name,
            )
            return Customer(ID=stripe_id, name=new_name, email=new_email)        
        except:
            return None

    # Delete customer
    def deleteCustomer(self, stripe_id):
        try:
            stripe.Customer.delete(stripe_id)
            return True
        except:
            return False