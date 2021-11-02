
# DROP TABLES
songplay_table_drop = "DROP TABLE IF EXISTS SONGPLAYS;"
user_table_drop = "DROP TABLE IF EXISTS USERS;"
song_table_drop = "DROP TABLE IF EXISTS SONGS;"
artist_table_drop = "DROP TABLE IF EXISTS ARTISTS;"
time_table_drop = "DROP TABLE IF EXISTS TIME;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE SONGPLAYS 
(SONGPLAY_ID SERIAL, 
START_TIME NUMERIC NOT NULL, 
USER_ID VARCHAR NOT NULL, 
LEVEL VARCHAR, 
SONG_ID VARCHAR DEFAULT 'Unknown', 
ARTIST_ID VARCHAR DEFAULT 'Unknown', 
SESSION_ID INT, LOCATION VARCHAR, 
USER_AGENT VARCHAR,
PRIMARY KEY(START_TIME, USER_ID));
""")

user_table_create = ("""
CREATE TABLE USERS 
(USER_ID VARCHAR PRIMARY KEY, 
FIRST_NAME VARCHAR, 
LAST_NAME VARCHAR, 
GENDER VARCHAR, 
LEVEL VARCHAR);
""")

song_table_create = ("""
CREATE TABLE SONGS 
(SONG_ID VARCHAR PRIMARY KEY,
TITLE VARCHAR, 
ARTIST_ID VARCHAR, 
YEAR INT, 
DURATION NUMERIC);
""")

artist_table_create = ("""
CREATE TABLE ARTISTS 
(ARTIST_ID VARCHAR PRIMARY KEY, 
NAME VARCHAR, 
LOCATION VARCHAR, 
LATITUDE NUMERIC, 
LONGITUDE NUMERIC);
""")

time_table_create = ("""
CREATE TABLE TIME 
(START_TIME NUMERIC PRIMARY KEY, 
HOUR SMALLINT, 
DAY SMALLINT, 
WEEK SMALLINT, 
MONTH SMALLINT, 
YEAR SMALLINT, 
WEEKDAY VARCHAR);
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO SONGPLAYS (START_TIME, USER_ID, LEVEL, SONG_ID, ARTIST_ID, SESSION_ID, LOCATION, USER_AGENT) 
VALUES ( %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s)
ON CONFLICT (start_time, user_id) DO UPDATE SET start_time=EXCLUDED.start_time, user_id=EXCLUDED.user_id, level=EXCLUDED.level, location=EXCLUDED.location, user_agent = EXCLUDED.user_agent;
""")

user_table_insert = ("""
INSERT INTO USERS (USER_ID, FIRST_NAME, LAST_NAME, GENDER, LEVEL) 
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id) DO UPDATE SET user_id=EXCLUDED.user_id, first_name =EXCLUDED.first_name, last_name=EXCLUDED.last_name, gender=EXCLUDED.gender, level=EXCLUDED.level;
""")

# Making the decision here to omit songs that have duplicate song ID's since in the JSON files the two songs with matching song ID's are the same.
song_table_insert = ("""INSERT INTO SONGS (SONG_ID, TITLE, ARTIST_ID, YEAR, DURATION) 
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (song_id) DO NOTHING;
""")

artist_table_insert = ("""
INSERT INTO ARTISTS (ARTIST_ID, NAME, LOCATION, LATITUDE, LONGITUDE) 
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (artist_id) DO UPDATE SET location=EXCLUDED.location, latitude=EXCLUDED.latitude, longitude=EXCLUDED.longitude;
""")


time_table_insert = ("""
INSERT INTO TIME (START_TIME, HOUR, DAY, WEEK, MONTH, YEAR, WEEKDAY) 
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (start_time) DO UPDATE SET start_time=EXCLUDED.start_time, hour=EXCLUDED.hour, day=EXCLUDED.day, week=EXCLUDED.week,month=EXCLUDED.month, year=EXCLUDED.year,weekday=EXCLUDED.weekday;
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
