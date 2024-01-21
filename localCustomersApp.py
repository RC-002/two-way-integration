from fastapi import FastAPI, HTTPException, status, Depends
from customers.service import dbService
from pydantic import BaseModel
from KafkaProducer import syncProducer
import re


class Customer(BaseModel):
    ID: str
    name: str
    email: str

class Helper():
    def isValidEmail(email):
        email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        match = email_pattern.match(email)
        return bool(match)
    

# App settings
app = FastAPI()
service = dbService()
syncProducer = syncProducer()

# Dependency to get the service instance
async def get_service():
    return service

# Dependency to get the producer instance
async def get_producer():
    return syncProducer


# Create Customer
@app.post("/customers/", status_code=status.HTTP_201_CREATED, response_model=Customer)
async def create_customer(name: str, email: str, service: dbService = Depends(get_service)):
    if not Helper.isValidEmail(email):
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid email address")
    
    customer = service.createCustomer(name, email)
    if customer is not None:
        syncProducer.writeToTopic("update", customer.ID, customer.name, customer.email)
        return customer
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create customer")

# Get Customer
@app.get("/customers/{customer_id}", response_model=Customer)
async def read_customer(customer_id: str, service: dbService = Depends(get_service)):
    customer = service.getCustomer(customer_id)
    if customer is not None:
        return customer
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

# Get All Customers
@app.get("/customers/", response_model=list[Customer])
async def read_customers(service: dbService = Depends(get_service)):
    customers = service.getAllCustomers()
    if customers is not None:
        return customers
    return []

# Update Customer
@app.put("/customers/{customer_id}", response_model=Customer)
async def update_customer(customer_id: str, new_name: str, new_email: str, service: dbService = Depends(get_service)):
    customer = service.updateCustomer(customer_id, new_name, new_email)
    if customer is not None:
        syncProducer.writeToTopic("delete", customer.ID, customer.name, customer.email)
        return customer
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update customer")

# Delete Customer
@app.delete("/customers/{customer_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_customer(customer_id: str, service: dbService = Depends(get_service)):
    customer = service.deleteCustomer(customer_id)
    if customer:
        syncProducer.writeToTopic("customer", ID = customer_id, name = None, email = None)
        return {"detail" :"Customer deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")



