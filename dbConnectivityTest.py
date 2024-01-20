from dbConnectivity import *

# Create engine and session
engine, session = create_engine_and_session()

# Create a new customer
print(createCustomer(session, id="1", name="John Doe", email="john.doe@example.com"))

# Read a customer
print(getCustomer(session, customer_id="1"))

# Update a customer
print(updateCustomer(session, customer_id="1", new_name="Updated Name", new_email="updated.email@example.com"))

# Delete a customer
print(deleteCustomer(session, customer_id="1"))

# Close session and dispose of the engine
closeConnection(engine, session)
