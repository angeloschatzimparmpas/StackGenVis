from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

import json
import collections
import numpy as np
import re
from numpy import array
import pandas as pd  
import warnings
import copy
from joblib import Memory
from itertools import chain

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB 
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn import model_selection
from sklearn.model_selection import GridSearchCV
from sklearn.manifold import MDS
from sklearn.manifold import TSNE
from sklearn.metrics import classification_report
from sklearn.preprocessing import scale

from mlxtend.classifier import StackingCVClassifier
from mlxtend.feature_selection import ColumnSelector

# This block of code is for the connection between the server, the database, and the client (plus routing).

# Access MongoDB 
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mydb"
mongo = PyMongo(app)

cors = CORS(app, resources={r"/data/*": {"origins": "*"}})

# Retrieve data from client 
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/Reset', methods=["GET", "POST"])
def Reset():
    global DataRawLength
    global DataResultsRaw
    global RANDOM_SEED
    RANDOM_SEED = 42

    global XData
    XData = []

    global yData
    yData = []

    global algorithmList
    algorithmList = []

    global ClassifierIDsList
    ClassifierIDsList = ''

    # Initializing models

    global classifiersId
    classifiersId = []
    global classifiersIDwithFI
    classifiersIDwithFI = []
    global classifiersIDPlusParams
    classifiersIDPlusParams = [] 
    global classifierID
    classifierID = 0

    global resultsList
    resultsList = []

    global RetrieveModelsList
    RetrieveModelsList = []

    global allParametersPerformancePerModel
    allParametersPerformancePerModel = []

    global all_classifiers
    all_classifiers = []

    global crossValidation
    crossValidation = 3

    global scoring
    #scoring = {'accuracy': 'accuracy', 'f1_macro': 'f1_weighted', 'precision': 'precision_weighted', 'recall': 'recall_weighted', 'jaccard': 'jaccard_weighted', 'neg_log_loss': 'neg_log_loss', 'r2': 'r2', 'neg_mean_absolute_error': 'neg_mean_absolute_error', 'neg_mean_absolute_error': 'neg_mean_absolute_error'}
    scoring = {'accuracy': 'accuracy', 'f1_macro': 'f1_weighted', 'precision': 'precision_weighted', 'recall': 'recall_weighted', 'jaccard': 'jaccard_weighted'}

    global yPredictProb
    yPredictProb = []
    
    global loopFeatures
    loopFeatures = 2

    global columns 
    columns = []

    global results
    results = []

    global target_names
    target_names = []
    return 'The reset was done!'

# Retrieve data from client 
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/ServerRequest', methods=["GET", "POST"])
def RetrieveFileName():
    fileName = request.get_data().decode('utf8').replace("'", '"') 
    global featureSelection 
    featureSelection = request.get_data().decode('utf8').replace("'", '"')
    featureSelection = json.loads(featureSelection)
    global DataRawLength
    global DataResultsRaw
    global RANDOM_SEED
    RANDOM_SEED = 42

    global XData
    XData = []

    global yData
    yData = []

    global ClassifierIDsList
    ClassifierIDsList = ''

    global algorithmList
    algorithmList = []

    # Initializing models

    global classifiersId
    classifiersId = []
    global classifiersIDwithFI
    classifiersIDwithFI = []
    global classifiersIDPlusParams
    classifiersIDPlusParams = [] 
    global classifierID
    classifierID = 0

    global RetrieveModelsList
    RetrieveModelsList = []

    global resultsList
    resultsList = []

    global allParametersPerformancePerModel
    allParametersPerformancePerModel = []

    global all_classifiers
    all_classifiers = []

    global crossValidation
    crossValidation = 3

    global scoring
    #scoring = {'accuracy': 'accuracy', 'f1_macro': 'f1_weighted', 'precision': 'precision_weighted', 'recall': 'recall_weighted', 'jaccard': 'jaccard_weighted', 'neg_log_loss': 'neg_log_loss', 'r2': 'r2', 'neg_mean_absolute_error': 'neg_mean_absolute_error', 'neg_mean_absolute_error': 'neg_mean_absolute_error'}
    scoring = {'accuracy': 'accuracy', 'f1_macro': 'f1_weighted', 'precision': 'precision_weighted', 'recall': 'recall_weighted', 'jaccard': 'jaccard_weighted'}

    global yPredictProb
    yPredictProb = []

    global loopFeatures
    loopFeatures = 2

    global columns 
    columns = []

    global results
    results = []

    global target_names
    target_names = []
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
    DataSetSelection()
    return 'Everything is okay'

# Sent data to client 
@app.route('/data/ClientRequest', methods=["GET", "POST"])
def CollectionData(): 
    json.dumps(DataResultsRaw)
    response = {
        'Collection': DataResultsRaw
    }
    return jsonify(response)

def DataSetSelection():  
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
            target_names.append(value)
        if (value == previous):
            AllTargetsFloatValues.append(Class)
        else:
            Class = Class + 1
            target_names.append(value)
            AllTargetsFloatValues.append(Class)
            previous = value

    ArrayDataResults = pd.DataFrame.from_dict(DataResults)

    global XData, yData, RANDOM_SEED
    XData, yData = ArrayDataResults, AllTargetsFloatValues
    warnings.simplefilter('ignore')
    return 'Everything is okay'

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

def column_index(df, query_cols):
    cols = df.columns.values
    sidx = np.argsort(cols)
    return sidx[np.searchsorted(cols,query_cols,sorter=sidx)].tolist()

global mem
mem = Memory("./cache_dir")

def GridSearch(clf, params, FI):
    global XData
    global yData
    global scoring
    global target_names
    grid = GridSearchCV(estimator=clf, 
                param_grid=params,
                scoring=scoring, 
                cv=crossValidation,
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
    PerClassMetrics = []
    FeatureImp = []
    PerFeatureAccuracy = []
    global subset
    global loopFeatures
    global yPredictProb
    global columns
    columns = []
    counter = 0
    subset = XData
    for i, eachClassifierParams in enumerate(grid.cv_results_['params']):
        eachClassifierParamsDictList = {}
        for key, value in eachClassifierParams.items():
            Listvalue = []
            Listvalue.append(value)
            eachClassifierParamsDictList[key] = Listvalue
            counter = counter + 1
        grid = GridSearchCV(estimator=clf, 
            param_grid=eachClassifierParamsDictList,
            scoring=scoring, 
            cv=crossValidation,
            refit='accuracy',
            n_jobs = -1)
        if (featureSelection['featureSelection'] == ''):
            subset = XData
        else:
            featureSelected = []
            for indices, each in enumerate(XData.columns):
                if (int(''.join(x for x in featureSelection['featureSelection'][loopFeatures] if x.isdigit())) == 1):
                    featureSelected.append(each)
                loopFeatures = loopFeatures + 3
            subset = XData[featureSelected]
            element = (column_index(XData, featureSelected))
            columns.append(element)
        grid.fit(subset, yData)   
        if (FI == 0):
            n_feats = XData.shape[1]
            for i in range(n_feats):
                scores = model_selection.cross_val_score(grid.best_estimator_, XData.values[:, i].reshape(-1, 1), yData, cv=crossValidation)
                PerFeatureAccuracy.append(scores.mean())

        yPredict = grid.predict(subset)
        yPredictProb.append(grid.predict_proba(subset))
        PerClassMetrics.append(classification_report(yData, yPredict, target_names=target_names, digits=2, output_dict=True))
        if (FI == 1):
            X = subset.values
            Y = array(yData)
            FeatureImp.append(class_feature_importance(X, Y, grid.best_estimator_.feature_importances_))

    FeatureImpPandas = pd.DataFrame(FeatureImp)
    PerClassMetricsPandas = pd.DataFrame(PerClassMetrics)
    PerFeatureAccuracyPandas = pd.DataFrame(PerFeatureAccuracy)
    return df_cv_results_classifiers, parameters, FeatureImpPandas, PerClassMetricsPandas, PerFeatureAccuracyPandas

def class_feature_importance(X, Y, feature_importances):
    N, M = X.shape
    X = scale(X)

    out = {}
    for c in set(Y):
        out[c] = dict(
            zip(range(N), np.mean(X[Y==c, :], axis=0)*feature_importances)
        )

    return out

#GridSearch = mem.cache(GridSearch)

def InitializeEnsemble(): 
    global resultsList 
    df_cv_results_classifiersList = []
    parametersList = []
    FeatureImportanceList = []
    PerClassMetricsList = []
    FeatureAccuracyList = []
    for j, result in enumerate(resultsList):
        df_cv_results_classifiersList.append(resultsList[j][0])
        parametersList.append(resultsList[j][1])
        FeatureImportanceList.append(resultsList[j][2])
        PerClassMetricsList.append(resultsList[j][3])
        FeatureAccuracyList.append(resultsList[j][4])

    df_cv_results_classifiers = pd.concat(df_cv_results_classifiersList, ignore_index=True, sort=False)
    parameters = pd.concat(parametersList, ignore_index=True, sort=False)
    FeatureImportance = pd.concat(FeatureImportanceList, ignore_index=True, sort=False)
    PerClassMetrics = pd.concat(PerClassMetricsList, ignore_index=True, sort=False)
    FeatureAccuracy = pd.concat(FeatureAccuracyList, ignore_index=True, sort=False)

    global scoring 
    NumberofscoringMetrics = len(scoring)

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

    mergedPredList = zip(*yPredictProb)
    mergedPredListListForm = []
    for el in mergedPredList:
        mergedPredListListForm.append(list(chain(*el)))
    XClassifiers = df_cv_results_classifiers_metrics
    
    PredictionSpace = FunTsne(mergedPredListListForm)
    DataSpace = FunTsne(XData)
    ModelSpace = FunMDS(XClassifiers)
    global ClassifierIDsList
    key = 0
    EnsembleModel(ClassifierIDsList, key)
    DataSpaceList = DataSpace.tolist()
    PredictionSpaceList = PredictionSpace.tolist()

    global Results

    Results = []
    FeatureImportance = FeatureImportance.to_json(orient='records')
    PerClassMetrics = PerClassMetrics.to_json(orient='records')
    FeatureAccuracy = FeatureAccuracy.to_json(orient='records')
    DataSpaceList = DataSpace.tolist()
    XDataJSON = XData.columns.tolist()
    Results.append(json.dumps(sumPerClassifier)) # Position: 0 
    Results.append(json.dumps(ModelSpace)) # Position: 1
    Results.append(json.dumps(classifiersIDPlusParams)) # Position: 2
    Results.append(FeatureImportance) # Position: 3
    Results.append(PerClassMetrics) # Position: 4
    Results.append(json.dumps(target_names)) # Position: 5 
    Results.append(FeatureAccuracy) # Position: 6
    Results.append(json.dumps(XDataJSON)) # Position: 7 
    Results.append(json.dumps(classifiersId)) # Position: 8
    Results.append(json.dumps(classifiersIDwithFI)) # Position: 9 
    Results.append(json.dumps(DataSpaceList)) # Position: 10
    Results.append(json.dumps(PredictionSpaceList)) # Position: 11 

    return Results



# Retrieve data from client 
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/ServerRequestSelPoin', methods=["GET", "POST"])
def RetrieveSelClassifiersID():
    global ClassifierIDsList
    ClassifierIDsList = request.get_data().decode('utf8').replace("'", '"')
    key = 1
    EnsembleModel(ClassifierIDsList, key)
    return 'Everything Okay'

# Retrieve data from client 
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/FeaturesSelection', methods=["GET", "POST"])
def FeatureSelPerModel():
    global featureSelection
    global loopFeatures
    global ClassifierIDsList
    RetrieveModelsPar = request.get_data().decode('utf8').replace("'", '"')
    RetrieveModelsPar = json.loads(RetrieveModelsPar)
    RetrieveModelsParRed = []
    print(RetrieveModelsPar['brushedAll']) # FIX THIS THING!!!!!
    for j, i in enumerate(RetrieveModelsPar['brushedAll']):
        print(j)
    RetrieveModelsParRed = [for j, i in enumerate(RetrieveModelsPar['brushedAll']) if j not in ClassifierIDsList]

    RetrieveModelsParPandas = pd.DataFrame(RetrieveModelsParRed)
    RetrieveModelsParPandas = RetrieveModelsParPandas.drop(columns=['performance'])
    RetrieveModelsParPandas = RetrieveModelsParPandas.to_dict(orient='list')
    print(RetrieveModelsParPandas)
    RetrieveModels = {}
    for key, value in RetrieveModelsParPandas.items():
        withoutDuplicates = Remove(value)
        RetrieveModels[key] = withoutDuplicates
    global RetrieveModelsListNew
    RetrieveModelsListNew.append(RetrieveModels)
    loopFeatures = 2
    featureSelection = request.get_data().decode('utf8').replace("'", '"')
    featureSelection = json.loads(featureSelection)
    global algorithmList
    results = []
    for index, eachalgor in enumerate(algorithmList):
        if (eachalgor == 'KNN'):
            clf = KNeighborsClassifier()
            params = RetrieveModelsListNew[index]
            IF = 0
            results.append(GridSearch(clf, params, IF))
            resultsList.append(results[0])
        else:
            clf = RandomForestClassifier()
            params = RetrieveModelsListNew[index]
            IF = 1
            results.append(GridSearch(clf, params, IF))
            resultsList.append(results[0])
    key = 2
    EnsembleModel(ClassifierIDsList, key)
    return 'Everything Okay'

def FunMDS (data):
    mds = MDS(n_components=2, random_state=RANDOM_SEED)
    XTransformed = mds.fit_transform(data).T
    XTransformed = XTransformed.tolist()
    return XTransformed

def FunTsne (data):
    tsne = TSNE(n_components=2).fit_transform(data)
    tsne.shape
    return tsne

def EnsembleModel (ClassifierIDsList, keyRetrieved): 

    global scores
    scores = []
    global all_classifiersSelection
    all_classifiersSelection = []  
    global columns

    global all_classifiers

    if (keyRetrieved == 0):
        columnsInit = []
        all_classifiers = []  
        columnsInit = [XData.columns.get_loc(c) for c in XData.columns if c in XData]
        for index, eachelem in enumerate(algorithmList):
            if (eachelem == 'KNN'):
                for each in resultsList[index][1]:
                    all_classifiers.append(make_pipeline(ColumnSelector(cols=columnsInit), KNeighborsClassifier().set_params(**each)))
            else:
                for each in resultsList[index][1]:
                    all_classifiers.append(make_pipeline(ColumnSelector(cols=columnsInit), RandomForestClassifier().set_params(**each)))

        lr = LogisticRegression()
        sclf = StackingCVClassifier(classifiers=all_classifiers,
                            use_probas=True,
                            meta_classifier=lr,
                            random_state=RANDOM_SEED,
                            n_jobs = -1)
    elif (keyRetrieved == 1):       
        ClassifierIDsList = json.loads(ClassifierIDsList)    
        for loop in ClassifierIDsList['ClassifiersList']:
            temp = [int(s) for s in re.findall(r'\b\d+\b', loop)]
            all_classifiersSelection.append(all_classifiers[temp[0]])

        lr = LogisticRegression()
        sclf = StackingCVClassifier(classifiers=all_classifiersSelection,
                            use_probas=True,
                            meta_classifier=lr,
                            random_state=RANDOM_SEED,
                            n_jobs = -1)
    else: 
        columnsReduce = columns.copy()
        lr = LogisticRegression()
        if (len(all_classifiersSelection) == 0):
            all_classifiers = []
            for index, eachelem in enumerate(algorithmList):
                if (eachelem == 'KNN'):
                    for j, each in enumerate(resultsList[index][1]):
                        all_classifiers.append(make_pipeline(ColumnSelector(cols=columnsReduce[j]), KNeighborsClassifier().set_params(**each)))
                    del columnsReduce[0:len(resultsList[index][1])]
                else:
                    for j, each in enumerate(resultsList[index][1]):
                        all_classifiers.append(make_pipeline(ColumnSelector(cols=columnsReduce[j]), RandomForestClassifier().set_params(**each)))
                    del columnsReduce[0:len(resultsList[index][1])]
            print(all_classifiers)
            sclf = StackingCVClassifier(classifiers=all_classifiers,
                                use_probas=True,
                                meta_classifier=lr,
                                random_state=RANDOM_SEED,
                                n_jobs = -1)
        else:
            for index, eachelem in enumerate(algorithmList):
                if (eachelem == 'KNN'):
                    print(resultsList[index][1])
                    for j, each in enumerate(resultsList[index][1]):
                        all_classifiersSelection.append(make_pipeline(ColumnSelector(cols=columnsReduce[j]), KNeighborsClassifier().set_params(**each)))
                    del columnsReduce[0:len(resultsList[index][1])]
                else:
                    for j, each in enumerate(resultsList[index][1]):
                        all_classifiersSelection.append(make_pipeline(ColumnSelector(cols=columnsReduce[j]), RandomForestClassifier().set_params(**each)))
                    del columnsReduce[0:len(resultsList[index][1])]
            print(all_classifiersSelection)
            sclf = StackingCVClassifier(classifiers=all_classifiersSelection,
                                use_probas=True,
                                meta_classifier=lr,
                                random_state=RANDOM_SEED,
                                n_jobs = -1)

    for clf, label in zip([sclf], 
                    ['StackingClassifier']):

        scores = model_selection.cross_val_score(clf, XData, yData, 
                                                cv=crossValidation, scoring='accuracy')



# Sending the final results to be visualized as a line plot
@app.route('/data/SendFinalResultsBacktoVisualize', methods=["GET", "POST"])
def SendToPlotFinalResults():
    FinalResults = []
    FinalResults.append(scores.mean())
    FinalResults.append(scores.std())
    response = {    
        'FinalResults': FinalResults
    }
    return jsonify(response)

# Sending the overview classifiers' results to be visualized as a scatterplot
@app.route('/data/PlotClassifiers', methods=["GET", "POST"])
def SendToPlot():
    while (len(DataResultsRaw) != DataRawLength):
        pass
    InitializeEnsemble()
    response = {    
        'OverviewResults': Results
    }
    return jsonify(response)

# Retrieve data from client 
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/ServerRequestSelParameters', methods=["GET", "POST"])
def RetrieveModel():
    global RetrievedModel
    RetrievedModel = request.get_data().decode('utf8').replace("'", '"')
    RetrievedModel = json.loads(RetrievedModel)
    global parametersPerformancePerModel
    parametersPerformancePerModel = []
    global algorithms 
    algorithms = RetrievedModel['Algorithms']
    for eachAlgor in algorithms:
        if (eachAlgor) == 'KNN':
            clf = KNeighborsClassifier()
            params = {'n_neighbors': list(range(1, 25)), 'weights': ['uniform', 'distance'], 'algorithm': ['brute', 'kd_tree', 'ball_tree'], 'metric': ['chebyshev', 'manhattan', 'euclidean', 'minkowski']}
        else: 
            clf = RandomForestClassifier()
            params = {'n_estimators': list(range(80, 120)), 'criterion': ['gini', 'entropy']}
        GridSearchForParameters(clf, params)
    SendEachClassifiersPerformanceToVisualize()
    return 'Everything Okay'

def GridSearchForParameters(clf, params):
    grid = GridSearchCV(estimator=clf, 
                param_grid=params,
                scoring='accuracy', 
                cv=crossValidation,
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

    global allParametersPerformancePerModel
    parametersPerformancePerModel = df_cv_results_classifiers[['mean_test_score','params']]
    parametersPerformancePerModel = parametersPerformancePerModel.to_json()
    allParametersPerformancePerModel.append(parametersPerformancePerModel)
    return 'Everything is okay'

#GridSearchForParameters = mem.cache(GridSearchForParameters)

# Sending each model's results
@app.route('/data/PerformanceForEachModel', methods=["GET", "POST"])
def SendEachClassifiersPerformanceToVisualize ():
    response = {    
        'PerformancePerModel': allParametersPerformancePerModel
    }
    return jsonify(response)

def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 

# Retrieve data from client 
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/SendBrushedParam', methods=["GET", "POST"])
def RetrieveModelsParam():
    RetrieveModelsPar = request.get_data().decode('utf8').replace("'", '"')
    RetrieveModelsPar = json.loads(RetrieveModelsPar)
    algorithm = RetrieveModelsPar['algorithm']
    RetrieveModelsParPandas = pd.DataFrame(RetrieveModelsPar['brushed'])
    RetrieveModelsParPandas = RetrieveModelsParPandas.drop(columns=['performance'])
    RetrieveModelsParPandas = RetrieveModelsParPandas.to_dict(orient='list')
    RetrieveModels = {}
    for key, value in RetrieveModelsParPandas.items():
        withoutDuplicates = Remove(value)
        RetrieveModels[key] = withoutDuplicates
    global RetrieveModelsList
    RetrieveModelsList.append(RetrieveModels)

    global classifierID
    global algorithmList
    results = []
    algorithmList.append(algorithm)
    if (algorithm == 'KNN'):
        clf = KNeighborsClassifier()
        params = RetrieveModels
        IF = 0
        results.append(GridSearch(clf, params, IF))
        resultsList.append(results[0])
        for j, oneClassifier in enumerate(results[0][1]): 
            classifiersId.append(classifierID)
            classifiersIDPlusParams.append(classifierID)
            classifierID = classifierID + 1
    else:
        clf = RandomForestClassifier()
        params = RetrieveModels
        IF = 1
        results.append(GridSearch(clf, params, IF))
        resultsList.append(results[0])
        for oneClassifier, j in enumerate(results[0][1]): 
            classifiersIDPlusParams.append(classifierID)
            classifiersIDwithFI.append(classifierID)
            classifierID = classifierID + 1
    return 'Everything Okay'

    