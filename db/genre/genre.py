import pickle
import csv

GENRE_PICKLE_PATH = '../../data_analysis/movie/genre_collection.pickle'

with open(GENRE_PICKLE_PATH, 'rb') as bf :
    genres = pickle.load(bf)

csv_columns = [ 'movieCd', 'genreAlt' ]
data = []
# max_len = -1
for gen in genres :
    row = {}
    for movie_code, genre in gen.items() :
        row[csv_columns[0]] = movie_code
        row[csv_columns[1]] = genre
        # max_len = max(max_len, len(genre))
    data.append(row)
# print(max_len)
# exit()
with open('genre.csv', 'w') as f :
    writer = csv.DictWriter(f, fieldnames=csv_columns)
    writer.writeheader()
    for datum in data :
        writer.writerow(datum)
