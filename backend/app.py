from flask import Flask
import datetime
from transcript import youtube_transcript
from flask import request
from flask_cors import CORS
#from youtube_transcript_api import YouTubeTranscriptApi

# define a variable to hold you app
app = Flask(__name__)
CORS(app)
# define your resource endpoints
@app.route('/', methods=['GET'])
def index_page():
    return "Hello world"

@app.route('/transcript', methods=['GET'])
def yt_transcript():
    return youtube_transcript(request)
  

# server the app when this file is run
if __name__ == '__main__':
    app.run(port=5000 , debug=True)