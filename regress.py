import sys
import os
import math
import numpy
from combine import CombiningClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime
import sklearn.cross_validation as cv

folder = sys.argv[1]
names = os.listdir(folder)
titles = list()
texts = list()
targets = list()
revCounts = list()
revRates = list()
dates = list()
extraVecs=list()
for f in names:  # grabs information from files
    cur = open(f + ".dat").readlines()
    texts.append(cur[0]+cur[2])
    targets.append(math.log(eval(cur[1])))
    revCounts.append(eval(cur[3]))
    revRates.append(eval(cur[4]))
    dates.append(datetime.strptime(cur[5], "%D"))
    extraVecs.append((eval(cur[3]),eval(cur[4]),len(cur[2])))
extract = TfidfVectorizer(stop_words='english')
data = extract.fit_transform(texts)
numpy.insert(data, 0, extraVecs, axis=0)
learner = CombiningClassifier()
quality = cv.cross_val_score(learner, data, targets, cv=10, n_jobs=-1)
print(quality)