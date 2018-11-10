from flask import Flask, request, jsonify, render_template
from movie_bot import get_movie_detail
from ticket_bot import get_ticket_list
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


@app.route('/get_detail', methods=['POST'])
def get_detail():
    data = request.get_json(silent=True)
    print(data)
    typeof = list(data['queryResult']['parameters'].keys()).pop()
    json_obj = {}
    if typeof == 'movie':
        json_obj = get_movie_detail(data)
    if list(data['queryResult']['parameters'].keys()).__contains__('geo-city'):
        json_obj = get_ticket_list(data)
    return json_obj


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
    response_text = {"message": fulfillment_text}
    # socketId = request.form['socketId']
    print(response_text)
    pusher_client.trigger('AIMEE', 'new_message',
                          {'human_message': message, 'bot_message': fulfillment_text})

    return jsonify(response_text)


if __name__ == '__main__':
    app.run()
