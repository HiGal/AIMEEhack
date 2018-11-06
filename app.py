import json

import requests
from flask import Flask, request, jsonify, render_template
import dialogflow
import pusher
import os

app = Flask(__name__)

pusher_client = pusher.Pusher(
    app_id='625201',
    key='706ab48dca940577335b',
    secret='60d12612ff0ece2809fb',
    cluster=os.getenv('PUSHER_CLUSTER'),
    ssl=True
)


@app.route('/')
def index():
    return render_template('chat.html')


@app.route('/get_movie_detail', methods=['POST'])
def get_movie_detail():
    data = request.get_json(silent=True)

    movie = data['queryResult']['parameters']['movie']
    api_key = os.getenv('OMDB_API_KEY')

    # getting list of search result from external database
    movie_detail = requests.get('https://api.themoviedb.org/3/search/movie?api_key={0}&query={1}&language=ru'.format(api_key,movie)).content
    movie_detail = json.loads(movie_detail)

    # getting more information about film
    movie_detail = requests.get('https://api.themoviedb.org/3/movie/{0}?api_key={1}&language=ru'.format(movie_detail['results'][0]['id'],api_key)).content
    movie_detail = json.loads(movie_detail)

    # getting link on youtube for the trailer
    video = requests.get("https://api.themoviedb.org/3/movie/{0}/videos?api_key={1}".format(movie_detail['id'],api_key)).content
    video = json.loads(video)

    # creating response and creating answer in json
    response = ("{{\"Type\": \"film\",\"Title\" : \" {0} \" ,\"Released\" : \" {1} \","
                "\"Video\":\"https://www.youtube.com/embed/{2}\","
                "\"Poster\": \"https://image.tmdb.org/t/p/w500/{3}\","
                "\"Tagline\":\"{4}\","
                "\"Score\":\"{5}\"}}")\
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


def detect_intent_texts(project_id, session_id, text, language_code):
        """
        Finding keywords (intents) in query string
        :return fullfillment text according to found intent text
        """
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, session_id)

        if text:
            text_input = dialogflow.types.TextInput(
                text=text, language_code=language_code)
            query_input = dialogflow.types.QueryInput(text=text_input)
            response = session_client.detect_intent(
                session=session, query_input=query_input)

            return response.query_result.fulfillment_text


@app.route('/send_message', methods=['POST'])
def send_message():
        """
        trigger front end using pusher api
        :return: response text as JSON
        """
        message = request.form['message']
        project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
        fulfillment_text = detect_intent_texts(project_id, "unique", message, 'ru')
        response_text = {"message":  fulfillment_text}
       # socketId = request.form['socketId']
        print(response_text)
        pusher_client.trigger('AIMEE', 'new_message',
                              {'human_message': message, 'bot_message': fulfillment_text})

        return jsonify(response_text)


if __name__ == '__main__':
    app.run()
