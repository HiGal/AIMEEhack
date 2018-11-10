from flask import request, jsonify, Blueprint
import requests
import json
import os


def get_ticket_list(data):
    origin = data['queryResult']['parameters']['geo-city']
    destination = data['queryResult']['parameters']['geo-city1']
    api_key = os.getenv('TICKET_API')

    iata_details = requests.get('https://www.travelpayouts.com/widgets_suggest_params?q=%20{0}%20{1}'.
                                format(origin, destination)).content
    origin = iata_details['origin']['iata']
    destination = iata_details['destination']['iata']
    ticket_details = requests.get(
        'http://api.travelpayouts.com/v1/prices/cheap?origin={0}&destination={1}&'
        'token={2}'.format(origin, destination, api_key)).content

    ticket_details = json.loads(ticket_details)
    print(ticket_details)

    response = ("{{\"Type\": \"ticket\",\"Origin\" : \" {0} \" ,\"Destination\" : \" {1} \", \"Price\" : \" {2} \", "
                "\"Departure\" : \" {3} \", \"Arrive\" : \" {4} \""
                ) \
        .format(origin,
                destination,
                ticket_details['data'][destination.__str__()][0]['price'],
                ticket_details['data'][destination.__str__()][0]['departure_at'],
                ticket_details['data'][destination.__str__()][0]['return_at']
                )

    reply = {

        'fulfillmentText': response
    }

    return jsonify(reply)
