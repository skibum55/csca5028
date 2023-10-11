import logging
import os

# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import db.dbAPI as dbAPI
import app.analyzer.sentiment as sentiment

# https://api.slack.com/messaging/retrieving

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
logger = logging.getLogger(__name__)
channel_name = "csca5028"
conversation_id = None

# TODO - create db and table on initialization in  main function, not here
db_filename = os.environ.get("SQLITE_DB")
dbAPI.create(db_filename) 

try:
    # Call the conversations.list method using the WebClient
    for result in client.conversations_list():
        if conversation_id is not None:
            break
        for channel in result["channels"]:
            # print(channel["name"])
            if channel["name"] == channel_name:
                conversation_id = channel["id"]
                #Print result
                print(f"Found conversation ID: {conversation_id}")
                break

except SlackApiError as e:
    print(f"Error: {e}")
    

# Store conversation history
conversation_history = []
# ID of the channel you want to send the message to
channel_id = "C05HXAFL41X"

try:
    # Call the conversations.history method using the WebClient
    # conversations.history returns the first 100 messages by default
    # These results are paginated, see: https://api.slack.com/methods/conversations.history$pagination
    result = client.conversations_history(channel=channel_id)
    # print(result)
    conversation_history = result["messages"]
    # print(conversation_history)

    # Print results
    logger.info("{} messages found in {}".format(len(conversation_history), channel_id))

except SlackApiError as e:
    logger.error("Error creating conversation: {}".format(e))

# conversation_id = "C01JASD6802"

try:
    # Call the conversations.history method using the WebClient
    # The client passes the token you included in initialization    
    result = client.conversations_history(
        channel=conversation_id,
        inclusive=True,
        oldest="1610144875.000600",
        # latest="1686118400",
        limit=100
    )  
    for message in result["messages"]:
    # Print message text
        messagetype=message["type"]
        messagesubtype=message.get("subtype") or ""
        mytext=message["text"]
        mythread=message.get("thread_ts") or ""
        myts=message["ts"]
        mymessage=(messagetype,mytext,myts)
        dbAPI.insert(mymessage)
        # if (messagesubtype != "channel_join"):
        #     print(messagetype, mytext, mythread,myts)
        msgSentiment = sentiment.sentimentAnalyzer(mytext)
        # write to sentiment table with id & sentiment
        dbAPI.insertSentiment(myts,msgSentiment)

except SlackApiError as e:
    print(f"Error: {e}")

def myfunction():
    return {"hola mundo"}