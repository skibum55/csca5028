"""modeule for slack data collection."""
import logging
import os

# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import db.db_api as db
from app.analyzer import sentiment

# https://api.slack.com/messaging/retrieving

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
logger = logging.getLogger(__name__)

# the collect function
def slack_collect():
    """Function printing python version."""
    channel_name = "csca5028"
    channel_id = None
    try:
        # Call the conversations.list method using the WebClient
        for result in client.conversations_list():
            if channel_id is not None:
                break
            for channel in result["channels"]:
                # print(channel["name"])
                if channel["name"] == channel_name:
                    channel_id = channel["id"]
                    #Print result
                    print(f"Found conversation ID: {channel_id}")
                    break

    except SlackApiError as e:
        print(f"Error: {e}")

    # conversation_history = getconversations(channel_id)
    getmessages(channel_id)
    return {"hola mundo"}

def getmessages(channel_id):
    """function to get messages and insert into database"""
    oldest_ts = db.get_latest()
    # oldest_ts=1672531261
    print(oldest_ts)
    try:
        # Call the conversations.history method using the WebClient
        # The client passes the token you included in initialization
        result = client.conversations_history(
            channel=channel_id,
            inclusive=True,
            oldest=oldest_ts or 0,
            # latest=oldest_ts,
            # latest="1672531261",
            limit=100
        )
        for message in result["messages"]:
        # Print message text
            messagetype=message["type"]
            # messagesubtype=message.get("subtype") or ""
            mytext=message["text"]
            # mythread=message.get("thread_ts") or ""
            myts=message["ts"]
            mymessage=(messagetype,mytext,myts)
            db.insert(mymessage)
            # if (messagesubtype != "channel_join"):
            #     print(messagetype, mytext, mythread,myts)
            msg_sentiment = sentiment.sentiment_analyzer(mytext)
            # write to sentiment table with id & sentiment
            label = msg_sentiment.labels[0]
            labscore = label.score
            label_sentiment=label.value
            # if label_sentiment == "NEGATIVE":
            #     labscore = labscore * -1
            db.insert_sentiment(myts,label_sentiment,labscore)

    except SlackApiError as e:
        print(f"Error: {e}")
