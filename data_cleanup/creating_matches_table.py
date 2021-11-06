'''
    Creates a .csv file of all matches based on provided .csv file of valid events

    Header of input .csv file:
        event_id, event_timestamp, event_type, event_data, has_all_req_data, match_id

    Header of output .csv file:
        event_id, start_timestamp, match_id, league_id, home, away, home_goals, away_goals

'''

import pandas as pd
import json
import ast

INPUT_CSV_FILEPATH = '..\\data\\cleaned_data\\valid_events.csv'
OUTPUT_CSV_FILEPATH = '..\\data\\cleaned_data\\matches.csv'

df = pd.read_csv(INPUT_CSV_FILEPATH)

def set_league_id(match):
    ''' returns a league_id [int] for a specific match '''
    return ast.literal_eval(match['event_data'])['league_id']
def set_home_team(match):
    ''' returns a home_team [string] for a specific match '''
    return ast.literal_eval(match['event_data'])['home_club']
def set_away_team(match):
    ''' returns a away_team [string] for a specific match '''
    return ast.literal_eval(match['event_data'])['away_club']


matches_df = df.query('event_type=="match_start"')
matches_df['league_id'] =  matches_df.apply(set_league_id, axis = 1)
matches_df['home'] = matches_df.apply(set_home_team, axis = 1)
matches_df['away'] = matches_df.apply(set_away_team, axis = 1)
matches_df['home_goals'] = -1
matches_df['away_goals'] = -1

matches_df = matches_df.drop(columns = ['event_data', 'has_all_req_data', 'event_type'])
matches_df = matches_df.rename(columns={"event_timestamp": "start_timestamp"})
def goal_scored_by(event):
    ''' returns a string ['home_club' or 'away_club'] that means which team scored the goal '''
    temp = ast.literal_eval(event['event_data']);
    return temp['scoring_club']

goals_df = df.query('event_type=="goal"')
goals_df['goal_scored_by'] = goals_df.apply(goal_scored_by, axis = 1)

match_ids = matches_df['match_id'].tolist()
for m_id in match_ids:
    row_idx = matches_df.index[matches_df['match_id'] == m_id]
    matches_df.loc[row_idx, 'home_goals'] = len(goals_df.query(f'match_id=={m_id} & goal_scored_by=="home"'))
    matches_df.loc[row_idx, 'away_goals'] = len(goals_df.query(f'match_id=={m_id} & goal_scored_by=="away"'))

with open(OUTPUT_CSV_FILEPATH, 'w') as g:
    g.write(matches_df.to_csv())
