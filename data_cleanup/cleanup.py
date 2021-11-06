'''
    Creates a .csv file of all valid events [requirements listed in comments] based on provided .jsonl file of all events

    Header of output .csv file:
        event_id, event_timestamp, event_type, event_data, has_all_req_data, match_id
        
'''

import json
import pandas as pd

RAW_JSONL_FILEPATH = '..\\data\\raw_data\\events.jsonl'
OUTPUT_CSV_FILEPATH = '..\\data\\cleaned_data\\valid_events.csv'

def event_has_all_required_data(event):
    ''' returns True if all of the required event data for a specific event is present '''

    REQUIRED_EVENT_DATA = {
        'match_start' : ['match_id', 'league_id', 'home_club', 'away_club'],
        'goal'        : ['match_id', 'scoring_club'],
        'match_end'   : ['match_id']
    }

    for req_ev_data in REQUIRED_EVENT_DATA[event['event_type']]:
        if not req_ev_data in event['event_data']:
            return False
    return True

def get_match_id(event):
    ''' returns a match_id for a specific event '''
    return event['event_data']['match_id']

Log = {
    'n_events': {'raw_data' : -1, 'after_removing_duplicates': -1, 'after_removing_those_without_all_req_data': -1, 'after_removing_all_invalid_timestamps': -1}
}

with open(RAW_JSONL_FILEPATH, 'r') as raw_data:

    f_raw_lines = raw_data.readlines()

    records = [json.loads(frl) for frl in f_raw_lines]

    data_frame = pd.DataFrame.from_records(records) ;
    Log['n_events']['raw_data'] = len(data_frame)

    #Requirement 1 : Eliminate all duplicates - every event has a unique event_id
    data_frame = data_frame.drop_duplicates(subset = ['event_id']) ; 
    Log['n_events']['after_removing_duplicates'] = len(data_frame)

    #Requirement 2 : Eliminate all events that do not contain all the required data for that event_type
    data_frame['has_all_req_data'] = data_frame.apply(event_has_all_required_data, axis = 1)
    data_frame = data_frame.drop(data_frame[data_frame['has_all_req_data'] == False].index) ; 
    Log['n_events']['after_removing_those_without_all_req_data'] = len(data_frame)

    #Requirement 3 : Eliminate goal events that happened before match_start or after match_end
    #Requirement 4 : Eliminate matches that do not have a valid match_start or after match_end
    data_frame['match_id'] = data_frame.apply(get_match_id, axis = 1)
   
    match_ids = data_frame['match_id'].unique()
    for m_id in match_ids:
        #print( data_frame.query(f'match_id=={m_id}'))
        match_start = data_frame.query(f'match_id=={m_id} & event_type == "match_start"')['event_timestamp']
        match_end = data_frame.query(f'match_id=={m_id} & event_type == "match_end"')['event_timestamp']
        if not (len(match_start) > 0 and len(match_end) > 0):
            #Eliminate the current match because it doesnt have a valid match_start or match_end timestamp
            data_frame = data_frame.query(f'match_id!={m_id}')
            continue
        match_start = match_start.iloc[0] 
        match_end = match_end.iloc[0]
        if match_end < match_start:
            #Eliminate the current match because match_start has to be lesser than match_end timestamp
            data_frame = data_frame.query(f'match_id!={m_id}')
            continue

        data_frame = data_frame.query(f'(match_id!={m_id} ) | (match_id=={m_id} & event_timestamp >= {match_start} & event_timestamp <= {match_end})')

    Log['n_events']['after_removing_all_invalid_timestamps'] = len(data_frame)

    with open(OUTPUT_CSV_FILEPATH, 'w') as g:
        g.write(data_frame.to_csv())

print(f'Log: {Log}')