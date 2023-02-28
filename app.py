#who2ask 
import os
from views import *
from dbops import *
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler #for socket hosting

app = App(token=os.environ["SLACK_BOT_TOKEN"])

if __name__ == '__main__':
    print("Hello Darling")
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start() 