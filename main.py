from fastapi import FastAPI, HTTPException, status, Depends
from customers.service import customerService
from pydantic import BaseModel

class Customer(BaseModel):
    id; str
    name: str
    email: str
# App settings
app = FastAPI()
service = customerService()

# Dependency to get the service instance
async def get_service():
    return service

# Create Customer
@app.post("/customers/", response_model=Customer)
async def create_customer(name: str, email: str, service: customerService = Depends(get_service)):
    if service.createCustomer(name, email):
        return {"name": name, "email": email}
    else:
        raise HTTPException(status_code=500, detail="Failed to create customer")
