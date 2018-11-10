import requests
from bs4 import BeautifulSoup
import uuid
import os

UNDEFINED_STRING='undefined'

def speech_to_text(filename=None, bytes=None):
    request_id = uuid.uuid4().hex
    key = os.getenv('YANDEX_API_KEY')
    if(key):
        url = 'https://asr.yandex.net/asr_xml?key=' + key + '&uuid=' + request_id + '&topic=queries&lang=ru-RU'
    else:
        return UNDEFINED_STRING

    # файл распознования
    headers = {"Content-Type": 'audio/ogg;codecs=opus'}

    if filename:
        data = open(filename, 'rb')
    elif bytes:
        data = bytes
    else:
        return UNDEFINED_STRING

    response = requests.post(url, headers=headers, data=data)

    soup = BeautifulSoup(response.text, 'html.parser')

    # soup.variant
    result = UNDEFINED_STRING
    answers = soup.findAll('variant')
    if (len(answers) > 0):
        result = answers[0].text
    return result
