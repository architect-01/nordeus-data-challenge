# Data Challenge From Nordeus
This repository represents a solution for the Nordeus Data Challenge. <br/>

# DEMO
Based on the selected league id, the current scoreboard is presented as a table.

The Demo Application is available at : https://nordeus-data-challenge.herokuapp.com

![alt demo](https://github.com/architect-01/nordeus-data-challenge/blob/main/demo_material/frontent.png?raw=true)

Note: After 30 minutes of inactivity the App goes to sleep so the first time loading can be a little slower.

# Challenge Description 
As input you are given a dataset (JSONL format) where each line is a valid JSON object that represents an event generated by a football mobile game. 
Each event emitted from the game has several fields/ parameters that describe the action that is happening inside the game. 
Some examples of events are: user logged in, match started, goal scored, match ended, user logged out, etc. Link to the input dataset (data/raw_data/events.jsonl).

Your task is to process, clean and transform the source dataset into a new data model that will be capable of answering certain questions about the state of the game, specifically, we are interested in the current state of the leaderboard for each league.

Dataset (events.jsonl)
| Parameter Name      | Parameter Type | Parameter Description|
| ----------- | ----------- | ----------- |
| event_id      | INT       | Unique identifier representing an event|
| event_timestamp   | INT   |  Time of event represented as Unix time    |
| event_type  | STRING   | One of the following: match_start, goal, or match_end|
| event_data  | JSON OBJECT | JSON object containing all event-specific data (check event data below)|


Required event data for match_start
| Parameter Name      | Parameter Type | Parameter Description|
| ----------- | ----------- | ----------- |
| match_id      | INT       | Unique identifier representing a match|
| league_id   | INT   |  Unique identifier representing a league   |
| home_club  | STRING   | Name of home club|
| away_club  | STRING | Name of away club|



Required event data for goal
| Parameter Name      | Parameter Type | Parameter Description|
| ----------- | ----------- | ----------- |
| match_id      | INT       | Unique identifier representing a match|
| scoring_club   | STRING   |  One of the following: home or away  |

Required vent data for match_end

Required event data for goal
| Parameter Name      | Parameter Type | Parameter Description|
| ----------- | ----------- | ----------- |
| match_id      | INT       | Unique identifier representing a match|

More information is available in the file : Data Engineering Challenge.docx

# Solution's Approach

There are three stages to this solution: Data Cleanup, Database Setup and REST Api + Frontend.

## Data Cleanup

Technologies used: Python 3 and pandas (pip install pandas) 

Rationale : Extract the information in stages using intermediary .csv files. 

Steps taken :
1. Removed all invalid events and generated a .csv file of valid events [using : data_cleanup/cleanup.py]
2. Generated a compact information about the match [using : data_cleanup/creating_matches_table.py]
3. Generated a scoreboard .csv file that contains all leagues [using : data_cleanup/creating_scoreboard_table.py]

## Database Setup

Technologies used: Python 3, sqlalchemy (pip install pip install SQLAlchemy) and PostgreSQL(Heroku)

Rationale : Store the scoreboard table to a SQL database to have it be accessed by the REST Api.

Steps taken :
1. Setup Heroku and PostgreSQL Add On [out of scope of this README]
2. Populate the database [using: database_init/setup.py]

##  REST API + Frontend.

Technologies used: NodeJS, ExpressJS, ReactJS

Rationale : Create a basic application (both frontend and the API).

### REST API
The server has only one route : **/api/scoreboard?league_id=LEAGUE_ID**
  
- Where the LEAGUE_ID is an INT. If not provided, or not of type INT it will signal an error.
- The call returns a list of all the teams in the specific list with the information including team_name, points, goal_diff.
- Any other route leads to the Frontend.

Logic of the server : When the route is hit, select the teams from the league from the SQL database and order them (first by points, then by goal_diff and then by name).

Location of code : website/index.js


### Frontend

Out of scope.







