from flask import jsonify


def get_location_detail():
    # creating response and creating answer in json
    response = "{{\"Type\": \"location\"}}"

    reply = {

        'fulfillmentText': response
    }

    return jsonify(reply)
