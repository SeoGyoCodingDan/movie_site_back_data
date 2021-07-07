import os
import pickle
from collections import defaultdict

ORIGINAL_VISIT_PATH = "../visit.pickle"
POSTER_PATH = "../movie_poster/"
files = [ file for file in os.listdir('.') if file.endswith('.pickle') ]
not_yet = defaultdict(int)

with open(ORIGINAL_VISIT_PATH, 'rb') as f :
    ori_visit = pickle.load(f)

for file in files :
    with open(file, 'rb') as f :
        tmp_visit = pickle.load(f)

    for key, val in tmp_visit.items() :
        if val :
            ori_visit[key] = True
        else :
            not_yet[file] += 1

with open(ORIGINAL_VISIT_PATH, 'wb') as f :
    pickle.dump(ori_visit, f)


entire_files = set(frozenset( ori_visit.keys() ))
poster_files = { poster[:-14] for poster in os.listdir(POSTER_PATH) if poster.endswith('.pickle') }
sub = entire_files-poster_files

print(f"len(entire_files), len(poster_files) : {len(entire_files)}, {len(poster_files)}")
print(f"len(entire_files-poster_files) : {len(entire_files-poster_files)}")
print(f"sub : {sub}")
# print(f"entire_files-poster_files : {entire_files-poster_files}")
print(f"len(ori_visit) : {len(ori_visit)}")
print(f"not yet : {not_yet}")


