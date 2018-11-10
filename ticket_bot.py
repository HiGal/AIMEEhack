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

    response = ("{{\"Type\": \"film\",\"Title\" : \" {0} \" ,\"Released\" : \" {1} \","
                "\"Video\":\"https://www.youtube.com/embed/{2}\","
                "\"Poster\": \"https://image.tmdb.org/t/p/w500/{3}\","
                "\"Tagline\":\"{4}\","
                "\"Score\":\"{5}\"}}") \
        .format(movie_detail['title'],
                movie_detail['release_date'],
                video['results'][0]['key'],
                movie_detail['poster_path'],
                movie_detail['tagline'],
                movie_detail['vote_average'])

    reply = {

        'fulfillmentText': response
    }

    return jsonify(reply)
