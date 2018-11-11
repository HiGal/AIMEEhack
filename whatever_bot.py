from flask import jsonify


def get_location_detail():
    # creating response and creating answer in json
    response = "{\"Type\": \"location\"}"

    reply = {

        'fulfillmentText': response
    }

    return jsonify(reply)


def get_osago_detail():
    # creating response and creating answer in json
    response = "{\"Type\": \"osago\"}"

    reply = {

        'fulfillmentText': response
    }

    return jsonify(reply)


def get_auto_detail():
    # creating response and creating answer in json
    response = "{\"Type\": \"auto\"}"

    reply = {

        'fulfillmentText': response
    }

    return jsonify(reply)


def get_kasko_detail():
    # creating response and creating answer in json
    response = "{\"Type\": \"kasko\"}"

    reply = {

        'fulfillmentText': response
    }

    return jsonify(reply)
