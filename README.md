## Project 1 for Data Engineering Nanodegree

### Requirements
- Python 3.7.2
- Jupyter Notebook

### Files Structure
- create_tables.py -> Used to create & drop tables.
- sql_queries.py -> Contains all queries used in all the other files

### Purpose of Sparkify DB
- The fact table 'songplays' is used to read all the sessions of users song listening behaviour
- Using the table, we can analyse where is the user listening from (location and browser) at what time, frequency of listing of song at a particular day, hour or week, which artist or songs are frequently played

### Database schema & ETL
- All the dimension table are used to save the basic data of the songs, users, artist and time
- The fact table is used to provide summary of each of users session