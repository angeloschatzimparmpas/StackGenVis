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
import ast

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
import eli5
from eli5.sklearn import PermutationImportance
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import RFE
from sklearn.decomposition import PCA

from mlxtend.classifier import StackingCVClassifier
from mlxtend.feature_selection import ColumnSelector

from skdist.distribute.search import DistGridSearchCV
from pyspark.sql import SparkSession

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
    
    global detailsParams
    detailsParams = []

    global algorithmList
    algorithmList = []

    global ClassifierIDsList
    ClassifierIDsList = ''

    # Initializing models

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

# Retrieve data from client and select the correct data set
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/ServerRequest', methods=["GET", "POST"])
def RetrieveFileName():

    fileName = request.get_data().decode('utf8').replace("'", '"')

    #global featureSelection 
    #featureSelection = request.get_data().decode('utf8').replace("'", '"')
    #featureSelection = json.loads(featureSelection)

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

    global detailsParams
    detailsParams = []

    # Initializing models

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
    scoring = {'accuracy': 'accuracy', 'f1_macro': 'f1_weighted', 'precision': 'precision_weighted', 'recall': 'recall_weighted', 'jaccard': 'jaccard_weighted'}
    #scoring = {'accuracy': 'accuracy', 'f1_macro': 'f1_weighted', 'precision': 'precision_weighted', 'recall': 'recall_weighted', 'jaccard': 'jaccard_weighted', 'neg_log_loss': 'neg_log_loss', 'r2': 'r2', 'neg_mean_absolute_error': 'neg_mean_absolute_error', 'neg_mean_absolute_error': 'neg_mean_absolute_error'}

    global NumberofscoringMetrics
    NumberofscoringMetrics = len(scoring)

    global yPredictProb
    yPredictProb = []

    global loopFeatures
    loopFeatures = 2

    global factors
    factors = [1,1,1,1,1]

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

def Preprocessing():
    global resultsList 
    df_cv_results_classifiersList = []
    parametersList = []
    PerClassMetricsList = []
    FeatureAccuracyList = []
    perm_imp_eli5PD = []
    featureScores = []
    for j, result in enumerate(resultsList):
        df_cv_results_classifiersList.append(resultsList[j][0])
        parametersList.append(resultsList[j][1])
        PerClassMetricsList.append(resultsList[j][2])
        FeatureAccuracyList.append(resultsList[j][3])
        perm_imp_eli5PD.append(resultsList[j][4])
        featureScores.append(resultsList[j][5])

    df_cv_results_classifiers = pd.concat(df_cv_results_classifiersList, ignore_index=True, sort=False)
    parameters = pd.concat(parametersList, ignore_index=True, sort=False)
    #FeatureImportanceListPD = pd.concat(FeatureImportanceList, ignore_index=True, sort=False)
    PerClassMetrics = pd.concat(PerClassMetricsList, ignore_index=True, sort=False)
    FeatureAccuracy = pd.concat(FeatureAccuracyList, ignore_index=True, sort=False)
    #RFEListPDCon = pd.concat(RFEListPD, ignore_index=True, sort=False)
    #perm_imp_rfpimpCon = pd.concat(perm_imp_rfpimp, ignore_index=True, sort=False)
    perm_imp_eli5PDCon = pd.concat(perm_imp_eli5PD, ignore_index=True, sort=False)
    featureScoresCon = pd.concat(featureScores, ignore_index=True, sort=False)
    global factors
    factors = [1,1,1,1,1,1]
    global df_cv_results_classifiers_metrics
    df_cv_results_classifiers_metrics = df_cv_results_classifiers.copy()
    df_cv_results_classifiers_metrics = df_cv_results_classifiers_metrics.filter(['mean_test_accuracy','mean_test_f1_macro','mean_test_precision','mean_test_recall','mean_test_jaccard'])
    return [parameters,PerClassMetrics,FeatureAccuracy,df_cv_results_classifiers_metrics,perm_imp_eli5PDCon,featureScoresCon]

def sumPerMetric(factors):
    sumPerClassifier = []
    preProcessResults = []
    preProcessResults = Preprocessing()
    loopThroughMetrics = preProcessResults[3]
    global scoring
    global metricsPerModel
    metricsPerModel = []
    metricsPerModel.append(loopThroughMetrics['mean_test_accuracy'].sum()/loopThroughMetrics['mean_test_accuracy'].count())
    metricsPerModel.append(loopThroughMetrics['mean_test_f1_macro'].sum()/loopThroughMetrics['mean_test_f1_macro'].count())
    metricsPerModel.append(loopThroughMetrics['mean_test_precision'].sum()/loopThroughMetrics['mean_test_precision'].count())
    metricsPerModel.append(loopThroughMetrics['mean_test_recall'].sum()/loopThroughMetrics['mean_test_recall'].count())
    metricsPerModel.append(loopThroughMetrics['mean_test_jaccard'].sum()/loopThroughMetrics['mean_test_jaccard'].count())
    for row in loopThroughMetrics.iterrows():
        rowSum = 0
        lengthFactors = len(scoring)
        for loop,elements in enumerate(row):
            lengthFactors = lengthFactors -  1 + factors[loop]
            rowSum = elements*factors[loop] + rowSum
        if lengthFactors is 0:
            sumPerClassifier = 0
        else:
            sumPerClassifier.append(rowSum/lengthFactors)
    return sumPerClassifier

# Retrieve data from client 
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/factors', methods=["GET", "POST"])
def RetrieveFactors():
    Factors = request.get_data().decode('utf8').replace("'", '"')
    FactorsInt = json.loads(Factors)
    global sumPerClassifierSel
    global ModelSpaceMDSNew
    global ModelSpaceTSNENew
    sumPerClassifierSel = []
    sumPerClassifierSel = sumPerMetric(FactorsInt['Factors'])
    ModelSpaceMDSNew = []
    ModelSpaceTSNENew = []
    preProcessResults = []
    preProcessResults = Preprocessing()
    XClassifiers = preProcessResults[3]
    flagLocal = 0
    countRemovals = 0
    for l,el in enumerate(FactorsInt['Factors']):
        if el is 0:
            XClassifiers.drop(XClassifiers.columns[[l-countRemovals]], axis=1, inplace=True)
            countRemovals = countRemovals + 1
            flagLocal = 1
    if flagLocal is 1:
        ModelSpaceMDSNew = FunMDS(XClassifiers)
        ModelSpaceTSNENew = FunTsne(XClassifiers)
        ModelSpaceTSNENew = ModelSpaceTSNENew.tolist()
    return 'Everything Okay'

@app.route('/data/UpdateOverv', methods=["GET", "POST"])
def UpdateOverview():
    global sumPerClassifierSel
    global ModelSpaceMDSNew
    global ModelSpaceTSNENew
    global metricsPerModel
    ResultsUpdateOverview = []
    ResultsUpdateOverview.append(sumPerClassifierSel)
    ResultsUpdateOverview.append(ModelSpaceMDSNew)
    ResultsUpdateOverview.append(ModelSpaceTSNENew)
    ResultsUpdateOverview.append(metricsPerModel)
    response = {    
        'Results': ResultsUpdateOverview
    }
    return jsonify(response)

def InitializeEnsemble(): 
    preProcessResults = []
    preProcessResults = Preprocessing()
    sumPerClassifier = sumPerMetric(factors)
    mergedPredList = zip(*yPredictProb)
    mergedPredListListForm = []
    for el in mergedPredList:
        mergedPredListListForm.append(list(chain(*el)))
    XClassifiers = preProcessResults[3]
    PredictionSpace = FunTsne(mergedPredListListForm)
    DataSpace = FunTsne(XData)
    ModelSpaceMDS = FunMDS(XClassifiers)
    ModelSpaceTSNE = FunTsne(XClassifiers)
    ModelSpaceTSNE = ModelSpaceTSNE.tolist()
    global ClassifierIDsList
    key = 0
    EnsembleModel(ClassifierIDsList, key)
    PredictionSpaceList = PredictionSpace.tolist()
    DataSpaceList = DataSpace.tolist()
    ReturnResults(sumPerClassifier,ModelSpaceMDS,ModelSpaceTSNE,preProcessResults,DataSpaceList,PredictionSpaceList)

def ReturnResults(sumPerClassifier,ModelSpaceMDS,ModelSpaceTSNE,preProcessResults,DataSpaceList,PredictionSpaceList):
    global Results
    Results = []
    parametersGen = preProcessResults[0]
    PerClassMetrics = preProcessResults[1]
    FeatureAccuracy = preProcessResults[2]
    perm_imp_eli5PDCon = preProcessResults[4]
    featureScoresCon = preProcessResults[5]
    parametersGenPD = parametersGen.to_json(orient='records')
    PerClassMetrics = PerClassMetrics.to_json(orient='records')
    FeatureAccuracy = FeatureAccuracy.to_json(orient='records')
    perm_imp_eli5PDCon = perm_imp_eli5PDCon.to_json(orient='records')
    featureScoresCon = featureScoresCon.to_json(orient='records')
    XDataJSON = XData.columns.tolist()
    global metricsPerModel
    Results.append(json.dumps(sumPerClassifier)) # Position: 0 
    Results.append(json.dumps(ModelSpaceMDS)) # Position: 1
    Results.append(json.dumps(parametersGenPD)) # Position: 2
    Results.append(PerClassMetrics) # Position: 3
    Results.append(json.dumps(target_names)) # Position: 4 
    Results.append(FeatureAccuracy) # Position: 5
    Results.append(json.dumps(XDataJSON)) # Position: 6 
    Results.append(json.dumps(DataSpaceList)) # Position: 7
    Results.append(json.dumps(PredictionSpaceList)) # Position: 8 
    Results.append(json.dumps(metricsPerModel)) # Position: 9
    Results.append(perm_imp_eli5PDCon) # Position: 10
    Results.append(featureScoresCon) # Position: 11
    Results.append(json.dumps(ModelSpaceTSNE)) # Position: 12
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
    global ClassifierIDsList
    featureSelection = request.get_data().decode('utf8').replace("'", '"')
    featureSelection = json.loads(featureSelection)
    global detailsParams
    global algorithmList
    results = []
    global resultsList
    resultsList = []
    global loopFeatures
    loopFeatures = 2

    algorithmsWithoutDuplicates = list(dict.fromkeys(algorithmList))
    for index, eachalgor in enumerate(algorithmsWithoutDuplicates):
        if (eachalgor == 'KNN'):
            clf = KNeighborsClassifier()
            params = detailsParams[index]
            results.append(GridSearch(clf, params))
            resultsList.append(results[0])
        else:
            clf = RandomForestClassifier()
            params =  detailsParams[index]
            results.append(GridSearch(clf, params))
            resultsList.append(results[0])
    if (featureSelection['featureSelection'] == ''):
        key = 0
    else:
        key = 2
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
    global algorithmList

    algorithmsWithoutDuplicates = list(dict.fromkeys(algorithmList))
    if (keyRetrieved == 0):
        columnsInit = []
        all_classifiers = []  
        columnsInit = [XData.columns.get_loc(c) for c in XData.columns if c in XData]

        for index, eachelem in enumerate(algorithmsWithoutDuplicates):
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
            for index, eachelem in enumerate(algorithmsWithoutDuplicates):
                if (eachelem == 'KNN'):
                    for j, each in enumerate(resultsList[index][1]):
                        all_classifiers.append(make_pipeline(ColumnSelector(cols=columnsReduce[j]), KNeighborsClassifier().set_params(**each)))
                    del columnsReduce[0:len(resultsList[index][1])]
                else:
                    for j, each in enumerate(resultsList[index][1]):
                        all_classifiers.append(make_pipeline(ColumnSelector(cols=columnsReduce[j]), RandomForestClassifier().set_params(**each)))
                    del columnsReduce[0:len(resultsList[index][1])]
            sclf = StackingCVClassifier(classifiers=all_classifiers,
                                use_probas=True,
                                meta_classifier=lr,
                                random_state=RANDOM_SEED,
                                n_jobs = -1)
        else:
            for index, eachelem in enumerate(algorithmsWithoutDuplicates):
                if (eachelem == 'KNN'):
                    for j, each in enumerate(resultsList[index][1]):
                        all_classifiersSelection.append(make_pipeline(ColumnSelector(cols=columnsReduce[j]), KNeighborsClassifier().set_params(**each)))
                    del columnsReduce[0:len(resultsList[index][1])]
                else:
                    for j, each in enumerate(resultsList[index][1]):
                        all_classifiersSelection.append(make_pipeline(ColumnSelector(cols=columnsReduce[j]), RandomForestClassifier().set_params(**each)))
                    del columnsReduce[0:len(resultsList[index][1])]
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

# Initialize every model for each algorithm
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/ServerRequestSelParameters', methods=["GET", "POST"])
def RetrieveModel():

    # get the models from the frontend
    RetrievedModel = request.get_data().decode('utf8').replace("'", '"')
    RetrievedModel = json.loads(RetrievedModel)

    algorithms = RetrievedModel['Algorithms']

    # loop through the algorithms
    global allParametersPerformancePerModel
    for eachAlgor in algorithms:
        if (eachAlgor) == 'KNN':
            clf = KNeighborsClassifier()
            params = {'n_neighbors': list(range(1, 25)), 'weights': ['uniform', 'distance'], 'algorithm': ['brute', 'kd_tree', 'ball_tree'], 'metric': ['chebyshev', 'manhattan', 'euclidean', 'minkowski']}
            AlgorithmsIDsEnd = 0
        else: 
            clf = RandomForestClassifier()
            params = {'n_estimators': list(range(80, 120)), 'criterion': ['gini', 'entropy']}
            AlgorithmsIDsEnd = 576
        allParametersPerformancePerModel = GridSearchForModels(clf, params, eachAlgor, factors, AlgorithmsIDsEnd)

    # call the function that sends the results to the frontend 
    SendEachClassifiersPerformanceToVisualize()

    return 'Everything Okay'

location = './cachedir'
memory = Memory(location, verbose=0)

# calculating for all algorithms and models the performance and other results
@memory.cache
def GridSearchForModels(clf, params, eachAlgor, factors, AlgorithmsIDsEnd):

    # instantiate spark session
    spark = (   
        SparkSession    
        .builder    
        .getOrCreate()    
        )
    sc = spark.sparkContext 

    # this is the grid we use to train the models
    grid = DistGridSearchCV(    
        estimator=clf, param_grid=params,     
        sc=sc, cv=crossValidation, refit='accuracy', scoring=scoring,
        verbose=0, n_jobs=-1)

    # fit and extract the probabilities
    grid.fit(XData, yData)

    # process the results
    cv_results = []
    cv_results.append(grid.cv_results_)
    df_cv_results = pd.DataFrame.from_dict(cv_results)

    # number of models stored
    number_of_models = len(df_cv_results.iloc[0][0])

    # initialize results per row
    df_cv_results_per_row = []

    # loop through number of models
    modelsIDs = []
    for i in range(number_of_models):
        modelsIDs.append(AlgorithmsIDsEnd+i)
         # initialize results per item
        df_cv_results_per_item = []
        for column in df_cv_results.iloc[0]:
            df_cv_results_per_item.append(column[i])
        df_cv_results_per_row.append(df_cv_results_per_item)

    # store the results into a pandas dataframe
    df_cv_results_classifiers = pd.DataFrame(data = df_cv_results_per_row, columns= df_cv_results.columns)

    # copy and filter in order to get only the metrics
    metrics = df_cv_results_classifiers.copy()
    metrics = metrics.filter(['mean_test_accuracy','mean_test_f1_macro','mean_test_precision','mean_test_recall','mean_test_jaccard']) 

    # control the factors
    sumperModel = []
    for index, row in metrics.iterrows():
        rowSum = 0
        lengthFactors = NumberofscoringMetrics
        for loop,elements in enumerate(row):
            lengthFactors = lengthFactors -  1 + factors[loop]
            rowSum = elements*factors[loop] + rowSum
        if lengthFactors is 0:
            sumperModel = 0
        else:
            sumperModel.append(rowSum/lengthFactors)
    
    # summarize all models metrics
    summarizedMetrics = pd.DataFrame(sumperModel)
    summarizedMetrics.rename(columns={0:'sum'})

    # concat parameters and performance
    parameters = pd.DataFrame(df_cv_results_classifiers['params'])
    parametersPerformancePerModel = pd.concat([summarizedMetrics, parameters], axis=1)
    parametersPerformancePerModel = parametersPerformancePerModel.to_json()
    
    parametersLocal = json.loads(parametersPerformancePerModel)['params'].copy()
    Models = []
    for index, items in enumerate(parametersLocal):
        Models.append(str(index))

    parametersLocalNew = [ parametersLocal[your_key] for your_key in Models ]

    permList = []
    PerFeatureAccuracy = []
    PerClassMetric = []

    for eachModelParameters in parametersLocalNew:
        clf.set_params(**eachModelParameters)

        perm = PermutationImportance(clf, cv = None, refit = True, n_iter = 25).fit(XData, yData)
        permList.append(perm.feature_importances_)

        n_feats = XData.shape[1]
        for i in range(n_feats):
            scores = model_selection.cross_val_score(clf, XData.values[:, i].reshape(-1, 1), yData, cv=crossValidation)
            PerFeatureAccuracy.append(scores.mean())

        clf.fit(XData, yData) 
        yPredict = clf.predict(XData)
        # retrieve target names (class names)
        PerClassMetric.append(classification_report(yData, yPredict, target_names=target_names, digits=2, output_dict=True))

    PerClassMetricPandas = pd.DataFrame(PerClassMetric)  
    del PerClassMetricPandas['accuracy']  
    del PerClassMetricPandas['macro avg']  
    del PerClassMetricPandas['weighted avg']  
    PerClassMetricPandas = PerClassMetricPandas.to_json()


    perm_imp_eli5PD = pd.DataFrame(permList)
    perm_imp_eli5PD = perm_imp_eli5PD.to_json()

    PerFeatureAccuracyPandas = pd.DataFrame(PerFeatureAccuracy)
    PerFeatureAccuracyPandas = PerFeatureAccuracyPandas.to_json()

    bestfeatures = SelectKBest(score_func=chi2, k='all')
    fit = bestfeatures.fit(XData,yData)
    dfscores = pd.DataFrame(fit.scores_)
    dfcolumns = pd.DataFrame(XData.columns)
    featureScores = pd.concat([dfcolumns,dfscores],axis=1)
    featureScores.columns = ['Specs','Score']  #naming the dataframe columns
    featureScores = featureScores.to_json()

    # gather the results and send them back
    results.append(modelsIDs) # Position: 0 and so on
    results.append(parametersPerformancePerModel) # Position: 1 and so on
    results.append(PerClassMetricPandas) # Position: 2 and so on
    results.append(PerFeatureAccuracyPandas) # Position: 3 and so on
    results.append(perm_imp_eli5PD) # Position: 4 and so on
    results.append(featureScores) # Position: 5 and so on

    return results

# Sending each model's results to frontend
@app.route('/data/PerformanceForEachModel', methods=["GET", "POST"])
def SendEachClassifiersPerformanceToVisualize():
    response = {    
        'PerformancePerModel': allParametersPerformancePerModel,
    }
    return jsonify(response)

def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            if (isinstance(num, float)):
                if np.isnan(num):
                    pass
                else:
                    final_list.append(int(num)) 
            else:
                final_list.append(num) 
    return final_list 

# Retrieve data from client 
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/SendBrushedParam', methods=["GET", "POST"])
def RetrieveModelsParam():
    RetrieveModelsPar = request.get_data().decode('utf8').replace("'", '"')
    RetrieveModelsPar = json.loads(RetrieveModelsPar)
    
    global algorithmList
    algorithmList = RetrieveModelsPar['algorithms']
    count = []
    if ('KNN' in algorithmList):
        count.append('KNN')
    if ('RF' in algorithmList):
        count.append('RF')

    global detailsParams
    results = []
    counter1 = 0
    counter2 = 0
    KNNModels = []
    RFModels = []
    parametersLocalKNN = json.loads(allParametersPerformancePerModel[1])['params'].copy()
    your_key = '496'
    parametersLocalRF = json.loads(allParametersPerformancePerModel[4])['params'].copy()
    for index, items in enumerate(algorithmList):
        if (items == 'KNN'):
            counter1 = counter1 + 1
            KNNModels.append(RetrieveModelsPar['models'][index])
        else:
            counter2 = counter2 + 1
            RFModels.append(str(int(RetrieveModelsPar['models'][index])-576))

    parametersLocalKNNNew = [ parametersLocalKNN[your_key] for your_key in KNNModels ]
    parametersLocalRFNew = [ parametersLocalRF[your_key] for your_key in RFModels ]

    #output = pd.DataFrame()
    #print(RetrieveModelsPar['models'])
    #for d in RetrieveModelsPar['parameters']:  
    #    output = output.append(json.loads(d), ignore_index=True)
    #RetrieveModelsPandSel = output.loc[0:counter1,:]
    #RetrieveModelsPandSel2 = output.loc[counter1:counter1+counter2,:]
    #RetrieveModelsPandSelDic = RetrieveModelsPandSel.to_dict(orient='list')
    #RetrieveModelsPandSelDic2 = RetrieveModelsPandSel2.to_dict(orient='list')
    #print(RetrieveModelsPandSelDic)
    #RetrieveModels = {}
    #for key, value in RetrieveModelsPandSelDic.items():
    #    withoutDuplicates = Remove(value)
    #    RetrieveModels[key] = withoutDuplicates

    #RetrieveModels2 = {}
    #for key, value in RetrieveModelsPandSelDic2.items():
    #    withoutDuplicates = Remove(value)
    #    RetrieveModels2[key] = withoutDuplicates
    global resultsList
    resultsList = []
    for alg in count:
        if (alg == 'KNN'):
            clf = KNeighborsClassifier()
            #params = RetrieveModels
            #detailsParams.append(params)
            results.append(GridSearch(clf, parametersLocalKNNNew))
            resultsList.append(results[0])
        elif (alg == 'RF'):
            clf = RandomForestClassifier()
            #params = RetrieveModels2
            #detailsParams.append(params)
            results.append(GridSearch(clf, parametersLocalRFNew))
            resultsList.append(results[0])
        else:
            pass
    return 'Everything Okay'