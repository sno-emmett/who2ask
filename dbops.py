#sqlite db operations
import sqlite3

async def search_db(query):
  #read db and query results
  con = sqlite3.connect("who2ask.db")
  cur = con.cursor()
  cur.execute('''SELECT users.user_id, users.real_name, users.image_72, topics.name, topics.notes
             FROM topics 
             INNER JOIN users 
             ON topics.owner = users.user_id
             WHERE topics.name LIKE ?''', ('%'+query+'%',))
  data = cur.fetchall()
  con.close()
  # for row in data:
  #   print(row)
  return data

async def get_topics_by_user(user_id):
  #return all topics by user
  con = sqlite3.connect("who2ask.db")
  cur = con.cursor()
  cur.execute('''SELECT topics.id, topics.name, topics.notes, topics.community_badge, topics.snohetta_badge
             FROM topics 
             INNER JOIN users 
             ON topics.owner = users.user_id
             WHERE users.user_id = ?''', (user_id,))
  data = cur.fetchall()
  con.close()
  # for row in data:
  #   print(row)
  return data

async def get_topic_by_id(topic_id):
  #return topic by id
  con = sqlite3.connect("who2ask.db")
  cur = con.cursor()
  cur.execute('''SELECT topics.id, topics.name, topics.notes, topics.community_badge, topics.snohetta_badge
             FROM topics 
             WHERE topics.id = ?''', (topic_id,))
  data = cur.fetchall()
  con.close()
  # for row in data:
  #   print(row)
  return data

async def update_topic(topic_name, topic_notes, topic_id):
  #update topic in db
  con = sqlite3.connect("who2ask.db")
  cur = con.cursor()
  cur.execute('''UPDATE topics SET name = ?, notes = ? WHERE id = ?''', (topic_name, topic_notes, topic_id))
  con.commit()
  con.close()
  return

async def add_topic(topic_name, topic_notes, topic_owner):
  #add topic to db
  con = sqlite3.connect("who2ask.db")
  cur = con.cursor()
  cur.execute("INSERT OR IGNORE INTO topics(name, owner, notes) VALUES (?, ?, ?)", (topic_name, topic_owner, topic_notes))
  topic_id = cur.lastrowid
  cur.execute("INSERT OR IGNORE INTO join_users_topics(user, topic) VALUES (?, ?)", (topic_owner, topic_id))
  con.commit()
  
async def delete_topic(topic_id):
  #delete topic from db
  con = sqlite3.connect("who2ask.db")
  cur = con.cursor()
  cur.execute('''DELETE FROM topics WHERE id = ?''', (topic_id,))
  con.commit()
  con.close()
  return

async def add_user(user_id, real_name, image_72):
  #add user to db
  con = sqlite3.connect("who2ask.db")
  cur = con.cursor()
  cur.execute("INSERT OR IGNORE INTO users(user_id, real_name, image_72) VALUES (?, ?, ?)", (user_id, real_name, image_72))
  con.commit()
  con.close()
  return

async def get_all_users():
  #return list of all users in db
  con = sqlite3.connect("who2ask.db")
  cur = con.cursor()
  cur.execute('''SELECT users.user_id, users.real_name, users.image_72
             FROM users''')
  data = cur.fetchall()
  con.close()
  return data