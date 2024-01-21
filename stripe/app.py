import stripe
from threading import Thread
from flask import Flask, jsonify, request
from stripeService import stripeService
from KafkaConsumer import syncConsumer
from KafkaProducer import syncProducer
from Helper import Helper

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = "<>"

app = Flask(__name__)
service = stripeService()
consumer = syncConsumer()
producer = syncProducer()
helper = Helper()

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
    
    # Handle the event
    if event['type'] == 'customer.created':
        print("New Customer Created")
        data = helper.getDataOnCreateOrUpdate(event['data']['object'])
        producer.writeToTopic("create", data)

    elif event['type'] == 'customer.updated':
        print("Customer Updated")
        data = helper.getDataOnCreateOrUpdate(event['data']['object'])
        producer.writeToTopic("update", data)

    elif event['type'] == 'customer.deleted':
        print("Customer Deleted")
        data = helper.getDataOnDelete(event['data']['object'])
        producer.writeToTopic("delete", data)

    else:
        print('Unhandled event type:', event['type'])

    return jsonify(success=True)


# Start Kafka listener in the background when the Flask app starts
def start_background_worker():
    with app.app_context():
        consumer.sync()

if __name__ == '__main__':
    t = Thread(target=start_background_worker)
    t.start()
    app.run(port=5000)