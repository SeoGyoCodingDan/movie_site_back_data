import pickle
import csv

PEOPLE_PICKLE_PATH = '../../data_analysis/people_info/people_info.pickle'

with open(PEOPLE_PICKLE_PATH, 'rb') as bf :
    people = pickle.load(bf)

csv_columns = [ 'peopleCd', 'peopleNm', 'sex', 'repRoleNm' ]
data = []

for people_code, content in people.items() :
    datum = {}
    for key, val in content.items() :
        if key in csv_columns :
            datum[key] = val
    data.append(datum)

with open('people.csv', 'w') as f :
    writer = csv.DictWriter(f, fieldnames=csv_columns)
    writer.writeheader()
    for datum in data :
        writer.writerow(datum)