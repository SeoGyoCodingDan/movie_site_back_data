import pickle
import csv

FILMO_PICKLE_PATH = '../../data_analysis/people_info/filmo_collection.pickle'

with open(FILMO_PICKLE_PATH, 'rb') as bf :
    filmos = pickle.load(bf)

csv_columns = [ 'movieCd', 'moviePartNm', 'peopleCd' ]
data = []

for filmo in filmos :
    row = {}
    for key, val in filmo.items() :
        if key in csv_columns :
            row[key] = val
    data.append(row)

with open('filmo.csv', 'w') as f :
    writer = csv.DictWriter(f, fieldnames=csv_columns)
    writer.writeheader()
    for datum in data :
        writer.writerow(datum)
