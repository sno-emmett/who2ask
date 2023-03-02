#sqlite db operations
import sqlite3

async def search_db(query):
  #read db and query results
  con = sqlite3.connect("who2ask.db")
  cur = con.cursor()
  cur.execute("SELECT * FROM TABLENAME WHERE name LIKE'%?%'",(query,))
  data = cur.fetchall()
  con.close()
  return data