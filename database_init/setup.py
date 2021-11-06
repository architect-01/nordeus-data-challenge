'''
    Initializes the PostgreSQL database [for HEROKU app] with scoreboards for all leagues

    Column names for 'scoreboards' table:
        league_id, team_name, points, goal_diff

'''

import pandas as pd
from sqlalchemy import create_engine


PostgreSQL_URI = # GET FROM HEROKU

engine = create_engine(PostgreSQL_URI)

# df = pd.read_csv('..//data//cleaned_data//matches.csv')
# df.to_sql('matches', engine)

df = pd.read_csv('..//data//cleaned_data//scoreboards.csv')
df.to_sql('scoreboards', engine)
