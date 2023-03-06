#who2ask 
import os, asyncio, json
from views import *
from dbops import *
from admincheck import *
from slack_bolt.app.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])
homeviews = {}

@app.event("app_home_opened")
async def app_home_opened(client, event, logger):
  user_id = event["user"]
  user_name = ""
  user_image = ""
  
  # Get user info (eventually we'll cache this)
  try:
    response = await client.users_profile_get(user=user_id)
    user_name = response["profile"]["real_name_normalized"]
    user_image = response["profile"]["image_72"]
  except Exception as e:
    logger.error("Error: {}".format(e))
  
  # Compose the home tab view
  # check if user had open search results
  if user_id not in homeviews:
    is_admin = user_is_admin(user_id)
    homeviews[user_id] = compose_home(user_name, user_image, is_admin)
  
  try:
    await app.client.views_publish(
      user_id=user_id,
      view=homeviews[user_id]
    )
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")

@app.action("input_search")
async def handle_search(ack, body, logger):
    await ack()
    query = body['actions'][0]['value']
    user_id = body['user']['id']
    
    # update homeviews[user_id] with search results so that if user clicks away, they can return to their search results
    results = await search_db(query)
    homeviews[user_id] = compose_search_results(query, results, user_is_admin(user_id))
    try:
      await app.client.views_publish(
        user_id=user_id,
        view=homeviews[user_id]
      )
    except Exception as e:
      logger.error(f"Error publishing home tab: {e}")
    
    #await get_workspace_users(logger)
    #await search_db(query)

@app.action("button_view_profile")
async def handle_view_profile(ack, body, logger):
    await ack()
    user_id = body['user']['id']
    try:
      topics = await get_topics_by_user(user_id)
      await app.client.views_publish(
        user_id=user_id,
        view=compose_profile(topics)
      )
    except Exception as e:
      logger.error(f"Error publishing home tab: {e}")

async def get_workspace_users(logger):
  try:
    response = await app.client.users_list()
    #print(response)
    with open('users.json', 'w', encoding='utf-8') as f:
      json.dump(response['members'], f, ensure_ascii=False, indent=4)
    print("Wrote users to users.json")
  except Exception as e:
    logger.error(f"Error getting workspace users: {e}")

async def main():
  print("Hello Darling, i'm asynchronous!")
  handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
  await handler.start_async()

if __name__ == '__main__':
    asyncio.run(main())