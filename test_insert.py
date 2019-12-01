import psycopg2
from sql_queries import *
import pandas as pd


conn = psycopg2.connect("host=0.0.0.0 port=54320 dbname=sparkifydb user=postgres")
cur = conn.cursor()

songplay_data = (int(2), '2018-11-01 21:01:46.796000', int(8), '12132132', '12312321321', int(139), 'Phoenix-Mesa-Scottsdale, AZ', 'Mozilla')
try:
    cur.execute(songplay_table_insert, songplay_data)
except Exception as e:
    print("Unable to insert songplays data")
    print(e)
