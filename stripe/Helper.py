# Class to help handle local db operations for stripe events
import json

class Helper:
    def getDataOnCreateOrUpdate(self, customer):
        name = customer['name']
        email = customer['email']
        stripe_id = customer['id']
        return {
            "ID": stripe_id,
            "name": name,
            "email": email
        }
    
    def getDataOnDelete(self, customer):
        stripe_id = customer['id']
        return {
            "ID": stripe_id,
            "name": None,
            "email": None
        }