import pickle
import os
SRC_PATH = './movie_poster/'
files = [file for file in os.listdir(SRC_PATH) if file.endswith('.pickle')]
print(f"Num of files : {len(set(files))}")

non_empty_files = set()
empty_files = set()
empty_links = ['https://kobis.or.kr#', 'https://kobis.or.kr/#']


for idx, file in enumerate(files) :
    with open(SRC_PATH+file, 'rb') as f :
        result = pickle.load(f)
    print(f"idx : {idx}, result : {result}")
    (key, val), = result.items()
    if val in empty_links  :
        empty_files.add(key)
    else :
        non_empty_files.add(key)
    # if idx == 1000 :
    #     break

print(f"Num of empty files : {len(empty_files)}")
print(f"Num of non empty files : {len(non_empty_files)}")