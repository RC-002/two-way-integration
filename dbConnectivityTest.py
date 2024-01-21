from db.service import dbService

service = dbService()

# Create a new customer
print(service.createCustomer(id="1", name="John Doe", email="john.doe@example.com"))

# Read a customer
print(service.getCustomer(customer_id="1"))

# Update a customer
print(service.updateCustomer(customer_id="1", new_name="Updated Name", new_email="updated.email@example.com"))

# Delete a customer
print(service.deleteCustomer(customer_id="1"))

# Close session and dispose of the engine
service.closeConnection()

