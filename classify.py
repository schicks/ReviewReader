import numpy as np
import math
import matplotlib.pyplot as plt
import sqlite3 as sql
from scipy import interp, stats
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, chi2
from sklearn.cross_validation import StratifiedKFold
from sklearn.metrics import auc, roc_curve, f1_score

"""Takes a folder with folders of .dat files formatted as specified and extracts their data.

usage(in a python shell for interactivity); from regress.py import main; main(path/to/folder)

This prints the quality assessment of the regressor and leave it saved in the variable 'learner' for further use. """


def main():
    cursor = sql.connect('database.sqlite').cursor()
    cursor.execute("SELECT HelpfulnessNumerator, Text, UserId, Time, Score from Reviews")
    texts = list()
    targets = list()
    addData = [list(), list(), list()]
    reviews = cursor.fetchmany(10000)
    for row in reviews:
        texts.append(row[1])
        addData[0].append(row[2])
        addData[1].append(row[3])
        addData[2].append(row[4])
        targets.append(row[0])
    extract = TfidfVectorizer(stop_words='english')
    print(texts[0])
    print("binarizing...")
    targets = np.array(binarize(targets))
    addData[0] = integerfy(addData[0])
    addData = np.transpose(np.matrix(addData))
    print("generating folds...")
    cv = StratifiedKFold(targets, n_folds=10)
    print("extracting text...")
    data = extract.fit_transform(texts)
    print("performing feature reduction")
    data = SelectPercentile(chi2).fit_transform(data, targets)
    learner = GaussianNB()
    addLearner = GaussianNB()
    mean_tpr = 0
    mean_fpr = np.linspace(0, 1, 100)
    f1s = list()

    for i, (train_index, test_index) in enumerate(cv):
        print "analyzing fold %d" %(i+1)
        learner.fit(data[train_index].toarray(), targets[train_index])
        addLearner.fit(addData[train_index], targets[train_index])
        addprobas = addLearner.predict_proba(addData[test_index])
        baseprobas = learner.predict_proba(data[test_index].toarray())
        probas = [safehmean(addprobas[:,1][j], baseprobas[:,1][j]) for j in range(len(addprobas))]
        preds = [k > .5 for k in probas]
        f1s.append(f1_score(targets[test_index], preds))
        fpr, tpr, thresholds = roc_curve(targets[test_index], probas)
        mean_tpr += interp(mean_fpr, fpr, tpr)
        mean_tpr[0] = 0.0
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, lw=1, label='ROC fold %d (area = %0.2f)' % (i+1, roc_auc))
    plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')

    mean_tpr /= len(cv)
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    plt.plot(mean_fpr, mean_tpr, 'k--',
             label='Mean ROC (area = %0.2f)' % mean_auc, lw=2)

    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Negative Rate')
    plt.ylabel('True Negative Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.show()
    plt.savefig("ROC.png")
    avf=0
    for i in f1s:
        avf+=i
    avf/=len(f1s)
    print avf


def evalWithCommas(numberString):
    oMag = 1
    returned = 0
    for n in numberString[::-1]:
        if n in "0123456789":
            returned += eval(n) * oMag
            oMag *= 10
    return returned


def binarize(targets):
    booleans = list()
    threshold = sorted(targets)[int(math.floor(len(targets)*.1))]#clearly an integer, calm down python
    for i in targets:
        booleans.append(i is 0)

    print len(booleans)
    return booleans


def integerfy(ids):
    seen = dict()
    count = 0
    for id in ids:
        if id not in seen:
            seen[id] = count
            count += 1
    return [seen[id] for id in ids]

def isPositive(nums):
    for i in nums:
        if i<=0:
            print i
            return False
    return True

def safehmean(a,b):
    try:
        return stats.hmean([a,b])
    except ValueError:
        return 0


main()
