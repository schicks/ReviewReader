import numpy
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import LinearSVR


class CombiningClassifier:

    def __init__(self):
        self.textClassifier = RandomForestRegressor()
        self.extraClassifier = LinearSVR()

    def fit(self, X, y):
        extra = X[0:3:]
        text = X[3::]
        self.textClassifier.fit(text, y)
        self.extraClassifier.fit(extra, y)

    def predict(self, X):
        text = self.textClassifier.predict(X)
        extra = self.extraClassifier.predict(X)
        ours = list()
        for i in range(len(X)):
            ours.append(2/((1/text[i])+(1/extra[i])))
        return ours
