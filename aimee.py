import requests
from flask import jsonify
import json
import random

instance = 'http://137.117.181.156:4560/'

chat_id = 1
message_id = 1
dialogue_id = 1


def aimee_answer(data):
    message_id= random.randint(1,100)
    question = data['queryResult']['queryText']
    response = requests.get((instance + "/v2/ai/answer/?key={}&chat_id={}&message_id={}&dialogue_id={}") \
                          .format(question, chat_id, message_id, dialogue_id)).content
    response = json.loads(response)
    print(response['hypothesis'][0]['answer'])
    reply = {
        'fulfillmentText': response['hypothesis'][0]['answer']
    }
    print(reply)
    return jsonify(reply)
