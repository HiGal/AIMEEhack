from flask import request, jsonify, Blueprint
import requests
import json


def get_ticket_list(data):
    origin = data['origin']
    destination = data['destination']

    ticket_details = requests.get(
        'http://api.travelpayouts.com/v2/prices/latest?currency=rub&period_type=month&page=1&limit=5&'
        'show_to_affiliates=true&sorting=price&token=7bfcdb75c29756a4ce37cd93bdbe6801&origin={0}&destination={1}'.format(
            origin, destination)).content

    ticket_details = json.loads(ticket_details)

    response = ("{{\"Type\": \"ticket\",\"Origin\" : \" {0} \" ,\"Destination\" : \" {1} \","
                ) \
        .format(ticket_details['origin'],
                ticket_details['destination'])

    reply = {

        'fulfillmentText': response
    }

    return jsonify(reply)
