"""
optimize_SVC_parameters
Authors: Bhavit Patel
Date Created: March 2016

Exhaustive Grid Search / Brute Force parameter combinations
for finding the best parameters for svm.svc
Requires testing and cross-validation data
"""

from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC

import HandsOn


def optimize_SVC_parameters():
    print(__doc__)

    # Loading the training and cross-validation data
    trainingDataFile = 'initialTraining2_noquat.csv' # Training data
    cvDataFile = 'cvInitial2_noquat.csv' # Cross-validation data
    signTarget_train, signFeatures_train = HandsOn.readHandDataFromFile(trainingDataFile)
    signTarget_test, signFeatures_test = HandsOn.readHandDataFromFile(cvDataFile)

    # Set the parameters by cross-validation
    tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                         'C': [1, 10, 100, 1000]},
                        {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

    scores = ['precision', 'recall']

    for score in scores:
        print("# Tuning hyper-parameters for %s \n" % score) 

        clf = GridSearchCV(SVC(C=1), tuned_parameters, cv=5,
                           scoring='%s_weighted' % score)
        clf.fit(signFeatures_train, signTarget_train)

        print("Best parameters set found on development set:\n")
        print(clf.best_params_)
        print ""
        print("Grid scores on development set:\n")
        for params, mean_score, scores in clf.grid_scores_:
            print("%0.3f (+/-%0.03f) for %r"
                  % (mean_score, scores.std() * 2, params))
        print ""
        print("Detailed classification report:\n")
        print("The model is trained on the full development set.\n")
        print("The scores are computed on the full evaluation set.\n")
        signTarget_true, signTarget_pred = signTarget_test, clf.predict(signFeatures_test)
        print(classification_report(signTarget_true, signTarget_pred))
        print ""
    return 0
## end of optimzeSVM
