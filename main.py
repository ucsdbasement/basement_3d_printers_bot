# Slack api and event listener
import slack
from slack_blocks import help_command, camera_command, failed_command, cat_command

# Env variables
import os
from dotenv import load_dotenv

# Camera processing
from threading import Thread
from frame import get_frames

# Import writer class from csv module
from csv import writer

from flask import Flask, request, Response
from datetime import datetime

# Load env variables secrets
load_dotenv()

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SIGNING_SECRET = os.environ.get('SIGNING_SECRET')

# Flask application
app = Flask(__name__)

client = slack.WebClient(token=SLACK_BOT_TOKEN)

def send_camera_feed(user_id, channel_id, prusa_id):
    try:
        #get_frames(prusa_id=prusa_id, num_frames=30)
        client.files_upload(channels=channel_id, initial_comment=camera_command(prusa_id), file=f'frames/prusa_{prusa_id}/image.gif')

    except:
        client.chat_postMessage(channel=channel_id, attachments=failed_command)

    with open('log.csv', 'a') as f:
        writer_object = writer(f)
        writer_object.writerow([user_id, f'prusa_{prusa_id}', datetime.now()])

@app.route('/prusa-camera-help', methods=['POST'])
def printer_help():
    data = request.form
    user_id = data.get('user_id')

    # Open a direct message with user
    response = client.conversations_open(users=user_id)
    channel_id = response['channel']['id']

    blocks = help_command
    response = client.chat_postMessage(channel=channel_id, attachments=blocks)

    with open('log.csv', 'a') as f:
        writer_object = writer(f)
        writer_object.writerow([user_id, 'help', datetime.now()])

    return Response(), 200

@app.route('/prusa<prusa_id>-camera', methods=['POST'])
def prusa1_camera_feed(prusa_id):
    data = request.form
    user_id = data.get('user_id')

    # Open a direct message with user
    response = client.conversations_open(users=user_id)
    channel_id = response['channel']['id']

    thread_prusa1 = Thread(target=send_camera_feed, args=[user_id, channel_id, prusa_id])
    thread_prusa1.start()

    return Response(), 200

@app.route('/random-cat', methods=['POST'])
def random_cat():
    data = request.form
    user_id = data.get('user_id')

    # Open a direct message with user
    response = client.conversations_open(users=user_id)
    channel_id = response['channel']['id']

    response = client.chat_postMessage(channel=channel_id, attachments=cat_command())

    return Response(), 200

if __name__ == '__main__':
    app.run(debug=True, port=3000)