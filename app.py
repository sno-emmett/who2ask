#who2ask 
import os, asyncio, json
from views import *
from dbops import *
from admincheck import *
from slack_bolt.app.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])
homeviews = {}
profileviews = {}

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
    
    if user_id not in profileviews:
      try:
        topics = await get_topics_by_user(user_id)
        profileviews[user_id] = compose_profile(topics)
      except Exception as e:
        logger.error(f"Error composing profile: {e}")
      
    try:
      await app.client.views_publish(
        user_id=user_id,
        view=profileviews[user_id]
      )
    except Exception as e:
      logger.error(f"Error publishing home tab: {e}")
      
@app.action("button_view_admin")
async def handle_view_admin(ack, body, logger):
    await ack()
    user_id = body['user']['id']

    if user_is_admin(user_id):
      try:
        await app.client.views_publish(
          user_id=user_id,
          view=compose_admin()
        )
      except Exception as e:
        logger.error(f"Error publishing home tab: {e}")
    else:
      print("User is not admin")

@app.action("button_return_to_search")
async def handle_return_to_search(ack, body, logger):
    await ack()
    user_id = body['user']['id']
    try:
      await app.client.views_publish(
        user_id=user_id,
        view=homeviews[user_id]
      )
    except Exception as e:
      logger.error(f"Error publishing home tab: {e}")

@app.action("button_edit_topic")
async def handle_edit_topic(ack, body, logger):
  await ack()
  topic_id = body['actions'][0]['value']
  
  try:
    topic = await get_topic_by_id(topic_id)
    await app.client.views_open(
        trigger_id=body["trigger_id"],
        view= compose_edit_modal(topic[0])
    )
  except Exception as e:
      logger.error(f"Error publishing home tab: {e}")
      
@app.action("button_add_topic")
async def handle_add_topic(ack, body, logger):
  await ack()
  try:
    await app.client.views_open(
        trigger_id=body["trigger_id"],
        view= compose_add_modal()
    )
  except Exception as e:
      logger.error(f"Error publishing home tab: {e}")
      
@app.action("button_delete_topic")
async def handle_delete_topic_view(ack, body, logger):
  await ack()
  user_id = body['user']['id']
  
  try:
    topics = await get_topics_by_user(user_id)
    await app.client.views_publish(
        user_id=user_id,
        view=compose_profile_delete(topics)
    )
  except Exception as e:
    logger.error(f"Error publishing delete view home tab: {e}")

@app.action("button_cancel_delete_topic")
async def handle_cancel_delete_topic(ack, body, logger):
  await ack()
  user_id = body['user']['id']
  try:
    await app.client.views_publish(
      user_id=user_id,
      view=profileviews[user_id]
    )
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")

@app.action("button_confirm_delete_topic")
async def handle_confirm_delete_topic(ack, body, logger):
  await ack()
  user_id = body['user']['id']
  topic_id = body['actions'][0]['value']
  
  #remove topic from db
  try:
    await delete_topic(topic_id)
  except Exception as e:
    logger.error(f"Error deleting topic: {e}")
  
  #read updated user topics from db
  try:
    topics = await get_topics_by_user(user_id)
    profileviews[user_id] = compose_profile(topics)
  except Exception as e:
    logger.error(f"Error composing profile: {e}")
  
  #publish updated profile view
  try:
    await app.client.views_publish(
      user_id=user_id,
      view=profileviews[user_id]
    )
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")
      
@app.view("topic_edit_modal")
async def topic_edit_submission(ack, body, view, logger):
  await ack()
  user_id = body['user']['id']
  topic_name = view["state"]["values"]["topic_name_field"]["topic_name_input"]["value"]
  topic_notes = view["state"]["values"]["topic_notes_field"]["topic_notes_input"]["value"]
  topic_id = view["private_metadata"] #topic_id is stored in modal "private_metadata" in views
  
  #write updated topic to db
  try:
    await update_topic(topic_name, topic_notes, topic_id)
  except Exception as e:
    logger.error(f"Error writing topic: {e}")
  
  #read updated user topics from db
  try:
    topics = await get_topics_by_user(user_id)
    profileviews[user_id] = compose_profile(topics)
  except Exception as e:
    logger.error(f"Error composing profile: {e}")
  
  #publish updated profile view
  try:
    await app.client.views_publish(
      user_id=user_id,
      view=profileviews[user_id]
    )
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")

@app.view("topic_add_modal")
async def topic_add_submission(ack, body, view, logger):
  await ack()
  user_id = body['user']['id']
  topic_name = view["state"]["values"]["topic_name_field"]["topic_name_input"]["value"]
  topic_notes = view["state"]["values"]["topic_notes_field"]["topic_notes_input"]["value"]
  
  #add new topic to db
  try:
    await add_topic(topic_name, topic_notes, user_id)
  except Exception as e:
    logger.error(f"Error adding topic: {e}")
  
  #read updated user topics from db
  try:
    topics = await get_topics_by_user(user_id)
    profileviews[user_id] = compose_profile(topics)
  except Exception as e:
    logger.error(f"Error composing profile: {e}")
  
  #publish updated profile view
  try:
    await app.client.views_publish(
      user_id=user_id,
      view=profileviews[user_id]
    )
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")

@app.action("admin_add_user")
async def handle_admin_add_user(ack, body, logger):
  #opens modal to add user to db
  await ack()
  
@app.action("admin_remove_user")
async def handle_admin_remove_user(ack, body, logger):
  #opens modal to remove user from db
  await ack()

@app.action("admin_add_badge_to_topic")
async def handle_admin_add_badge_to_topic(ack, body, logger):
  #opens modal to add badge to topic
  await ack()

async def get_workspace_users(logger):
  #Retrives all users from slack workspace and writes them to users.json
  try:
    response = await app.client.users_list()
    with open('users.json', 'w', encoding='utf-8') as f:
      json.dump(response['members'], f, ensure_ascii=False, indent=4)
    print("Wrote users to users.json")
  except Exception as e:
    logger.error(f"Error getting workspace users: {e}")
    
async def get_workspace_user(user_id, logger):
  #retrieves user info from slack workspace
  try:
    response = await app.client.users_info(user=user_id)
    print(response)
  except Exception as e:
    logger.error(f"Error getting workspace user: {e}")

async def main():
  print("Hello Darling, i'm asynchronous!")
  handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
  await handler.start_async()

if __name__ == '__main__':
    asyncio.run(main())