from normal_distribution import *
import matplotlib.pyplot as plt


def get_roc_data():
    results = main()
    first_win = 0
    first_lose = 0
    without_refusal = []
    for res in results:
        if res['my_result'] is not None:
            without_refusal.append(res)
            if res['match']['second_score'] < res['match']['first_score']:
                first_win += 1
            else:
                first_lose += 1

    without_refusal = sorted(without_refusal, key=lambda x: -x['risk'])
    print(len(without_refusal))
    print(first_win)
    print(first_lose)
    print(first_lose + first_win)
    points = [[0, 0]]
    auc = 0
    for i in range(len(without_refusal)):
        previous_point = points[len(points) - 1]
        res = without_refusal[i]
        point = [0, 0]
        if res['match']['second_score'] < res['match']['first_score']:
            point[0] = previous_point[0]
            point[1] = previous_point[1] + 1./first_win
        else:
            point[0] = previous_point[0] + 1./first_lose
            point[1] = previous_point[1]
            if point[1] > 0:
                auc += 1.*point[1]/first_lose
        points.append(point)
    print(auc)
    print(points)
    fig = plt.figure()
    plt.plot(*zip(*points), marker='.', color='r', ls='')
    plt.show()



    # print(first_win)
    # print(first_lose)



get_roc_data()