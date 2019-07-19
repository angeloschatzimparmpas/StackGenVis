from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

import json
import collections
import numpy as np
import pandas as pd  
import warnings
import copy
from joblib import Memory

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB 
from sklearn.ensemble import RandomForestClassifier
from mlxtend.classifier import StackingCVClassifier
from sklearn import model_selection
from sklearn.model_selection import GridSearchCV
from sklearn.manifold import MDS

# This block of code is for the connection between the server, the database, and the client (plus routing).

# Access MongoDB 
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mydb"
mongo = PyMongo(app)

cors = CORS(app, resources={r"/data/*": {"origins": "*"}})

# Retrieve data from client 
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/ServerRequest', methods=["GET", "POST"])
def RetrieveFileName():
    global fileName 
    fileName = request.get_data().decode('utf8').replace("'", '"') 
    return jsonify(fileName)

# Sent data to client 
@app.route('/data/ClientRequest', methods=["GET", "POST"])
def CollectionData():
    global DataRawLength
    global DataResultsRaw
    DataRawLength = -1
    data = json.loads(fileName)  
    if data['fileName'] == 'BreastC':
        CollectionDB = mongo.db.BreastC.find()
    elif data['fileName'] == 'DiabetesC':
        CollectionDB = mongo.db.DiabetesC.find()
    else:
        CollectionDB = mongo.db.IrisC.find()
    DataResultsRaw = []
    for index, item in enumerate(CollectionDB):
        item['_id'] = str(item['_id'])
        item['InstanceID'] = index
        DataResultsRaw.append(item)
    DataRawLength = len(DataResultsRaw)
    json.dumps(DataResultsRaw) 
    response = {
        'Collection': DataResultsRaw
    }
    return jsonify(response)



# Main function 
if __name__ == '__main__':
    app.run()

# Debugging and mirroring client
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")

# This block of code is for server computations 

global mem
mem = Memory("./cache_dir")

def GridSearch(clf, params, scoring, FI):
    
    grid = GridSearchCV(estimator=clf, 
                param_grid=params,
                scoring=scoring, 
                cv=5,
                refit='accuracy',
                n_jobs = -1)

    grid.fit(XData, yData)
        
    cv_results = []
    cv_results.append(grid.cv_results_)
    df_cv_results = pd.DataFrame.from_dict(cv_results)

    number_of_classifiers = len(df_cv_results.iloc[0][0])
    number_of_columns = len(df_cv_results.iloc[0])
    df_cv_results_per_item = []
    df_cv_results_per_row = []

    for i in range(number_of_classifiers):
        df_cv_results_per_item = []
        for column in df_cv_results.iloc[0]:
            df_cv_results_per_item.append(column[i])
        df_cv_results_per_row.append(df_cv_results_per_item)

    df_cv_results_classifiers = pd.DataFrame(data = df_cv_results_per_row, columns= df_cv_results.columns)
    parameters = df_cv_results_classifiers['params']
    FeatureImp = []
    if (FI == 1):
        for eachClassifierParams in grid.cv_results_['params']:
            eachClassifierParamsDictList = {}
            for key, value in eachClassifierParams.items():
                Listvalue = []
                Listvalue.append(value)
                eachClassifierParamsDictList[key] = Listvalue
            grid = GridSearchCV(estimator=clf, 
                param_grid=eachClassifierParamsDictList,
                scoring=scoring, 
                cv=5,
                refit='accuracy',
                n_jobs = -1)
            grid.fit(XData, yData)
            FeatureImp.append(grid.best_estimator_.feature_importances_)

    return df_cv_results_classifiers, parameters, FeatureImp

GridSearch = mem.cache(GridSearch)

def InitializeEnsemble():  
    DataResults = copy.deepcopy(DataResultsRaw)
    for dictionary in DataResultsRaw:
        for key in dictionary.keys():
            if (key.find('*') != -1):
                target = key
                continue
        continue

    DataResultsRaw.sort(key=lambda x: x[target], reverse=True)
    DataResults.sort(key=lambda x: x[target], reverse=True)

    for dictionary in DataResults:
        del dictionary['_id']
        del dictionary['InstanceID']
        del dictionary[target]

    AllTargets = [o[target] for o in DataResultsRaw]
    AllTargetsFloatValues = []
    previous = None
    Class = 0
    for i, value in enumerate(AllTargets):
        if (i == 0):
            previous = value
        if (value == previous):
            AllTargetsFloatValues.append(Class)
        else:
            Class = Class + 1
            AllTargetsFloatValues.append(Class)
            previous = value

    ArrayDataResults = pd.DataFrame.from_dict(DataResults)

    global XData, yData, RANDOM_SEED
    XData, yData = ArrayDataResults, AllTargetsFloatValues
    warnings.simplefilter('ignore')

    RANDOM_SEED = 42

    ClassifierIDsList = ''
    key = 0

    # Initializing models

    #scoring = {'accuracy': 'accuracy', 'f1_macro': 'f1_weighted', 'precision': 'precision_weighted', 'recall': 'recall_weighted', 'jaccard': 'jaccard_weighted', 'neg_log_loss': 'neg_log_loss', 'r2': 'r2', 'neg_mean_absolute_error': 'neg_mean_absolute_error', 'neg_mean_absolute_error': 'neg_mean_absolute_error'}
    scoring = {'accuracy': 'accuracy', 'f1_macro': 'f1_weighted', 'precision': 'precision_weighted', 'recall': 'recall_weighted', 'jaccard': 'jaccard_weighted'}
    NumberofscoringMetrics = len(scoring)
    results = []

    clf = KNeighborsClassifier()
    params = {'n_neighbors': [1, 2, 10]}
    IF = 0
    #params = {'n_neighbors': [1, 3, 5],
    #        'weights': ['uniform', 'distance'],
    #        'metric': ['euclidean', 'manhattan']}
    
    results.append(GridSearch(clf, params, scoring, IF))

    clf = RandomForestClassifier()
    params = {'n_estimators': [10, 50]}
    IF = 1

    results.append(GridSearch(clf, params, scoring, IF))

    df_cv_results_classifiers = pd.concat([results[0][0], results[1][0]], ignore_index=True, sort=False)
    parameters = pd.concat([results[0][1], results[1][1]], ignore_index=True, sort=False)

    classifiersIDPlusParams = [] 
    classifierID = 0
    for oneClassifier in parameters: 
        classifierID = classifierID + 1
        classifiersIDPlusParams.append(classifierID)
        classifiersIDPlusParams.append(oneClassifier)

    del df_cv_results_classifiers['params']
    df_cv_results_classifiers_metrics = df_cv_results_classifiers.copy()


    df_cv_results_classifiers_metrics = df_cv_results_classifiers_metrics.ix[:, 0:NumberofscoringMetrics+1]
    del df_cv_results_classifiers_metrics['mean_fit_time']
    del df_cv_results_classifiers_metrics['mean_score_time']

    sumPerClassifier = []
    for index, row in df_cv_results_classifiers_metrics.iterrows():
        rowSum = 0
        for elements in row:
            rowSum = elements + rowSum
        sumPerClassifier.append(rowSum)
        
    XClassifiers = df_cv_results_classifiers_metrics
    embedding = MDS(n_components=2, random_state=RANDOM_SEED)
    X_transformed = embedding.fit_transform(XClassifiers).T
    
    X_transformed = X_transformed.tolist()

    EnsembleModel(ClassifierIDsList, key)

    global ResultsforOverview
    ResultsforOverview = []
    ResultsforOverview.append(json.dumps(sumPerClassifier)) 
    ResultsforOverview.append(json.dumps(X_transformed)) 
    ResultsforOverview.append(json.dumps(classifiersIDPlusParams)) 

    return ResultsforOverview

# Retrieve data from client 
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/ServerRequestSelPoin', methods=["GET", "POST"])
def RetrieveSelClassifiersID():
    ClassifierIDsList = request.get_data().decode('utf8').replace("'", '"')
    key = 1
    EnsembleModel(ClassifierIDsList, key)
    return 'Everything Okay'

def EnsembleModel (ClassifierIDsList, keyRetrieved): 

    if (keyRetrieved == 0):
        all_classifiers = []
        all_classifiers.append(KNeighborsClassifier(n_neighbors=1))
        all_classifiers.append(KNeighborsClassifier(n_neighbors=2))
        all_classifiers.append(KNeighborsClassifier(n_neighbors=10))
        all_classifiers.append(RandomForestClassifier(random_state=RANDOM_SEED, n_estimators = 1))
        all_classifiers.append(RandomForestClassifier(random_state=RANDOM_SEED, n_estimators = 50))
        lr = LogisticRegression()

        sclf = StackingCVClassifier(classifiers=all_classifiers,
                            use_probas=True,
                            meta_classifier=lr,
                            random_state=RANDOM_SEED,
                            n_jobs = -1)
        for clf, label in zip([sclf], 
                        ['StackingClassifierAllClassifiers']):

            scores = model_selection.cross_val_score(clf, XData, yData, 
                                                    cv=5, scoring='accuracy')
            print("Accuracy: %0.2f (+/- %0.2f) [%s]" 
                % (scores.mean(), scores.std(), label))
    else:        
        all_classifiers = []                 
        ClassifierIDsList = ClassifierIDsList.split('"')
        for loop in ClassifierIDsList:
            if ('ClassifierID' in loop):
                if (loop == 'ClassifierID: 1'):
                    all_classifiers.append(KNeighborsClassifier(n_neighbors=1))
                elif (loop == 'ClassifierID: 2'):
                    all_classifiers.append(KNeighborsClassifier(n_neighbors=2))
                elif (loop == 'ClassifierID: 3'):
                    all_classifiers.append(KNeighborsClassifier(n_neighbors=10))
                elif (loop == 'ClassifierID: 4'):
                    all_classifiers.append(RandomForestClassifier(random_state=RANDOM_SEED, n_estimators = 1))
                else:
                    all_classifiers.append(RandomForestClassifier(random_state=RANDOM_SEED, n_estimators = 50))

        lr = LogisticRegression()

        sclf = StackingCVClassifier(classifiers=all_classifiers,
                            use_probas=True,
                            meta_classifier=lr,
                            random_state=RANDOM_SEED,
                            n_jobs = -1)
        for clf, label in zip([sclf], 
                        ['StackingClassifierSelectedClassifiers']):

            scores = model_selection.cross_val_score(clf, XData, yData, 
                                                    cv=5, scoring='accuracy')
            print("Accuracy: %0.2f (+/- %0.2f) [%s]" 
                % (scores.mean(), scores.std(), label))

# Sending the overview classifiers' results to be visualized as a scatterplot
@app.route('/data/PlotClassifiers', methods=["GET", "POST"])
def SendToPlot():
    while (len(DataResultsRaw) != DataRawLength):
        pass
    InitializeEnsemble()
    response = {    
        'OverviewResults': ResultsforOverview
    }
    return jsonify(response)