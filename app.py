#who2ask 
import os
from views import *
from dbops import *
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler #for socket hosting

app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.event("app_home_opened")
def update_home_tab(client, event, logger):
  try:
    client.views_publish(
      user_id=event["user"],
      view=compose_home()
    )
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")

if __name__ == '__main__':
    print("Hello Darling")
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start() 