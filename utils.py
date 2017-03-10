import json


def get_history():
    with open('data_2012.json') as data_file:
        data = json.load(data_file)
    return data


def get_old_history():
    with open('data_2013.json') as data_file:
        data = json.load(data_file)
    with open('data_2012.json') as data_file:
        data += json.load(data_file)
    return data


def get_prev_match_of_home_team(team, history, date):
    filtered_history = filter(lambda x: x['first_team'] == team, history)
    if filtered_history:
        return filtered_history[0]
    else:
        return None


def get_all_prev_match_of_home_team(team, history, date):
    filtered_history = filter(lambda x: x['first_team'] == team, history)
    return filtered_history


def get_prev_match_of_guest_team(team, history, date):
    filtered_history = filter(lambda x: x['second_team'] == team, history)
    if filtered_history:
        return filtered_history[0]
    else:
        return None


def get_all_prev_match_of_guest_team(team, history, date):
    filtered_history = filter(lambda x: x['second_team'] == team, history)
    return filtered_history