import os
import math
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
import sklearn.cross_validation as cv

"""Takes a folder with .dat files formatted as specified and extracts their data.

usage(in a python shell for interactivity); from regress.py import main; main(path/to/folder)

This prints the quality assessment of the regressor and leave it saved in the variable 'learner' for further use. """


def main(folder):
    names = os.listdir(folder)
    texts = list()
    targets = list()
    for f in names:  # grabs information from files
        cur = open(folder + "/" + f).readlines()
        texts.append(os.path.splitext(f)[0] + cur[1])
        targets.append(math.log(evalWithCommas(cur[0])))
    extract = TfidfVectorizer(stop_words='english')
    print("extracting text...")
    data = extract.fit_transform(texts)
    learner = RandomForestRegressor()
    print("evaluating regressor...")
    quality = cv.cross_val_score(learner, data, targets, cv=10, n_jobs=-1)
    print(quality)


def evalWithCommas(numberString):
    oMag = 1
    returned = 0
    for n in numberString[::-1]:
        if n in "0123456789":
            returned += eval(n) * oMag
            oMag *= 10
    return returned
