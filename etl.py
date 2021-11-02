import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    This function will proccess data from the song data files and insert them into their proper tables in the database, SONGS and USERS
    """
    # open song file
    df = pd.read_json(filepath, lines = True)

    # insert song record
    song_data = df[['song_id','title','artist_id','year','duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    This function will proccess data from the log data files and insert them into their proper tables in the database, USERS, TIME.
    Then after the tables for ARTISTS and SONGS has been created, uses the log file to add data to SONGPLAYS
    """
    # open log file
    df = pd.read_json(filepath, lines = True)

    # filter by NextSong action
    df.query("page == 'NextSong'",inplace = True)

    weekdays = {
    0: 'Sunday',
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday'}
    
    # convert timestamp column to datetime and exract relevant fields from datetime object
    time_df = pd.DataFrame(df['ts'])
    time_df['stamp'] = time_df['ts'].apply(lambda x: pd.to_datetime(x, unit = 'ms'))
    time_df['hour'] = time_df['stamp'].apply(lambda x: x.hour)
    time_df['day'] = time_df['stamp'].apply(lambda x: x.day)
    time_df['week'] = time_df['stamp'].apply(lambda x: x.week)
    time_df['month'] = time_df['stamp'].apply(lambda x: x.month)
    time_df['year'] = time_df['stamp'].apply(lambda x: x.year)
    time_df['weekday'] = time_df['stamp'].apply(lambda x: x.dayofweek).map(weekdays)
    time_df= time_df[['ts','hour','day','week','month','year','weekday']]

    
    # insert time data records
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

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
        songplay_data = (row.ts,row.userId, row.level, songid, artistid, row.sessionId,row.location,row.userAgent)

        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    This function will gather files needed for ETL then call the respective functions for allocating data from each file type into the correct database table.
    """
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


def main():
    """
    This function will connect to the database then call the ETL functions in this script to laod data into the database. 
    """
    #Connect to DB
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()
    
    #Do ETL
    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
