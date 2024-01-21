from db.service import dbService

service = dbService()

# Create a new customer
customer = service.createCustomer(name="John Doe", email="john.doe@example.com")
print("Created: " + str(customer))

id = customer.ID

# Read a customer
print("Get Customer" + str(service.getCustomer(id)))

# Update a customer
print("Update Customer: " + str(service.updateCustomer(id, new_name="Updated Name", new_email="updated.email@example.com")))

# Delete a customer
print(service.deleteCustomer(id))

# Close session and dispose of the engine
service.closeConnection()

