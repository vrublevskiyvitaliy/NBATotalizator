import json


def all_data():
    data = {}
    with open('my_results_2014.json') as data_file:
        data['2014'] = json.load(data_file)
    with open('my_results_2013.json') as data_file:
        data['2013'] = json.load(data_file)
    with open('my_results_2012.json') as data_file:
        data['2012'] = json.load(data_file)
    return data


def main():
    data = all_data()
    for i in range(len(data['2014'])):
        sum = data['2014'][i]['gain'] + data['2013'][i]['gain'] + data['2013'][i]['gain']
        if sum > 0 or data['2014'][i]['gain'] > 0 and data['2013'][i]['gain'] > 0 and data['2013'][i]['gain'] > 0:
            print(data['2014'][i])
            print(data['2013'][i])
            print(data['2012'][i])
            print('*'**9)


main()