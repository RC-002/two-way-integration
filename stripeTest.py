import stripe

# Set your Stripe API key
stripe.api_key = '<>'

def create_stripe_customer(email, name=None):
    try:
        # Create a new customer
        customer = stripe.Customer.create(
            email=email,
            name=name,
        )

        # Print the newly created customer ID
        print(f"Customer created with ID: {customer.id}")

        return customer

    except stripe.error.StripeError as e:
        # Handle Stripe errors
        print(f"Stripe Error: {e}")
        return None

def retrieve_stripe_customer(customer_id):
    try:
        # Retrieve a customer by ID
        customer = stripe.Customer.retrieve(customer_id)

        # Print customer details
        print(f"Customer ID: {customer.id}, Email: {customer.email}, Name: {customer.name}")

        return customer

    except stripe.error.StripeError as e:
        # Handle Stripe errors
        print(f"Stripe Error: {e}")
        return None

def update_stripe_customer(customer_id, new_email=None, new_name=None):
    try:
        # Update a customer by ID
        customer = stripe.Customer.modify(
            customer_id,
            email=new_email,
            name=new_name,
        )

        # Print updated customer details
        print(f"Customer updated - ID: {customer.id}, Email: {customer.email}, Name: {customer.name}")

        return customer

    except stripe.error.StripeError as e:
        # Handle Stripe errors
        print(f"Stripe Error: {e}")
        return None

def delete_stripe_customer(customer_id):
    try:
        # Delete a customer by ID
        deleted_customer = stripe.Customer.delete(customer_id)

        # Print the ID of the deleted customer
        print(f"Customer deleted with ID: {deleted_customer.id}")

        return deleted_customer

    except stripe.error.StripeError as e:
        # Handle Stripe errors
        print(f"Stripe Error: {e}")
        return None

# Example usage
email_to_create = "example2@example.com"
customer_name = "John Doe"

# Create a new customer
new_customer = create_stripe_customer(email_to_create, name=customer_name)

# Retrieve the created customer
if new_customer:
    retrieved_customer = retrieve_stripe_customer(new_customer.id)

    # Update the retrieved customer
    if retrieved_customer:
        updated_customer = update_stripe_customer(retrieved_customer.id, new_email="updated@example.com", new_name="Updated Name")

        # Delete the updated customer
        if updated_customer:
            deleted_customer = delete_stripe_customer(updated_customer.id)