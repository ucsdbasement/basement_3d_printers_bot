import requests
import random

help_command = [
    {
        "type": "header",
        "color": "#d1d2d3",
        "author_name": "The Basement 3D-Printers Bot",
        "author_icon": "http://placekitten.com/g/16/16",
        "title": "Hi there :wave:, I am a bot for the 3D-Printers at The Basement. I can help monitor your prints while you are away.",
    },
    {
        "mrkdwn_in": ["text"],
        "color": "#ff4500",
        "title": ":exclamation:Reach out to me with these available commands. Please give me a few seconds for camera related commands. Previous requested camera footages will automatically be deleted to optimize storage space.:exclamation:",
        "fields": 
        [
            {"value": "-`/prusa-camera-help`: Command guide"},
            {"value": "-`/prusa1-camera`: Display camera footage for Prusa 3D-Printer 1"},
            {"value": "-`/prusa2-camera`: Display camera footage for Prusa 3D-Printer 2"},
            {"value": "-`/prusa3-camera`: Display camera footage for Prusa 3D-Printer 3"},
            {"value": "-`/random-cat`: Receive a random cat picture"},
        ],
        "footer": "Report to @Kendrick Nguyen for any bugs/issues."
    }
]

failed_command = [
    {
        "type": "header",
        "color": "#d1d2d3",
        "author_name": "The Basement 3D-Printers Bot",
        "author_icon": "http://placekitten.com/g/16/16",
        "title": "Sorry, camera request failed. Please try again or contact our technician for help :face_with_thermometer:.",
    }
]

def camera_command(prusa_id):
    command = f'/prusa{prusa_id}-camera'
    return f'> :warning: Prusa 3D-Printer {prusa_id} Camera Footage via `{command}` command. Previous requested camera footages will automatically be deleted to optimize storage space.:warning:'

def cat_command():
    request_url = 'https://cataas.com/c?json=true&width=200&height=200'
    response_body = requests.get(request_url).json()
    url = 'https://cataas.com' + response_body['url']

    puns = ['How do you like me meow?',
            'Now wait a meowment...',
            'Meow are you doing?',
            "Meow you're talking!",
            'Here and meow...',
            'Press paws and live in the meow.',
            'Any minute meow...',
            "You're my best fur-end.",
            "It's meow or never.",
            "Stop stressing meowt!",
            "Enjoy every meowment."]

    cat_command = [
        {
            "type": "header",
            "color": "#d1d2d3",
            "author_name": "The Basement 3D-Printers Bot",
            "author_icon": "http://placekitten.com/g/16/16",
            "title": random.choice(puns),
            "image_url": url
        }
    ]

    return cat_command