import random
import string

from stripeService import stripeService

service = stripeService()

def generateRandomName():
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return name.capitalize()

def generateRandomEmail():
    email_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'example.com', 'domain.com']
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    domain = random.choice(email_domains)
    email = username + '@' + domain
    return email

# Example usage
email_to_create = generateRandomEmail()
customer_name = generateRandomName()


# Create a new customer
new_customer = service.createCustomer(email_to_create, customer_name)
print("New customer created")

# Retrieve the created customer
if new_customer is not None:
    retrieved_customer = service.getCustomer(new_customer.ID)
    print("New customer retrieved")

    # Update the retrieved customer
    if retrieved_customer is not None:
        updated_customer = service.updateCustomer(retrieved_customer.ID, new_email=generateRandomEmail(), new_name=generateRandomName())
        print("Customer updated")

        # Delete the updated customer
        if updated_customer is not None:
            deleted_customer = service.deleteCustomer(updated_customer.ID)        
            print("Deleted customer")
            exit(0)

print("Something went wrong :)")