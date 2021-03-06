import numpy as np
import math
import scipy.stats
from utils import *

CLOSE_TO_ZERO = 0.13
REFUSAL = 'REFUSAL'
REFUSAL_TO_BAD_STATISTIC_AMOUNT = 1
REFUSAL_MAX_RISK = 0.2
all_data =[]


def get_probability(match, history):
    previous_home_match = get_all_prev_match_of_home_team(match['first_team'], history, match['date'])
    previous_guest_match = get_all_prev_match_of_guest_team(match['second_team'], history, match['date'])

    if len(previous_home_match) <= REFUSAL_TO_BAD_STATISTIC_AMOUNT or \
                    len(previous_guest_match) <= REFUSAL_TO_BAD_STATISTIC_AMOUNT:
        return None

    home_scores = [match['first_score'] - match['second_score'] for match in previous_home_match]
    guest_scores = [match['second_score'] - match['first_score'] for match in previous_guest_match]

    home_scores = np.array(home_scores)
    guest_scores = np.array(guest_scores)

    home_mean = np.mean(home_scores)
    guest_mean = np.mean(guest_scores)

    home_std = np.std(home_scores)
    guest_std = np.std(guest_scores)

    diff_mean = home_mean - guest_mean
    diff_std = math.sqrt(home_std**2 + guest_std**2)

    guest_win_probability = scipy.stats.norm(diff_mean, diff_std).cdf(0)
    home_win_probability = 1 - guest_win_probability
    return [home_win_probability, guest_win_probability]


def get_risk(match, history):
    probability = get_probability(match, history)

    if probability is None:
        return None

    [h_probability, g_probability] = probability

    home_risk = 1 - h_probability * match['f_odd']
    guest_risk = 1 - g_probability * match['s_odd']

    if home_risk > REFUSAL_MAX_RISK or guest_risk > REFUSAL_MAX_RISK:
        return None

    total_risk = guest_risk - home_risk
    #total_risk = h_probability - g_probability
    return total_risk


def get_winner_simple(match, history):
    risk = get_risk(match, history)
    if risk is None:
        return REFUSAL
    if abs(risk) <= CLOSE_TO_ZERO:
        return REFUSAL
    if risk <= 0:
        return [risk, match['second_team']]
    else:
        return [risk, match['first_team']]


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
            [risk, winner] = winner
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
                    'is_correct': is_correct,
                    'risk': risk
                }
            )

    sum_gain = 0
    sum_correct = 0
    first_team_win = 0
    correct_predictions = 0
    incorrect_predictions = 0
    drop_predictions = 0
    refusals = 0

    for res in my_results:
        if res['my_result'] == res['match']['first_team']:
            first_team_win += 1
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

    print('Prediction percent: ', correct_predictions*1./(len(history)-drop_predictions))
    print('We gain: ', sum_gain)
    print('Per game gain: ', sum_gain / len(history))
    print('Total summarized predictions: ', sum_correct)
    print('All predictions: ', correct_predictions + incorrect_predictions)
    print('Correct predictions: ', correct_predictions)
    print('Incorrect predictions: ', incorrect_predictions)
    print('We cannot predict: ', drop_predictions)
    print('Refusals: ', refusals)
    print('First team win: ', first_team_win)

    return my_results


def get_best_model():
    max_gain = -1000
    best_k1 = 0
    best_k2 = 0
    best_k3 = -100
    global CLOSE_TO_ZERO
    global REFUSAL_TO_BAD_STATISTIC_AMOUNT
    global REFUSAL_MAX_RISK
    global all_data
    cur = 0
    for k1 in range(20):
        k1_coef = k1 * 0.01
        CLOSE_TO_ZERO = k1_coef
        for k2 in range(6):
            k2_coef = k2
            REFUSAL_TO_BAD_STATISTIC_AMOUNT = k2_coef
            for k3 in range(10):
                k3_coef = k3 * 0.1 - 0.5
                REFUSAL_MAX_RISK = k3_coef
                gain = main()
                all_data.append({'k1': k1_coef, 'k2': k2_coef, 'k3': k3_coef, 'gain': gain})
                if gain > max_gain:
                    best_k1 = k1_coef
                    best_k2 = k2_coef
                    best_k3 = k3_coef
                    max_gain = gain
                cur += 1
                print cur
    print('BEST CLOSE_TO_ZERO: ' + str(best_k1))
    print('BEST REFUSAL_TO_BAD_STATISTIC_AMOUNT: ' + str(best_k2))
    print('BEST REFUSAL_MAX_RISK: ' + str(best_k3))
    print('We gain: ' + str(max_gain))
    write_to_file()


def write_to_file():
    global all_data
    with open('my_results_2012_.json', 'w') as outfile:
        json.dump(all_data, outfile)

get_best_model()
main()
