from utils import *

CLOSE_TO_ZERO = 2
REFUSAL = 'REFUSAL'


def get_winner_simple(match, history):
    previous_home_match = get_prev_match_of_home_team(match['first_team'], history, match['date'])
    previous_guest_match = get_prev_match_of_guest_team(match['second_team'], history, match['date'])

    if previous_home_match is None or previous_guest_match is None:
        return None

    home_risk = previous_home_match['first_score'] - previous_home_match['second_score']

    guest_risk = previous_guest_match['second_score'] - previous_guest_match['first_score']

    total_risk = home_risk - guest_risk

    if abs(total_risk) <= CLOSE_TO_ZERO:
        return REFUSAL
    elif total_risk <= 0:
        return match['second_team']
    else:
        return match['first_team']


def main():
    history = get_history()
    my_results = []
    for i in range(len(history)):
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
        elif winner == REFUSAL:
            my_results.append(
                {
                    'match': history[i],
                    'my_result': REFUSAL,
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
    refusals = 0

    for res in my_results:
        sum_gain += res['gain']
        sum_correct += res['is_correct']
        if res['is_correct'] > 0:
            correct_predictions += 1
        elif res['is_correct'] < 0:
            incorrect_predictions += 1
        elif res['my_result'] == REFUSAL:
            refusals += 1
        else:
            drop_predictions += 1

    print('We gain: ', sum_gain)
    print('Per game gain: ', sum_gain / len(history))
    print('Total summarized predictions: ', sum_correct)
    print('Correct predictions: ', correct_predictions)
    print('Incorrect predictions: ', incorrect_predictions)
    print('We cannot predict: ', drop_predictions)
    print('Refusals: ', refusals)


main()

