import pickle
import csv

MOVIE_PICKLE_PATH = '../../data_analysis/movie/movie.pickle'
MOVIE_POSTER_PATH = "../photo/movie_poster/"

with open(MOVIE_PICKLE_PATH, 'rb') as bf :
    movies = pickle.load(bf)

csv_columns = [ 'movieCd', 'movieNm', 'prdtYear', 'openDt', 'prdtStatNm', 'repNationNm', 'posterUrl' ]
data = []

for movie_code, content in movies.items() :
    datum = {}
    for key, val in content.items() :
        if key in csv_columns :
            if key == 'openDt' :
                if val :
                    val = val[0:4]+'-'+val[4:6]+'-'+val[6:]
            datum[key] = val

    try :
        with open(f"{MOVIE_POSTER_PATH}{movie_code}_poster.pickle", 'rb') as f :
            poster_url = pickle.load(f)
        datum['posterUrl'] = poster_url[movie_code]
    except :
        print(f"Except : {movie_code}")

    data.append(datum)

with open('movie.csv', 'w') as f :
    writer = csv.DictWriter(f, fieldnames=csv_columns)
    writer.writeheader()
    for datum in data :
        writer.writerow(datum)
