from flask import jsonify
from datetime import datetime
import requests
import json
import os


def get_movie_detail(data):
    THREE_WEEKS = 1814400
    movie = data['queryResult']['parameters']['movie']
    api_key = os.getenv('OMDB_API_KEY')

    # getting list of search result from external database
    movie_detail = requests.get(
        'https://api.themoviedb.org/3/search/movie?api_key={0}&query={1}&language=ru'.format(api_key, movie)).content
    movie_detail = json.loads(movie_detail)

    # getting more information about film
    movie_detail = requests.get(
        'https://api.themoviedb.org/3/movie/{0}?api_key={1}&language=ru'.format(movie_detail['results'][0]['id'],
                                                                                api_key)).content
    movie_detail = json.loads(movie_detail)

    # getting link on youtube for the trailer
    video = requests.get(
        "https://api.themoviedb.org/3/movie/{0}/videos?api_key={1}".format(movie_detail['id'], api_key)).content
    video = json.loads(video)

    date = movie_detail['release_date']
    date = datetime.strptime(date, '%Y-%m-%d')
    today = datetime.today()

    inTheatres = 'false'

    if (today - date).total_seconds() < THREE_WEEKS:
        inTheatres = 'true'

    # creating response and creating answer in json
    response = ("{{\"Type\": \"film\",\"Title\" : \" {0} \" ,\"Released\" : \" {1} \","
                "\"Video\":\"https://www.youtube.com/embed/{2}\","
                "\"Poster\": \"https://image.tmdb.org/t/p/w500/{3}\","
                "\"Tagline\":\"{4}\","
                "\"Score\":\"{5}\","
                "\"Status\":\"{6}\"}}") \
        .format(movie_detail['title'],
                movie_detail['release_date'],
                video['results'][0]['key'],
                movie_detail['poster_path'],
                movie_detail['tagline'],
                movie_detail['vote_average'],
                inTheatres)

    reply = {

        'fulfillmentText': response
    }

    return jsonify(reply)
