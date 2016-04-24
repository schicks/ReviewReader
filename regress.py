import os
import math
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
import sklearn.cross_validation as cv

"""Takes a folder with .dat files formatted as specified and extracts their data.

usage(in a python shell for interactivity); from regress.py import main; main(path/to/folder)

This prints the quality assessment of the regressor and leave it saved in the variable 'learner' for further use. """


def main(args):
    folder = args
    names = os.listdir(folder)
    texts = list()
    targets = list()
    for f in names:  # grabs information from files
        cur = open(f + ".dat").readlines()
        texts.append(f+cur[1])
        targets.append(math.log(eval(cur[0])))
    extract = TfidfVectorizer(stop_words='english')
    print("extracting text...")
    data = extract.fit_transform(texts)
    learner = RandomForestRegressor()
    print("evaluating regressor...")
    quality = cv.cross_val_score(learner, data, targets, cv=10, n_jobs=-1)
    print(quality)