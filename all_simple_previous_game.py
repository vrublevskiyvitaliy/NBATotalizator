
from utils import *


def get_risk(match, history):
    previous_home_match = get_all_prev_match_of_home_team(match['first_team'], history, match['date'])
    previous_guest_match = get_all_prev_match_of_guest_team(match['second_team'], history, match['date'])

    if len(previous_home_match) == 0 or len(previous_guest_match) == 0:
        return None

    home_risk = 0
    for match in previous_home_match:
        home_risk += match['first_score'] - match['second_score']
    home_risk /= len(previous_home_match)

    guest_risk = 0
    for match in previous_guest_match:
        guest_risk += match['second_score'] - match['first_score']
    guest_risk /= len(previous_guest_match)

    total_risk = home_risk - guest_risk
    return total_risk


def get_winner_simple(match, history):
    risk = get_risk(match, history)
    if risk is None:
        return None
    if risk <= 0:
        return match['second_team']
    else:
        return match['first_team']


def main():
    history = get_history()
    my_results = []
    for i in range(len(history)):
        if i == 1220:
            t = 0
        winner = get_winner_simple(history[i], history[i+1:])
        if winner is None:
            my_results.append(
                {
                    'match': history[i],
                    'my_result': None,
                    'gain': 0,
                    'is_correct': 0
                }
            )
        else:
            if history[i]['first_score'] > history[i]['second_score']:
                actual_winner = history[i]['first_team']
                gain_c = history[i]['f_odd']
            else:
                actual_winner = history[i]['second_team']
                gain_c = history[i]['s_odd']

            if winner == actual_winner:
                my_gain = gain_c - 1
                is_correct = 1
            else:
                my_gain = -1
                is_correct = -1

            my_results.append(
                {
                    'match': history[i],
                    'my_result': winner,
                    'gain': my_gain,
                    'is_correct': is_correct
                }
            )

    sum_gain = 0
    sum_correct = 0
    correct_predictions = 0
    incorrect_predictions = 0
    drop_predictions = 0
    for res in my_results:
        sum_gain += res['gain']
        sum_correct += res['is_correct']
        if res['is_correct'] > 0:
            correct_predictions += 1
        elif res['is_correct'] < 0:
            incorrect_predictions += 1
        else:
            drop_predictions += 1

    print('Prediction percent: ', correct_predictions*1./(len(history)-drop_predictions))
    print('We gain: ' + str(sum_gain))
    print('Per game gain: ' + str(sum_gain / len(history)))
    print('Total summarized predictions: ' + str(sum_correct))
    print('Correct predictions: ' + str(correct_predictions))
    print('Incorrect predictions: ' + str(incorrect_predictions))
    print('We cannot predict: ' + str(drop_predictions))


main()

