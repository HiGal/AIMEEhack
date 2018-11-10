from flask import request, jsonify, Blueprint
import requests
import json
import os


def get_ticket_list(data):
    origin = data['query_result']['parameters']['origin']
    destination = data['query_result']['parameters']['destination']
    api_key = os.getenv('TICKET_API')

    ticket_details = requests.get(
        'http://api.travelpayouts.com/v1/prices/cheap?origin={0}&destination={1}&'
        'token={2}'.format(origin, destination, api_key)).content

    ticket_details = json.loads(ticket_details)

    response = ("{{\"Type\": \"ticket\",\"Origin\" : \" {0} \" ,\"Destination\" : \" {1} \", \"Price\" : \" {2} \", "
                "\"Departure\" : \" {3} \", \"Arrive\" : \" {4} \""
                ) \
        .format(origin,
                destination,
                ticket_details['price'],
                ticket_details['departure_at'],
                ticket_details['return_at']
                )

    reply = {

        'fulfillmentText': response
    }

    return jsonify(reply)
