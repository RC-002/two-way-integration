import stripe
from threading import Thread
from flask import Flask, jsonify, request
from stripeService import stripeService
from KafkaConsumer import syncConsumer

stripe.api_key = 'sk_test_51OaYX4SJjgpVMnDMdKLpH5QXIdF0GHPQa0XrfTydE9DxU5kVQSxrpaGPPnT5gqfQuZAWi82m2TsGQ1h2PQ5XJW6e00G2bEX1X6'

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = 'whsec_yniVCAQpNBhEmW6gJTwpeAMT84KECbzl'

app = Flask(__name__)
service = stripeService()
consumer = syncConsumer()

# Class to help handle local db operations for stripe events
class Helper:
    def updateCustomer(customer):
        name = customer['name']
        email = customer['email']
        stripe_id = customer['id']      
        return service.updateCustomer(stripe_id, name, email)
    
    def createCustomer(customer):
        name = customer['name']
        email = customer['email']
        stripe_id = customer['id']  
        return service.createCustomer(stripe_id, name, email)
    
    def deleteCustomer(customer):
        stripe_id = customer['id']
        return service.deleteCustomer(stripe_id)
    
        
@app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return jsonify(success=False), 500
    except stripe.error.SignatureVerificationError as e:
        return jsonify(success=False), 500
    
    print(event)
    # # Handle the event
    # if event['type'] == 'customer.created':
    #     print("New Customer Created")
    #     print(Helper.createCustomer(event['data']['object']))
    # elif event['type'] == 'customer.updated':
    #     print("Customer Updated")
    #     print(Helper.updateCustomer(event['data']['object']))
    # elif event['type'] == 'customer.deleted':
    #     print("Customer Deleted")
    # else:
    #     print('Unhandled event type:', event['type'])

    return jsonify(success=True)


# Start Kafka listener in the background when the Flask app starts
def start_background_worker():
    with app.app_context():
        consumer.sync()

if __name__ == '__main__':
    t = Thread(target=start_background_worker)
    t.start()
    app.run(port=5000)