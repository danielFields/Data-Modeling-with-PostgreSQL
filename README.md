# Data Modeling with PostgreSQL
This project creates and executes an ETL pipeline for a mock musicstreaming application. This was made during an assignment from the [Udacity Data Engineering Nanodegree](https://www.udacity.com/course/data-engineer-nanodegree--nd027).

# Purpose of Database
To store data from user activity on our Sparkify Music Streaming App in a database whose structure allows for analytical dataset creation and ad-hoc querying across several dimensions.

This ETL pipeline consists of two python scripts `create_tables.py` which removes old tables and set up new empty tables in the database and `etl.py` which populates the tables from the data found in the song data and log data.

Both of these scripts have been combines in the bash shell script `run_pipeline.sh`, so to run the full ETL pipeline run `bash run_pipeline.sh` from the command line.

## Data Sources
### Song Data
Song data is composed of many JSON files each contiaing infromation on the artist who created the song and the song's details.
```
{num_songs:1
artist_id:"ARKRRTF1187B9984DA"
artist_latitude:null
artist_longitude:null
artist_location:""
artist_name:"Sonora Santanera"
song_id:"SOXVLOJ12AB0189215"
title:"Amor De Cabaret"
duration:177.47546
year:0}
```
### Log Data
Log data is series of log files from the music listening appplication that details various statictics and facts about a user's activity on the platform. Shown blow, is an exmaple of one entry in the log file. (PII has been redacted, and in place is XXX to show where in an actual log that information would go.)
```
{'artist': "Des'ree",
 'auth': 'Logged In',
 'firstName': 'XXX',
 'gender': 'XXX',
 'itemInSession': 1,
 'lastName': 'XXX',
 'length': 246.30812,
 'level': 'free',
 'location': 'Phoenix-Mesa-Scottsdale, AZ',
 'method': 'PUT',
 'page': 'NextSong',
 'registration': 1540344794796.0,
 'sessionId': 139,
 'song': 'You Gotta Be',
 'status': 200,
 'ts': 1541106106796,
 'userAgent': '"Mozilla\\/5.0 (Windows NT 6.1; WOW64) AppleWebKit\\/537.36 (KHTML, like Gecko) Chrome\\/35.0.1916.153 Safari\\/537.36"',
 'userId': '8'}
```

## Schema Structure
The data in this database is organized into a star schema consisiting of the 1 fact table detailing songs listened to and by who in addition to 4 different dimension tables that add context to the user activity data generated from log files.   

![Schema ERD](Song_ERD.png)



## Analytical Insights

**Example Queries**

 * What are the top 10 most listened to songS?
```
SELECT SONGS.TITLE, COUNT(START_TIME) AS NUMBER_OF_LISTENS
FROM SONGS 
INNER JOIN
SONGPLAYS
ON SONGS.SONG_ID = SONGPLAYS.SONG_ID
GROUP BY SONGPLAYS.SONG_ID 
ORDER BY COUNT(START_TIME) DESC
LIMIT 10;
```

 * Which artist has the most songs in the database?
 ```
 (SELECT ARTIST_ID, NAME FROM ARTISTS) AS ARTIST_NAMES
 INNER JOIN
 (SELECT ARTIST_ID, COUNT(SONG_ID) AS N_SONGS FROM SONGS) AS SONG_COUNTS
 ON ARTIST_NAMES.ARTIST_ID = SONG_COUNTS.ARTIST_ID
 ORDER BY N_SONGS DESC
 LIMIT 1;
 ```
 
 To run ETL Process run `create_tables.py` before `etl.py` or use one of the command-line scripts that runs both in order.  
 If on a Windows machine run `run_pipeline.bat`
 If on a Unix machine run `run_pipeline.sh`
