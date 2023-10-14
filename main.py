# Slack api
import slack
import slack_blocks

# Env variables
import os
from dotenv import load_dotenv

# Camera processing
from threading import Thread
from frame import get_frames

# Database
import db

from flask import Flask, request, Response

# Load env variables secrets
load_dotenv()

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SIGNING_SECRET = os.environ.get('SIGNING_SECRET')

# Flask application
app = Flask(__name__)

client = slack.WebClient(token=SLACK_BOT_TOKEN)

def send_camera_feed(user_id, channel_id, prusa_id):
    try:
        file_id = db.delete_file_cache(user_id)
        if file_id:
            client.files_delete(file=file_id)

        #get_frames(prusa_id=prusa_id, num_frames=30)

        file_path = f'frames/prusa_{prusa_id}/image.gif'
        response = client.files_upload(channels=channel_id, initial_comment=slack_blocks.camera_command(prusa_id), file=file_path)
        file_id = response['file']['id']

        db.add_file_cache(user_id, file_id)

    except:
        client.chat_postMessage(channel=channel_id, attachments=slack_blocks.failed_command)

    db.record_activity(user_id, f'prusa_{prusa_id}')

@app.route('/prusa-camera-help', methods=['POST'])
def printer_help():
    data = request.form
    user_id = data.get('user_id')

    # Open a direct message with user
    response = client.conversations_open(users=user_id)
    channel_id = response['channel']['id']

    blocks = slack_blocks.help_command
    response = client.chat_postMessage(channel=channel_id, attachments=blocks)

    db.record_activity(user_id, 'help')

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

    response = client.chat_postMessage(channel=channel_id, attachments=slack_blocks.cat_command())

    return Response(), 200

if __name__ == '__main__':
    app.run(debug=True, port=3000)