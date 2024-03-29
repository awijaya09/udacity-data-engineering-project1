import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


"""
    This function processes Song JSON from a Filepath
    and save the song data and artist data to the respective tables

    Input:
    cur -> refers to the cursor to the database
    filepath -> filepath string to the json files
"""


def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[["song_id", "title", "artist_id", "year", "duration"]].values.tolist()
    cur.execute(song_table_insert, song_data[0])

    # insert artist record
    artist_data = df[["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]].values.tolist()
    cur.execute(artist_table_insert, artist_data[0])


"""
    This function processes Log JSON from a Filepath
    and save time data and songplay records

    Input:
    cur -> refers to the cursor to the database
    filepath -> filepath string to the json files
"""


def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page == "NextSong"]
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')

    # insert time data records
    time_data = list((t, t.dt.hour, t.dt.day, t.dt.weekofyear, t.dt.month, t.dt.year, t.dt.weekday))
    column_labels = list(("start_time", "hour", "day", "week", "month", "year", "weekday"))
    time_df = pd.DataFrame.from_dict(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


"""
    The process_data function loops all the files in the directory
    and return the files
"""


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


"""
    The main function connects to the database and get the cursor.
    The function also calls to the above process song and log data

    Once all excuted the the database connection si closed.
"""


def main():
    conn = psycopg2.connect("host=0.0.0.0 port=54320 dbname=sparkifydb user=postgres")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
