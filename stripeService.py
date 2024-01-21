import stripe
from customers.model import Customer

class Helper():        
    def getStripeID(stripeCustomer):
        id = str(stripeCustomer.get("id"))
        return id


class stripeService:
    stripe.api_key = "<>"

    # Created a customer locally, now create a customer in Stripe
    def createCustomer(self, email, name):
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
            )
            return Customer(ID=Helper.getStripeID(customer), name=customer.name, email=customer.email)
        except:
            return None
    # Get all customers from Stripe
    def getCustomer(self, customer_id):
        try:
            customer = stripe.Customer.retrieve(customer_id)
            return Customer(ID=customer.id, name=customer.name, email=customer.email)
        except stripe.error.StripeError as e:
            return None
        

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

    # Delete customer locally, then delete customer in Stripe 
    def deleteCustomer(self, stripe_id):
        try:
            stripe.Customer.delete(stripe_id)
            return True
        except:
            return False