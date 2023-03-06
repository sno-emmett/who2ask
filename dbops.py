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