#who2ask 
import os
from views import *
from dbops import *
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler #for socket hosting

app = App(token=os.environ["SLACK_BOT_TOKEN"])
homeviews = {}
# "/who [topic]" will return a list of people with relevant knowledge of the topic.
# "/what [name]" will return a list of topics the named person has volunteered. 

@app.event("app_home_opened")
def app_home_opened(client, event, logger):
  user_id = event["user"]
  user_name = ""
  user_image = ""
  
  # Get user info (eventually we'll cache this)
  try:
    response = client.users_profile_get(user=user_id)
    user_name = response["profile"]["real_name_normalized"]
    user_image = response["profile"]["image_72"]
  except Exception as e:
    logger.error("Error: {}".format(e))
  
  # Compose the home tab view
  # check if user had open search results
  if user_id not in homeviews:
    homeviews[user_id] = compose_home(user_name, user_image)
  
  try:
    app.client.views_publish(
      user_id=user_id,
      view=homeviews[user_id]
    )
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")

@app.action("input_search")
def handle_search(ack, body, logger):
    ack()
    query = body['actions'][0]['value']
    user_id = body['user']['id']
    
    # update homeviews[user_id] with search results so that if user clicks away, they can return to their search results
    homeviews[user_id] = compose_search_results(query)
    try:
      app.client.views_publish(
        user_id=user_id,
        view=homeviews[user_id]
      )
    except Exception as e:
      logger.error(f"Error publishing home tab: {e}")

if __name__ == '__main__':
    print("Hello Darling")
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start() 