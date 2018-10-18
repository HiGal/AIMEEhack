from flask import Flask,request,jsonify, render_template
import pusher

app = Flask(__name__)

pusher_client = pusher.Pusher(
  app_id='625201',
  key='706ab48dca940577335b',
  secret='60d12612ff0ece2809fb',
  cluster='eu',
  ssl=True
)

@app.route('/')
def index():
    return render_template('chat.html')


if __name__ == '__main__':
    app.run()
cd