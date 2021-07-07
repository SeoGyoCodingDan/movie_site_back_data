from selenium import webdriver
from bs4 import BeautifulSoup
import pickle
import time
import os
from multiprocessing import Process, current_process

MOVIE_LIST_PATH = '../../data_analysis/movie/movie.pickle'
VISIT_LIST_PATH = './visit/'
MOVIE_POSTER_PATH = './movie_poster/'
# HOW_MANY = 2000
# HOW_MANY = 3400
# HOW_MANY = 1500
# HOW_MANY = 100 # 대략 700초 정도
HOW_MANY = 11
CHECK_POINT = 100
NUM_OF_PROC = 10
NUM_OF_FIL_PER_PROC = 7700

BASE_URL = 'https://kobis.or.kr/kobis/business/mast/mvie/searchMovieList.do?dtTp=movie&dtCd='
BASE_RESULT_URL = 'https://kobis.or.kr/'

def make_visit_list() :
    global MOVIE_LIST_PATH, VISIT_LIST_PATH, MOVIE_POSTER_PATH
    global NUM_OF_FIL_PER_PROC

    with open(MOVIE_LIST_PATH, 'rb') as f:
        MOVIE_LIST = pickle.load(f)
    VISIT = {movie_code : False for movie_code in MOVIE_LIST}
    already_files = [ file[:file.index('_')] for file in os.listdir(MOVIE_POSTER_PATH) if file.endswith('pickle') ]

    # print(len(already_files))
    # print(already_files[:100])

    for already_file in already_files :
        VISIT[already_file] = True

    # tmp = [val for val in VISIT.values() if val == False]
    # print(len(tmp))
    # exit()
    # print(VISIT)
    # exit()

    file_count, visit_idx = 0, 0
    MINI_VISIT = {}
    for key, val in VISIT.items() :
        if val :
            continue

        MINI_VISIT[key] = val
        file_count += 1

        if file_count == NUM_OF_FIL_PER_PROC :
            with open(VISIT_LIST_PATH+f"visit_{visit_idx}.pickle", 'wb') as f :
                pickle.dump(MINI_VISIT, f)
            file_count = 0
            visit_idx += 1
            print(f"visit_idx : {visit_idx}, len(MINI_VISIT) : {len(MINI_VISIT)}")
            MINI_VISIT = {}

    return file_count


def crawling(VISIT_PATH) :
    global CHECK_POINT
    mini_start_time = time.time()
    with open(VISIT_PATH, 'rb') as f :
        VISIT = pickle.load(f)
    file_count = 0
    for movie_code, is_visit in VISIT.items() :
        if is_visit :
            continue

        try:
            url = BASE_URL + movie_code
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)
            driver.get(url)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            img_src = soup.find("a", {'class': 'fl thumb'})

            target_url = img_src['href']
            result_url = BASE_RESULT_URL + target_url

            result = {movie_code: result_url}
            with open(MOVIE_POSTER_PATH + f"{movie_code}_poster.pickle", 'wb') as f:
                pickle.dump(result, f)

            VISIT[movie_code] = True
            file_count += 1

            if file_count != 0 and file_count % CHECK_POINT == 0:
                print(f"Process-id : {current_process().name}, file_count : {file_count}")
                print(f"Process-id : {current_process().name}, execution time : {time.time() - mini_start_time}")

            if file_count == HOW_MANY:
                break

        except:
            continue

    with open(VISIT_PATH, 'wb') as f:
        pickle.dump(VISIT, f)

if __name__ == '__main__' :
    start_time = time.time()
    # num_of_visit_files = make_visit_list()
    # MINI_VISIT_PATH = [f"{VISIT_LIST_PATH}visit_{idx}.pickle" for idx in range(num_of_visit_files)]
    MINI_VISIT_PATH = [f"{VISIT_LIST_PATH}visit_{idx}.pickle" for idx in range(NUM_OF_PROC)]
    procs = []

    for visit_path in MINI_VISIT_PATH :
        proc = Process(target=crawling, args=(visit_path,))
        procs.append(proc)
        proc.start()

    for proc in procs :
        proc.join()

    print(f"Execution time : {time.time()-start_time}")