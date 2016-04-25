import os
import numpy as np
import math
import matplotlib.pyplot as plt
import re
from sys import argv
from scipy import interp
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import StratifiedKFold
from sklearn.metrics import auc, roc_curve

"""Takes a folder with folders of .dat files formatted as specified and extracts their data.

usage(in a python shell for interactivity); from regress.py import main; main(path/to/folder)

This prints the quality assessment of the regressor and leave it saved in the variable 'learner' for further use. """


def main(folder):
    books = os.listdir(folder)
    texts = list()
    targets = list()
    for book in books:
        names = os.listdir(folder+"/"+book)
        curtargets = list()
        for f in names:  # grabs information from files
            cur = open(folder + "/"+book+"/" + f).readline()
            curtargets.append(math.log(evalWithCommas(re.match("([0-9,]*)", cur).group(1))))
            texts.append(os.path.splitext(f)[0] + cur)
        targets.extend(booleanize(curtargets))
    extract = TfidfVectorizer(stop_words='english')
    cv = StratifiedKFold(targets, n_folds=5)
    print("extracting text...")
    targets=np.array(targets)
    data = extract.fit_transform(texts)
    learner = RandomForestClassifier()
    mean_tpr = 0
    mean_fpr = np.linspace(0, 1, 100)

    for i, (train_index, test_index) in enumerate(cv):
        probas = learner.fit(data[train_index], targets[train_index]).predict_proba(data[test_index])
        fpr, tpr, thresholds = roc_curve(targets[test_index], probas[:, 1])
        mean_tpr += interp(mean_fpr, fpr, tpr)
        mean_tpr[0] = 0.0
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, lw=1, label='ROC fold %d (area = %0.2f)' % (i, roc_auc))
    plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')

    mean_tpr /= len(cv)
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    plt.plot(mean_fpr, mean_tpr, 'k--',
             label='Mean ROC (area = %0.2f)' % mean_auc, lw=2)

    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()


def evalWithCommas(numberString):
    oMag = 1
    returned = 0
    for n in numberString[::-1]:
        if n in "0123456789":
            returned += eval(n) * oMag
            oMag *= 10
    return returned


def booleanize(targets):
    sortedTargets = sorted(targets)
    booleans = list()
    for i in targets:
        booleans.append(i not in sortedTargets[0:len(targets)/10])
    return(booleans)


main(argv[1])