'''
    Creates a .csv file of all teams and their current points as well as goal difference

    Header of output .csv file:
        event_id, start_timestamp, match_id, league_id, home, away, home_goals, away_goals

    Header of output .csv file:
        league_id, team_name, points, goal_diff

'''

import pandas as pd
import json
import ast

INPUT_CSV_FILEPATH = '..\\data\\cleaned_data\\matches.csv' 
OUTPUT_CSV_FILEPATH = '..\\data\\cleaned_data\\scoreboards.csv'

all_df = pd.read_csv(INPUT_CSV_FILEPATH)

all_scb_df = pd.DataFrame(data = {'league_id': [], 'team_name' : [], 'points': [], 'goal_diff': []})

for league_id in range(1, 10): # for every league calculate the points and goal_diff for each team

    df = all_df.query(f'league_id=={league_id}')

    all_teams = list(set(df['home'].unique().tolist() + df['away'].unique().tolist()))

    scb_df = pd.DataFrame(data = {'league_id': int(league_id), 'team_name' : all_teams, 'points': 0, 'goal_diff': 0})

    points_col = [] ; goal_dif_col = []
    for t in all_teams: # for every team create a df of matches it was involved in and do the points and goal_diff calculation
        points = 0 ; goal_diff = 0
        team_matches_df = df.query(f'home=="{t}"')
        for index, row in team_matches_df.iterrows():
            if row['home_goals'] > row['away_goals']:
                points += 3
            if row['home_goals'] == row['away_goals']:
                points += 1

            goal_diff += row['home_goals'] - row['away_goals']
        
        team_matches_df = df.query(f'away=="{t}"')
        for index, row in team_matches_df.iterrows():
            if row['home_goals'] < row['away_goals']:
                points += 3
            if row['home_goals'] == row['away_goals']:
                points += 1

            goal_diff -= row['home_goals'] - row['away_goals']

        points_col.append(points) ; goal_dif_col.append(goal_diff)

    scb_df['points'] = points_col ; scb_df['goal_diff'] = goal_dif_col ; 
    scb_df = scb_df.sort_values(['points', 'team_name'])

    all_scb_df = pd.concat([all_scb_df, scb_df])

all_scb_df = all_scb_df.astype({'league_id': int, 'points': int, 'goal_diff': int})

with open(OUTPUT_CSV_FILEPATH, 'w') as g:
    g.write(all_scb_df.to_csv())
