
# DROP TABLES
songplay_table_drop = "DROP TABLE IF EXISTS SONGPLAYS;"
user_table_drop = "DROP TABLE IF EXISTS USERS;"
song_table_drop = "DROP TABLE IF EXISTS SONGS;"
artist_table_drop = "DROP TABLE IF EXISTS ARTISTS;"
time_table_drop = "DROP TABLE IF EXISTS TIME;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE SONGPLAYS (SONGPLAY_ID VARCHAR DEFAULT 'Unknown', START_TIME NUMERIC, USER_ID VARCHAR, LEVEL VARCHAR, SONG_ID VARCHAR DEFAULT 'Unknown', ARTIST_ID VARCHAR DEFAULT 'Unknown', SESSION_ID INT, LOCATION VARCHAR, USER_AGENT VARCHAR);
""")

user_table_create = ("""
CREATE TABLE USERS (USER_ID VARCHAR, FIRST_NAME VARCHAR, LAST_NAME VARCHAR, GENDER VARCHAR, LEVEL VARCHAR);
""")

song_table_create = ("""
CREATE TABLE SONGS (SONG_ID VARCHAR, TITLE VARCHAR, ARTIST_ID VARCHAR, YEAR INT, DURATION NUMERIC);
""")

artist_table_create = ("""
CREATE TABLE ARTISTS (ARTIST_ID VARCHAR, NAME VARCHAR, LOCATION VARCHAR, LATITUDE NUMERIC, LONGITUDE NUMERIC);
""")

time_table_create = ("""
CREATE TABLE TIME (START_TIME NUMERIC, HOUR SMALLINT, DAY SMALLINT, WEEK SMALLINT, MONTH SMALLINT, YEAR SMALLINT, WEEKDAY VARCHAR);
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO SONGPLAYS (SONGPLAY_ID, START_TIME, USER_ID, LEVEL, SONG_ID, ARTIST_ID, SESSION_ID, LOCATION, USER_AGENT) 
VALUES (%s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s)
ON CONFLICT DO NOTHING;
""")

user_table_insert = ("""
INSERT INTO USERS (USER_ID, FIRST_NAME, LAST_NAME, GENDER, LEVEL) 
VALUES (%s, %s, %s, %s, %s);
""")

song_table_insert = ("""INSERT INTO SONGS (SONG_ID, TITLE, ARTIST_ID, YEAR, DURATION) 
VALUES (%s, %s, %s, %s, %s);
""")

artist_table_insert = ("""
INSERT INTO ARTISTS (ARTIST_ID, NAME, LOCATION, LATITUDE, LONGITUDE) 
VALUES (%s, %s, %s, %s, %s);
""")


time_table_insert = ("""
INSERT INTO TIME (START_TIME, HOUR, DAY, WEEK, MONTH, YEAR, WEEKDAY) 
VALUES (%s, %s, %s, %s, %s, %s, %s);
""")

# FIND SONGS
song_select = (""" SELECT SONG_ID, ARTISTS.ARTIST_ID
                    FROM SONGS INNER JOIN ARTISTS 
                    ON SONGS.ARTIST_ID = ARTISTS.ARTIST_ID
                    WHERE
                    TITLE = %s
                    AND
                    NAME = %s 
                    AND
                    DURATION = %s;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]