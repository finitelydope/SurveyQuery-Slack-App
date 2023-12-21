import logging
import gspread
import sys

# sys.path.append('/Apps') 
from ludo3 import insert_rows


from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.web import WebClient

SLACK_BOT_TOKEN = "xoxb-3576667958966-6349896653174-dteaD2y723lanfpZWtOUqim6"
SLACK_APP_TOKEN = "xapp-1-A06AJUPT0UC-6379305771776-681a1c4bb93ef1548e379824605cbd675149996857ed0a5dbf1f1e319e7bb78e"

credentials_file = "first-project-408605-1f1b495d074d.json"
spreadsheet_name = "Testing"

logging.basicConfig(level=logging.DEBUG)
logger=logging.getLogger()


# Install the Slack app and get xoxb- token in advance
app = App(token=SLACK_BOT_TOKEN)
@app.command("/get_survey")
def handle_mention(ack, body, client):
    ack()
    user_id = body["user_name"]
    try:
        # Call views_open with the built-in client
        response = client.views_open(
            trigger_id=body["trigger_id"],
                # View payload
                view={
                        "type": "modal",
                        "callback_id":"view_01",
                        "title": {
                            "type": "plain_text",
                            "text": "Survey Query",
                            "emoji": True
                        },
                        "submit": {
                            "type": "plain_text",
                            "text": "Submit",
                            "emoji": True
                        },
                        "close": {
                            "type": "plain_text",
                            "text": "Cancel",
                            "emoji": True
                        },
                        "blocks":
                        [
                            {
                                "type": "section",
                                "text": {
                                    "type": "plain_text",
                                    "text": f":wave: Hey <@{user_id}> !\n\nWe'd love to hear from you how we can make this place the best place you’ve ever worked.",
                                    "emoji": True
                                }
                            },
                            {
                                "type": "divider"
                            },
                            {
                                "type": "input",
                                "block_id" : "block_01",
                                "label": {
                                    "type": "plain_text",
                                    "text": "You enjoy working here at Pistachio & Co",
                                    "emoji": True
                                },
                                "element": {
                                    "type": "radio_buttons",
                                    "action_id":"ele_01",
                                    "options": [
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "Strongly agree",
                                                "emoji": True
                                            },
                                            "value": "1"
                                        },
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "Agree",
                                                "emoji": True
                                            },
                                            "value": "2"
                                        },
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "Neither agree nor disagree",
                                                "emoji": True
                                            },
                                            "value": "3"
                                        },
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "Disagree",
                                                "emoji": True
                                            },
                                            "value": "4"
                                        },
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "Strongly disagree",
                                                "emoji": True
                                            },
                                            "value": "5"
                                        }
                                    ]
                                }
                            },
                            {
                                "type": "input",
                                "block_id": "block_02",
                                "element": {
                                    "type": "radio_buttons",
                                    "action_id":"ele_02",
                                    "options": [
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "Excellent",
                                                "emoji": True
                                            },
                                            "value": "value-0"
                                        },
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "Good",
                                                "emoji": True
                                            },
                                            "value": "value-1"
                                        },
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "Needs Improvement",
                                                "emoji": True
                                            },
                                            "value": "value-2"
                                        }
                                    ]
                                    # "action_id": "radio_buttons-action"
                                },
                                "label": {
                                    "type": "plain_text",
                                    "text": "In your opinion, how well do team members collaborate with each other?",
                                    "emoji": True
                                }
                            },
                            {
                                "type": "input",
                                "block_id": "block_03",
                                "element":
                                {
                                    "type": "radio_buttons",
                                    "action_id": "ele_03",
                                    "options":[
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "Needs Improvement",
                                                "emoji": True
                                            },
                                            "value": "value-0"
                                        },
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "Excellent",
                                                "emoji": True
                                            },
                                            "value": "value-1"
                                        },
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "Good",
                                                "emoji": True
                                            },
                                            "value": "value-2"
                                        }
                                    ],
                                    #"action_id": "radio_buttons-action"
                                },
                                "label":
                                {
                                    "type": "plain_text",
                                    "text": "How would you rate our team's overall communication effectiveness on a scale of 1 to 5?",
                                    "emoji": True
                                }
                            }
                        ]
                    }    
        )
        logger.info(f"Modal opened successfully: {response}")
    except Exception as e:
        logger.error(f"Error opening modal: {e}")
    
@app.view("view_01")
def handle_submission(ack, body, client, view, logger):
    # Assume there's an input block with `input_c` as the block_id and `dreamy_input`
    ack()
    
    answer1 = view["state"]["values"]["block_01"]["ele_01"]["selected_option"]["text"]["text"]
    answer2 = view["state"]["values"]["block_02"]["ele_02"]["selected_option"]["text"]["text"]
    answer3 = view["state"]["values"]["block_03"]["ele_03"]["selected_option"]["text"]["text"]

    logger.info(answer1)
    logger.info(answer2)
    logger.info(answer3)
    data = [answer1, answer2, answer3]

    user = body["user"]["id"]
    msg = ""
    try:
        # Save to DB
        insert_rows(data)
        msg = f"Your submission of Survey was successful"
    except Exception as e:
        # Handle error
        msg = "There was an error with your submission"
 
    # Message the user
    try:
        client.chat_postMessage(channel=user, text=msg)
    except e:
        logger.exception(f"Failed to post a message {e}")



if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()

