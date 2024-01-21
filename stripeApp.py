import json
import os
import stripe

from flask import Flask, jsonify, request

stripe.api_key = "<>"

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = "<>"

app = Flask(__name__)

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
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'customer.created':
        print('New customer created:', event['data']['object'])
    elif event['type'] == 'customer.updated':
        print('Customer updated:', event['data']['object'])
    elif event['type'] == 'customer.deleted':
        print('Customer deleted:', event['data']['object'])
    else:
        # Handle other events as needed
        print('Unhandled event type:', event['type'])

    return '', 200
