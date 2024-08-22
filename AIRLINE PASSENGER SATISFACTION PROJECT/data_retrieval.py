import sqlite3
conn=sqlite3.connect("customerdata.db")
cur=conn.cursor()
query="select*from CustomerDetails"

cur.execute(query)
for record in cur.fetchall():
    print(record)

cur.close()
cur.close()