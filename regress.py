import sys
import os
from sklearn.svm import SVR
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
for f in names:  # grabs information from files
    cur = open(f + ".dat").readlines()
    texts.append(cur[2])
    targets.append(eval(cur[1]))
    titles.append(cur[0])
    revCounts.append(eval(cur[3]))
    revRates.append(eval(cur[4]))
    dates.append(datetime.strptime(cur[5], "%D"))
extract = TfidfVectorizer(stop_words='english')
textLearner = SVR()
quality = cv.cross_val_score(textLearner, extract.fit_transform(texts), targets, cv=10, n_jobs=-1)
print(quality)