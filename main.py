# Slack api and event listener
import slack

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
        client.files_upload(channels=channel_id, initial_comment=f':warning: Prusa 3D-Printer {prusa_id} Camera Feed', file=f'frames/prusa_{prusa_id}/image.gif')

    except:
        text = ':warning: Camera request failed. Please try again or contact The Basement technician for help.\n:exclamation: These are the available Basement 3D-Printers commands:\n> `/prusa-camera-help` Command guide\n> `/prusa1-camera` Display camera feed for Prusa 3D-Printer 1\n> `/prusa2-camera` Display camera feed for Prusa 3D-Printer 2\n> `/prusa3-camera` Display camera feed for Prusa 3D-Printer 3'
        client.chat_postMessage(channel=channel_id, text=text, mrkdwn=True)

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

    text = ':wave: Hi there, I am a bot for the 3D-Printers at The Basement. I can help you monitor your prints while you are away.\n:exclamation: These are the available Basement 3D-Printers commands:\n> `/prusa-camera-help` Command guide\n> `/prusa1-camera` Display camera feed for Prusa 3D-Printer 1\n> `/prusa2-camera` Display camera feed for Prusa 3D-Printer 2\n> `/prusa3-camera` Display camera feed for Prusa 3D-Printer 3'
    response = client.chat_postMessage(channel=channel_id, text=text, mrkdwn=True)

    with open('log.csv', 'a') as f:
        writer_object = writer(f)
        writer_object.writerow([user_id, 'help', datetime.now()])

    return Response(), 200

@app.route('/prusa<prusa_id>-camera', methods=['POST'])
def prusa1_camera_feed(prusa_id):
    data = request.form
    user_id = data.get('user_id')

    print(data)

    # Open a direct message with user
    response = client.conversations_open(users=user_id)
    channel_id = response['channel']['id']

    thread_prusa1 = Thread(target=send_camera_feed, args=[user_id, channel_id, prusa_id])
    thread_prusa1.start()

    return Response(), 200

if __name__ == '__main__':
    app.run(debug=True, port=3000)