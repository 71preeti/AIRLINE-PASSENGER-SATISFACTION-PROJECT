import sqlite3
conn=sqlite3.connect('customerdata.db')

query_to_create_table="""
CREATE TABLE CustomerDetails (
age int,
flight_distance int ,
inflight_entertainment int,
baggage_handling int ,
cleanliness int ,
departure_delay int ,
arrival_delay int ,
gender varchar(200),
customer_type varchar(200),
travel_type varchar(200),
economy varchar(200),
economy_plus varchar(200),
PREDICTION  varchar(200)
);


"""

cur=conn.cursor()
cur.execute(query_to_create_table)
print("YOUR DATABASE AND TABLE IS CREATED")
cur.close()
conn.close()
