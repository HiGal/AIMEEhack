from flask import request, jsonify, Blueprint
import requests
import json
import os


def get_ticket_list(data):
    o_city = data['queryResult']['parameters']['geo-city']
    d_city = data['queryResult']['parameters']['geo-city1']
    api_key = os.getenv('TICKET_API')

    iata_details = requests.get('https://www.travelpayouts.com/widgets_suggest_params?q=%20{0}%20{1}'.
                                format(o_city, d_city)).content
    iata_details = json.loads(iata_details)

    try:

        origin = iata_details['origin']['iata']
        destination = iata_details['destination']['iata']
        ticket_details = requests.get(
            'http://api.travelpayouts.com/v1/prices/cheap?origin={0}&destination={1}&'
            'token={2}'.format(origin, destination, api_key)).content

        ticket_details = json.loads(ticket_details)
        print(ticket_details)
        insurance = calculate_ensurance(ticket_details)

        ticket = list(ticket_details['data'][destination].keys())[0]

        response = ("{{\"Type\": \"ticket\", \"Origin\": \"{0}\", \"Destination\": \"{1}\", \"Price\": \"{2}"
                    "\", \"Departure\": \"{3}\", \"Insurance\": \"{4}\"}}"
                    ).format(o_city,
                             d_city,
                             ticket_details['data'][destination][ticket]['price'],
                             ticket_details['data'][destination][ticket]['departure_at'],
                             insurance)
    except(KeyError):
        response = "Извините, но таких билетов нет."
    reply = {

        'fulfillmentText': response
    }

    return jsonify(reply)


def calculate_ensurance(ticket_details):
    return "Вы можете застраховать себя от несчастных случаев, потери багажа и задержки рейса"
