from flask import Flask,request,jsonify, render_template
import pusher
import os

app = Flask(__name__)

pusher_client = pusher.Pusher(
  app_id=os.getenv('PUSHER_APP_ID'),
  key=os.getenv('PUSHER_KEY'),
  secret=os.getenv('PUSHER_SECRET'),
  cluster=os.getenv('PUSHER_CLUSTER'),
  ssl=True
)

@app.route('/')
def index():
    return render_template('chat.html')


if __name__ == '__main__':
    app.run()
