from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, '/jukebox')

def get_headlines():
    return 'You gay lol'

@app.route('/')
def homepage():
    return 'hi there, how ya doin?'

@ask.launch
def start_skill():
    welcome_message = 'Hello there, would you like the news?'
    return question(welcome_message)

@ask.intent('YesIntent')
def share_headlines():
    headlines = get_headlines()
    headline_msg = 'The current world news headlines are... {}'.format(headlines)
    return statement(headline_msg)

ask.intent("NoIntent")
def no_intent():
    bye_text = 'Cya later scrublord... bye'
    return bye_text

if __name__ == '__main__':
    app.run(debug=True)
