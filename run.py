from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

import json
import collections
import numpy as np
import re
from numpy import array
from statistics import mode
import pandas as pd  
import warnings
import copy
from joblib import Memory
from itertools import chain
import ast

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from yellowbrick.regressor import CooksDistance
from sklearn.naive_bayes import GaussianNB 
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn import model_selection
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

from scipy.spatial import procrustes

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

    global factors
    factors = [1,1,1,1,1]

    global restoreClicked 
    restoreClicked = False

    global XData
    XData = []

    global yData
    yData = []

    global XDataStored
    XDataStored = []

    global yDataStored
    yDataStored = []
    
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
    
    global loopFeatures
    loopFeatures = 2

    global results
    results = []

    global resultsMetrics
    resultsMetrics = []

    global parametersSelData
    parametersSelData = []

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

    global restoreClicked 
    restoreClicked = False

    global RANDOM_SEED
    RANDOM_SEED = 42

    global XData
    XData = []

    global yData
    yData = []

    global XDataStored
    XDataStored = []

    global yDataStored
    yDataStored = []

    global filterDataFinal
    filterDataFinal = 'mean'

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

    global loopFeatures
    loopFeatures = 2

    global factors
    factors = [1,1,1,1,1]

    global results
    results = []

    global resultsMetrics
    resultsMetrics = []

    global parametersSelData
    parametersSelData = []

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
    
    dataBefore = copy.deepcopy(DataResults)

    for dictionary in DataResults:
        del dictionary['_id']
        del dictionary['InstanceID']
        del dictionary[target]

    global AllTargets
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

    global XDataStored, yDataStored
    XDataStored = XData.copy()
    yDataStored = yData.copy()

    DataSpaceRes = FunTsne(XData)
    DataSpaceListRes = DataSpaceRes.tolist()

    XDataJSONEntireSetRes = XData.to_json(orient='records')

    global preResults 
    preResults = []

    preResults.append(json.dumps(target_names)) # Position: 0
    preResults.append(json.dumps(DataSpaceListRes)) # Position: 1
    preResults.append(json.dumps(XDataJSONEntireSetRes)) # Position: 2
    preResults.append(json.dumps(yData)) # Position: 3
    preResults.append(json.dumps(AllTargets)) # Position: 4
    preResults.append(json.dumps(dataBefore)) # Position: 5
    preResults.append(json.dumps(target)) # Position: 6

    warnings.simplefilter('ignore')
    return 'Everything is okay'

# Sending each model's results to frontend
@app.route('/data/requestDataSpaceResults', methods=["GET", "POST"])
def SendDataSpaceResults():
    global preResults

    response = {    
        'preDataResults': preResults,
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

# Initialize every model for each algorithm
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/ServerRequestSelParameters', methods=["GET", "POST"])
def RetrieveModel():

    # get the models from the frontend
    RetrievedModel = request.get_data().decode('utf8').replace("'", '"')
    RetrievedModel = json.loads(RetrievedModel)

    global algorithms
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
            params = {'n_estimators': list(range(40, 120)), 'criterion': ['gini', 'entropy']}
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
    PerFeatureAccuracyAll = []
    PerClassMetric = []
    perModelProb = []

    for eachModelParameters in parametersLocalNew:
        clf.set_params(**eachModelParameters)

        perm = PermutationImportance(clf, cv = None, refit = True, n_iter = 25).fit(XData, yData)
        permList.append(perm.feature_importances_)

        n_feats = XData.shape[1]
        PerFeatureAccuracy = []
        for i in range(n_feats):
            scores = model_selection.cross_val_score(clf, XData.values[:, i].reshape(-1, 1), yData, cv=crossValidation)
            PerFeatureAccuracy.append(scores.mean())
        PerFeatureAccuracyAll.append(PerFeatureAccuracy)
        clf.fit(XData, yData) 
        yPredict = clf.predict(XData)
        # retrieve target names (class names)
        PerClassMetric.append(classification_report(yData, yPredict, target_names=target_names, digits=2, output_dict=True))
        yPredictProb = clf.predict_proba(XData)
        perModelProb.append(yPredictProb.tolist())

    perModelProbPandas = pd.DataFrame(perModelProb)
    perModelProbPandas = perModelProbPandas.to_json()

    PerClassMetricPandas = pd.DataFrame(PerClassMetric)  
    del PerClassMetricPandas['accuracy']  
    del PerClassMetricPandas['macro avg']  
    del PerClassMetricPandas['weighted avg']  
    PerClassMetricPandas = PerClassMetricPandas.to_json()


    perm_imp_eli5PD = pd.DataFrame(permList)
    perm_imp_eli5PD = perm_imp_eli5PD.to_json()

    PerFeatureAccuracyPandas = pd.DataFrame(PerFeatureAccuracyAll)
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
    metrics = metrics.to_json()
    results.append(metrics) # Position: 6 and so on
    results.append(perModelProbPandas) # Position: 7 and so on

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

    counter1 = 0
    counter2 = 0
    global KNNModels
    KNNModels = []
    global RFModels
    RFModels = []
    global algorithmsList
    algorithmsList = RetrieveModelsPar['algorithms']

    for index, items in enumerate(algorithmsList):
        if (items == 'KNN'):
            counter1 = counter1 + 1
            KNNModels.append(int(RetrieveModelsPar['models'][index]))
        else:
            counter2 = counter2 + 1
            RFModels.append(int(RetrieveModelsPar['models'][index]))

    return 'Everything Okay'

# Retrieve data from client 
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/factors', methods=["GET", "POST"])
def RetrieveFactors():
    Factors = request.get_data().decode('utf8').replace("'", '"')
    FactorsInt = json.loads(Factors)
    factors = FactorsInt['Factors']

    global sumPerClassifierSel
    global ModelSpaceMDSNew
    global ModelSpaceTSNENew
    global metricsPerModel
    sumPerClassifierSel = []
    sumPerClassifierSel = preProcsumPerMetric(factors)
    ModelSpaceMDSNew = []
    ModelSpaceTSNENew = []
    loopThroughMetrics = PreprocessingMetrics()
    metricsPerModel = preProcMetricsAllAndSel()
    flagLocal = 0
    countRemovals = 0
    for l,el in enumerate(factors):
        if el is 0:
            loopThroughMetrics.drop(loopThroughMetrics.columns[[l-countRemovals]], axis=1, inplace=True)
            countRemovals = countRemovals + 1
            flagLocal = 1
    if flagLocal is 1:
        ModelSpaceMDSNew = FunMDS(loopThroughMetrics)
        ModelSpaceTSNENew = FunTsne(loopThroughMetrics)
        ModelSpaceTSNENew = ModelSpaceTSNENew.tolist()
    return 'Everything Okay'

@app.route('/data/UpdateOverv', methods=["GET", "POST"])
def UpdateOverview():
    ResultsUpdateOverview = []
    ResultsUpdateOverview.append(sumPerClassifierSel)
    ResultsUpdateOverview.append(ModelSpaceMDSNew)
    ResultsUpdateOverview.append(ModelSpaceTSNENew)
    ResultsUpdateOverview.append(metricsPerModel)
    response = {    
        'Results': ResultsUpdateOverview
    }
    return jsonify(response)

def PreprocessingMetrics():
    dicKNN = json.loads(allParametersPerformancePerModel[6])
    dicRF = json.loads(allParametersPerformancePerModel[14])
    dfKNN = pd.DataFrame.from_dict(dicKNN)
    dfKNN.index = dfKNN.index.astype(int)
    dfKNNFiltered = dfKNN.loc[KNNModels, :]
    dfRF = pd.DataFrame.from_dict(dicRF)
    dfRF.index = dfRF.index.astype(int) + 576
    dfRFFiltered = dfRF.loc[RFModels, :]
    df_concatMetrics = pd.concat([dfKNNFiltered, dfRFFiltered])
    return df_concatMetrics

def PreprocessingPred():
    dicKNN = json.loads(allParametersPerformancePerModel[7])
    dicRF = json.loads(allParametersPerformancePerModel[15])
    dfKNN = pd.DataFrame.from_dict(dicKNN)
    dfKNN.index = dfKNN.index.astype(int)
    dfKNNFiltered = dfKNN.loc[KNNModels, :]
    dfRF = pd.DataFrame.from_dict(dicRF)
    dfRF.index = dfRF.index.astype(int) + 576
    dfRFFiltered = dfRF.loc[RFModels, :]
    df_concatProbs = pd.concat([dfKNNFiltered, dfRFFiltered])
    predictions = []
    for column, content in df_concatProbs.items():
        el = [sum(x)/len(x) for x in zip(*content)]
        predictions.append(el)
    return predictions

def PreprocessingPredUpdate(Models):
    Models = json.loads(Models)
    ModelsList= []
    for loop in Models['ClassifiersList']:
        temp = [int(s) for s in re.findall(r'\b\d+\b', loop)]
        ModelsList.append(temp[0])
    dicKNN = json.loads(allParametersPerformancePerModel[7])
    dicRF = json.loads(allParametersPerformancePerModel[15])
    dfKNN = pd.DataFrame.from_dict(dicKNN)
    dfKNN.index = dfKNN.index.astype(int)
    dfKNNFiltered = dfKNN.loc[KNNModels, :]
    dfRF = pd.DataFrame.from_dict(dicRF)
    dfRF.index = dfRF.index.astype(int) + 576
    dfRFFiltered = dfRF.loc[RFModels, :]
    df_concatProbs = pd.concat([dfKNNFiltered, dfRFFiltered])
    listProbs = df_concatProbs.index.values.tolist()
    deletedElements = 0
    for index, element in enumerate(listProbs):
        if element in ModelsList:
            index = index - deletedElements
            df_concatProbs = df_concatProbs.drop(df_concatProbs.index[index])
            deletedElements = deletedElements + 1
    df_concatProbsCleared = df_concatProbs
    listIDsRemaining = df_concatProbsCleared.index.values.tolist()

    predictionsAll = PreprocessingPred()
    PredictionSpaceAll = FunTsne(predictionsAll)

    predictionsSel = []
    for column, content in df_concatProbsCleared.items():
        el = [sum(x)/len(x) for x in zip(*content)]
        predictionsSel.append(el)

    PredictionSpaceSel = FunTsne(predictionsSel)

    #ModelSpaceMDSNewComb = [list(a) for a in  zip(PredictionSpaceAll[0], ModelSpaceMDS[1])]

    #ModelSpaceMDSNewSel = FunMDS(df_concatMetrics)
    #ModelSpaceMDSNewSelComb = [list(a) for a in  zip(ModelSpaceMDSNewSel[0], ModelSpaceMDSNewSel[1])]

    mtx2PredFinal = []
    mtx1Pred, mtx2Pred, disparity2 = procrustes(PredictionSpaceAll, PredictionSpaceSel)

    a1, b1 = zip(*mtx2Pred)
    mtx2PredFinal.append(a1)
    mtx2PredFinal.append(b1)
    return [mtx2PredFinal,listIDsRemaining]

def PreprocessingParam():
    dicKNN = json.loads(allParametersPerformancePerModel[1])
    dicRF = json.loads(allParametersPerformancePerModel[9])
    dicKNN = dicKNN['params']
    dicRF = dicRF['params']
    dfKNN = pd.DataFrame.from_dict(dicKNN)
    dfKNN = dfKNN.T
    dfKNN.index = dfKNN.index.astype(int)
    dfKNNFiltered = dfKNN.loc[KNNModels, :]
    dfRF = pd.DataFrame.from_dict(dicRF)
    dfRF = dfRF.T
    dfRF.index = dfRF.index.astype(int) + 576
    dfRFFiltered = dfRF.loc[RFModels, :]
    df_params = pd.concat([dfKNNFiltered, dfRFFiltered])
    return df_params

def PreprocessingParamSep():
    dicKNN = json.loads(allParametersPerformancePerModel[1])
    dicRF = json.loads(allParametersPerformancePerModel[9])
    dicKNN = dicKNN['params']
    dicRF = dicRF['params']
    dfKNN = pd.DataFrame.from_dict(dicKNN)
    dfKNN = dfKNN.T
    dfKNN.index = dfKNN.index.astype(int)
    dfKNNFiltered = dfKNN.loc[KNNModels, :]
    dfRF = pd.DataFrame.from_dict(dicRF)
    dfRF = dfRF.T
    dfRF.index = dfRF.index.astype(int) + 576
    dfRFFiltered = dfRF.loc[RFModels, :]
    return [dfKNNFiltered,dfRFFiltered]

def preProcessPerClassM():
    dicKNN = json.loads(allParametersPerformancePerModel[2])
    dicRF = json.loads(allParametersPerformancePerModel[10])
    dfKNN = pd.DataFrame.from_dict(dicKNN)
    dfKNN.index = dfKNN.index.astype(int)
    dfKNNFiltered = dfKNN.loc[KNNModels, :]
    dfRF = pd.DataFrame.from_dict(dicRF)
    dfRF.index = dfRF.index.astype(int) + 576
    dfRFFiltered = dfRF.loc[RFModels, :]
    df_concatParams = pd.concat([dfKNNFiltered, dfRFFiltered])
    return df_concatParams

def preProcessFeatAcc():
    dicKNN = json.loads(allParametersPerformancePerModel[3])
    dicRF = json.loads(allParametersPerformancePerModel[11])
    dfKNN = pd.DataFrame.from_dict(dicKNN)
    dfKNN.index = dfKNN.index.astype(int)
    dfKNNFiltered = dfKNN.loc[KNNModels, :]
    dfRF = pd.DataFrame.from_dict(dicRF)
    dfRF.index = dfRF.index.astype(int) + 576
    dfRFFiltered = dfRF.loc[RFModels, :]
    df_featAcc = pd.concat([dfKNNFiltered, dfRFFiltered])
    return df_featAcc

def preProcessPerm():
    dicKNN = json.loads(allParametersPerformancePerModel[4])
    dicRF = json.loads(allParametersPerformancePerModel[12])
    dfKNN = pd.DataFrame.from_dict(dicKNN)
    dfKNN.index = dfKNN.index.astype(int)
    dfKNNFiltered = dfKNN.loc[KNNModels, :]
    dfRF = pd.DataFrame.from_dict(dicRF)
    dfRF.index = dfRF.index.astype(int) + 576
    dfRFFiltered = dfRF.loc[RFModels, :]
    df_perm = pd.concat([dfKNNFiltered, dfRFFiltered])
    return df_perm

def preProcessFeatSc():
    dicKNN = json.loads(allParametersPerformancePerModel[5])
    dfKNN = pd.DataFrame.from_dict(dicKNN)
    return dfKNN

def preProcsumPerMetric(factors):
    sumPerClassifier = []
    loopThroughMetrics = PreprocessingMetrics()
    for row in loopThroughMetrics.iterrows():
        rowSum = 0
        lengthFactors = len(scoring)
        name, values = row
        for loop, elements in enumerate(values):
            lengthFactors = lengthFactors -  1 + factors[loop]
            rowSum = elements*factors[loop] + rowSum
        if lengthFactors is 0:
            sumPerClassifier = 0
        else:
            sumPerClassifier.append(rowSum/lengthFactors)
    return sumPerClassifier

def preProcMetricsAllAndSel():
    loopThroughMetrics = PreprocessingMetrics()
    metricsPerModelColl = []
    metricsPerModelColl.append(loopThroughMetrics['mean_test_accuracy'].sum()/loopThroughMetrics['mean_test_accuracy'].count())
    metricsPerModelColl.append(loopThroughMetrics['mean_test_f1_macro'].sum()/loopThroughMetrics['mean_test_f1_macro'].count())
    metricsPerModelColl.append(loopThroughMetrics['mean_test_precision'].sum()/loopThroughMetrics['mean_test_precision'].count())
    metricsPerModelColl.append(loopThroughMetrics['mean_test_recall'].sum()/loopThroughMetrics['mean_test_recall'].count())
    metricsPerModelColl.append(loopThroughMetrics['mean_test_jaccard'].sum()/loopThroughMetrics['mean_test_jaccard'].count())
    for index, metric in enumerate(metricsPerModelColl):
        metricsPerModelColl[index] = metric*factors[index]
    return metricsPerModelColl

def preProceModels():
    models = KNNModels + RFModels
    return models

def FunMDS (data):
    mds = MDS(n_components=2, random_state=RANDOM_SEED)
    XTransformed = mds.fit_transform(data).T
    XTransformed = XTransformed.tolist()
    return XTransformed

def FunTsne (data):
    tsne = TSNE(n_components=2).fit_transform(data)
    tsne.shape
    return tsne

def InitializeEnsemble(): 

    XModels = PreprocessingMetrics()
    DataSpace = FunTsne(XData)
    DataSpaceList = DataSpace.tolist()

    global ModelSpaceMDS
    global ModelSpaceTSNE

    ModelSpaceMDS = FunMDS(XModels)
    ModelSpaceTSNE = FunTsne(XModels)
    ModelSpaceTSNE = ModelSpaceTSNE.tolist()

    PredictionProbSel = PreprocessingPred()
    PredictionSpace = FunTsne(PredictionProbSel)
    PredictionSpaceList = PredictionSpace.tolist()

    ModelsIDs = preProceModels()

    key = 0
    EnsembleModel(ModelsIDs, key)

    ReturnResults(ModelSpaceMDS,ModelSpaceTSNE,DataSpaceList,PredictionSpaceList)

def ReturnResults(ModelSpaceMDS,ModelSpaceTSNE,DataSpaceList,PredictionSpaceList):

    global Results
    global AllTargets
    Results = []

    parametersGen = PreprocessingParam()
    PerClassMetrics = preProcessPerClassM()
    FeatureAccuracy = preProcessFeatAcc()
    perm_imp_eli5PDCon = preProcessPerm()
    featureScoresCon = preProcessFeatSc()
    metricsPerModel = preProcMetricsAllAndSel()
    sumPerClassifier = preProcsumPerMetric(factors)
    ModelsIDs = preProceModels()

    parametersGenPD = parametersGen.to_json(orient='records')
    PerClassMetrics = PerClassMetrics.to_json(orient='records')
    FeatureAccuracy = FeatureAccuracy.to_json(orient='records')
    perm_imp_eli5PDCon = perm_imp_eli5PDCon.to_json(orient='records')
    featureScoresCon = featureScoresCon.to_json(orient='records')
    XDataJSONEntireSet = XData.to_json(orient='records')
    XDataJSON = XData.columns.tolist()

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
    Results.append(json.dumps(ModelsIDs)) # Position: 13
    Results.append(json.dumps(XDataJSONEntireSet)) # Position: 14
    Results.append(json.dumps(yData)) # Position: 15
    Results.append(json.dumps(AllTargets)) # Position: 16

    return Results


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
@app.route('/data/ServerRemoveFromStack', methods=["GET", "POST"])
def RetrieveSelClassifiersIDandRemoveFromStack():
    ClassifierIDsList = request.get_data().decode('utf8').replace("'", '"')

    PredictionProbSelUpdate = PreprocessingPredUpdate(ClassifierIDsList)

    global resultsUpdatePredictionSpace
    resultsUpdatePredictionSpace = []
    resultsUpdatePredictionSpace.append(json.dumps(PredictionProbSelUpdate[0])) # Position: 0
    resultsUpdatePredictionSpace.append(json.dumps(PredictionProbSelUpdate[1]))

    key = 3
    EnsembleModel(ClassifierIDsList, key)

    return 'Everything Okay'

# Sending the overview classifiers' results to be visualized as a scatterplot
@app.route('/data/UpdatePredictionsSpace', methods=["GET", "POST"])
def SendPredBacktobeUpdated():
    response = {    
        'UpdatePredictions': resultsUpdatePredictionSpace
    }
    return jsonify(response)

# Retrieve data from client 
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/ServerRequestSelPoin', methods=["GET", "POST"])
def RetrieveSelClassifiersID():
    ClassifierIDsList = request.get_data().decode('utf8').replace("'", '"')
    ComputeMetricsForSel(ClassifierIDsList)

    key = 1
    EnsembleModel(ClassifierIDsList, key)
    return 'Everything Okay'

def ComputeMetricsForSel(Models):
    Models = json.loads(Models)
    MetricsAlltoSel = PreprocessingMetrics()
    listofModels = []
    for loop in Models['ClassifiersList']:
        temp = [int(s) for s in re.findall(r'\b\d+\b', loop)]
        listofModels.append(temp[0])
    MetricsAlltoSel = MetricsAlltoSel.loc[listofModels,:]

    global metricsPerModelCollSel
    metricsPerModelCollSel = []
    metricsPerModelCollSel.append(MetricsAlltoSel['mean_test_accuracy'].sum()/MetricsAlltoSel['mean_test_accuracy'].count())
    metricsPerModelCollSel.append(MetricsAlltoSel['mean_test_f1_macro'].sum()/MetricsAlltoSel['mean_test_f1_macro'].count())
    metricsPerModelCollSel.append(MetricsAlltoSel['mean_test_precision'].sum()/MetricsAlltoSel['mean_test_precision'].count())
    metricsPerModelCollSel.append(MetricsAlltoSel['mean_test_recall'].sum()/MetricsAlltoSel['mean_test_recall'].count())
    metricsPerModelCollSel.append(MetricsAlltoSel['mean_test_jaccard'].sum()/MetricsAlltoSel['mean_test_jaccard'].count())
    for index, metric in enumerate(metricsPerModelCollSel):
        metricsPerModelCollSel[index] = metric*factors[index]

    return 'okay'

# Sending the overview classifiers' results to be visualized as a scatterplot
@app.route('/data/BarChartSelectedModels', methods=["GET", "POST"])
def SendToUpdateBarChart():
    response = {    
        'SelectedMetricsForModels': metricsPerModelCollSel
    }
    return jsonify(response)

# Retrieve data from client 
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/ServerRequestDataPoint', methods=["GET", "POST"])
def RetrieveSelDataPoints():

    DataPointsSel = request.get_data().decode('utf8').replace("'", '"')
    DataPointsSelClear = json.loads(DataPointsSel)
    listofDataPoints = []
    for loop in DataPointsSelClear['DataPointsSel']:
        temp = [int(s) for s in re.findall(r'\b\d+\b', loop)]
        listofDataPoints.append(temp[0])

    paramsListSepPD = []
    paramsListSepPD = PreprocessingParamSep()

    paramsListSeptoDicKNN = paramsListSepPD[0].to_dict(orient='list')
    paramsListSeptoDicRF = paramsListSepPD[1].to_dict(orient='list')

    RetrieveParamsCleared = {}
    RetrieveParamsClearedListKNN = []
    for key, value in paramsListSeptoDicKNN.items():
        withoutDuplicates = Remove(value)
        RetrieveParamsCleared[key] = withoutDuplicates
    RetrieveParamsClearedListKNN.append(RetrieveParamsCleared)

    RetrieveParamsCleared = {}
    RetrieveParamsClearedListRF = []
    for key, value in paramsListSeptoDicRF.items():
        withoutDuplicates = Remove(value)
        RetrieveParamsCleared[key] = withoutDuplicates
    RetrieveParamsClearedListRF.append(RetrieveParamsCleared)

    if (len(paramsListSeptoDicKNN['n_neighbors']) is 0):
        RetrieveParamsClearedListKNN = []

    if (len(paramsListSeptoDicRF['n_estimators']) is 0):
        RetrieveParamsClearedListRF = []
    
    for eachAlgor in algorithms:
        if (eachAlgor) == 'KNN':
            clf = KNeighborsClassifier()
            #params = {'n_neighbors': list(range(1, 25)), 'weights': ['uniform', 'distance'], 'algorithm': ['brute', 'kd_tree', 'ball_tree'], 'metric': ['chebyshev', 'manhattan', 'euclidean', 'minkowski']}
            params = RetrieveParamsClearedListKNN
            AlgorithmsIDsEnd = 0
        else: 
            clf = RandomForestClassifier()
            #params = {'n_estimators': list(range(40, 120)), 'criterion': ['gini', 'entropy']}
            params = RetrieveParamsClearedListRF
            AlgorithmsIDsEnd = 576
        metricsSelList = GridSearchSel(clf, params, factors, AlgorithmsIDsEnd, listofDataPoints)
    if (len(metricsSelList[0]) != 0 and len(metricsSelList[1]) != 0):

        dicKNN = json.loads(metricsSelList[0])
        dfKNN = pd.DataFrame.from_dict(dicKNN)
        parametersSelDataPD = parametersSelData[0].apply(pd.Series)
        set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[0], paramsListSepPD[0]]).drop_duplicates(keep=False)
        set_diff_df = set_diff_df.index.tolist()
        if (len(set_diff_df) == 0):
            dfKNNCleared = dfKNN
        else:
            dfKNNCleared = dfKNN.drop(dfKNN.index[set_diff_df])

        dicRF = json.loads(metricsSelList[1])
        dfRF = pd.DataFrame.from_dict(dicRF)
        parametersSelDataPD = parametersSelData[1].apply(pd.Series)
        set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[1], paramsListSepPD[1]]).drop_duplicates(keep=False)
        set_diff_df = set_diff_df.index.tolist()
        if (len(set_diff_df) == 0):
            dfRFCleared = dfRF
        else:
            dfRFCleared = dfRF.drop(dfRF.index[set_diff_df])

        df_concatMetrics = pd.concat([dfKNNCleared, dfRFCleared])
    else:
        if (len(metricsSelList[0]) != 0):
            dicKNN = json.loads(metricsSelList[0])
            dfKNN = pd.DataFrame.from_dict(dicKNN)
            parametersSelDataPD = parametersSelData[0].apply(pd.Series)
            set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[0], paramsListSepPD[0]]).drop_duplicates(keep=False)
            set_diff_df = set_diff_df.index.tolist()
            if (len(set_diff_df) == 0):
                dfKNNCleared = dfKNN
            else:
                dfKNNCleared = dfKNN.drop(dfKNN.index[set_diff_df])
            df_concatMetrics = dfKNNCleared
        else:
            dicRF = json.loads(metricsSelList[1])
            dfRF = pd.DataFrame.from_dict(dicRF)
            parametersSelDataPD = parametersSelData[1].apply(pd.Series)
            set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[1], paramsListSepPD[1]]).drop_duplicates(keep=False)
            set_diff_df = set_diff_df.index.tolist()
            if (len(set_diff_df) == 0):
                dfRFCleared = dfRF
            else:
                dfRFCleared = dfRF.drop(dfRF.index[set_diff_df])
            df_concatMetrics = dfRFCleared


    
    global sumPerClassifierSelUpdate
    sumPerClassifierSelUpdate = []
    sumPerClassifierSelUpdate = preProcsumPerMetricAccordingtoData(factors, df_concatMetrics)

    ModelSpaceMDSNewComb = [list(a) for a in  zip(ModelSpaceMDS[0], ModelSpaceMDS[1])]

    ModelSpaceMDSNewSel = FunMDS(df_concatMetrics)

    ModelSpaceMDSNewSelComb = [list(a) for a in  zip(ModelSpaceMDSNewSel[0], ModelSpaceMDSNewSel[1])]

    global mt2xFinal
    mt2xFinal = []
    mtx1, mtx2, disparity = procrustes(ModelSpaceMDSNewComb, ModelSpaceMDSNewSelComb)
    a, b = zip(*mtx2)
    mt2xFinal.append(a)
    mt2xFinal.append(b)

    return 'Everything Okay'


def GridSearchSel(clf, params, factors, AlgorithmsIDsEnd, DataPointsSel):
    if (len(params) == 0):
        resultsMetrics.append([]) # Position: 0 and so on 
        parametersSelData.append([])
    else:
        # instantiate spark session
        spark = (   
            SparkSession    
            .builder    
            .getOrCreate()    
            )
        sc = spark.sparkContext 

        XDatasubset = XData.loc[DataPointsSel,:]
        yDataSubset = [yData[i] for i in DataPointsSel]
        # this is the grid we use to train the models
        grid = DistGridSearchCV(    
            estimator=clf, param_grid=params,     
            sc=sc, cv=crossValidation, refit='accuracy', scoring=scoring,
            verbose=0, n_jobs=-1)

        # fit and extract the probabilities
        grid.fit(XDatasubset, yDataSubset)

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

        parametersSelData.append(df_cv_results_classifiers['params'])

        # copy and filter in order to get only the metrics
        metrics = df_cv_results_classifiers.copy()
        metrics = metrics.filter(['mean_test_accuracy','mean_test_f1_macro','mean_test_precision','mean_test_recall','mean_test_jaccard']) 
        metrics = metrics.to_json()

        resultsMetrics.append(metrics) # Position: 0 and so on 

    return resultsMetrics


def preProcsumPerMetricAccordingtoData(factors, loopThroughMetrics):
    sumPerClassifier = []
    for row in loopThroughMetrics.iterrows():
        rowSum = 0
        lengthFactors = len(scoring)
        name, values = row
        for loop, elements in enumerate(values):
            lengthFactors = lengthFactors -  1 + factors[loop]
            rowSum = elements*factors[loop] + rowSum
        if lengthFactors is 0:
            sumPerClassifier = 0
        else:
            sumPerClassifier.append(rowSum/lengthFactors)
    return sumPerClassifier

# Sending the overview classifiers' results to be visualized as a scatterplot
@app.route('/data/ServerSentDataPointsModel', methods=["GET", "POST"])
def SendDataPointsModels():
    ResultsUpdate = []
    global sumPerClassifierSelUpdate
    sumPerClassifierSelUpdateJSON = json.dumps(sumPerClassifierSelUpdate)
    ResultsUpdate.append(sumPerClassifierSelUpdateJSON)
    global mt2xFinal
    mt2xFinalJSON = json.dumps(mt2xFinal)
    ResultsUpdate.append(mt2xFinalJSON)
    response = {    
        'DataPointsModels': ResultsUpdate
    }
    return jsonify(response)

# Retrieve data from client 
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/FeaturesSelection', methods=["GET", "POST"])
def FeatureSelPerModel():
    global featureSelection
    featureSelection = request.get_data().decode('utf8').replace("'", '"')
    featureSelection = json.loads(featureSelection)
    key = 2
    ModelsIDs = preProceModels()
    EnsembleModel(ModelsIDs, key)
    return 'Everything Okay'

def EnsembleModel(Models, keyRetrieved): 
    global scores
    scores = []

    global all_classifiersSelection  
    all_classifiersSelection = []

    global XData
    global yData

    lr = LogisticRegression()

    if (keyRetrieved == 0):
        global all_classifiers
        all_classifiers = []
        columnsInit = []
        columnsInit = [XData.columns.get_loc(c) for c in XData.columns if c in XData]

        temp = json.loads(allParametersPerformancePerModel[1])
        dfParamKNN = pd.DataFrame.from_dict(temp)
        dfParamKNNFilt = dfParamKNN.iloc[:,1]

        for eachelem in KNNModels:
            arg = dfParamKNNFilt[eachelem]
            all_classifiers.append(make_pipeline(ColumnSelector(cols=columnsInit), KNeighborsClassifier().set_params(**arg)))
    
        temp = json.loads(allParametersPerformancePerModel[9])
        dfParamRF = pd.DataFrame.from_dict(temp)
        dfParamRFFilt = dfParamRF.iloc[:,1]
        for eachelem in RFModels:
            arg = dfParamRFFilt[eachelem-576]
            all_classifiers.append(make_pipeline(ColumnSelector(cols=columnsInit), RandomForestClassifier().set_params(**arg)))
        
        global sclfStack
        sclfStack = 0

        global sclf 
        sclf = 0
        sclf = StackingCVClassifier(classifiers=all_classifiers,
                            use_probas=True,
                            meta_classifier=lr,
                            random_state=RANDOM_SEED,
                            n_jobs = -1)
        sclfStack = sclf
    elif (keyRetrieved == 1):     
        Models = json.loads(Models)
        ModelsAll = preProceModels()
        for index, modHere in enumerate(ModelsAll):
            flag = 0
            for loop in Models['ClassifiersList']:
                temp = [int(s) for s in re.findall(r'\b\d+\b', loop)]
                if (int(temp[0]) == int(modHere)):
                    flag = 1
            if (flag is 1):
                all_classifiersSelection.append(all_classifiers[index])

        sclf = StackingCVClassifier(classifiers=all_classifiersSelection,
                            use_probas=True,
                            meta_classifier=lr,
                            random_state=RANDOM_SEED,
                            n_jobs = -1)
    elif (keyRetrieved == 2):
        # fix this part!
        if (len(all_classifiersSelection) == 0):
            all_classifiers = []
            columnsInit = []

            temp = json.loads(allParametersPerformancePerModel[1])
            dfParamKNN = pd.DataFrame.from_dict(temp)
            dfParamKNNFilt = dfParamKNN.iloc[:,1]
            print(featureSelection)
            flag = 0
            for index, eachelem in enumerate(KNNModels):
                arg = dfParamKNNFilt[eachelem]
                all_classifiers.append(make_pipeline(ColumnSelector(cols=featureSelection['featureSelection'][index]), KNeighborsClassifier().set_params(**arg)))
                store = index
                flag = 1
            
            temp = json.loads(allParametersPerformancePerModel[9])
            dfParamRF = pd.DataFrame.from_dict(temp)
            dfParamRFFilt = dfParamRF.iloc[:,1]
            if (flag == 0):
                store = 0  
            else:
                store = store + 1               
            for index, eachelem in enumerate(RFModels):
                arg = dfParamRFFilt[eachelem-576]
                print(index)
                print(featureSelection['featureSelection'][index+store])
                all_classifiers.append(make_pipeline(ColumnSelector(cols=featureSelection['featureSelection'][index+store]), RandomForestClassifier().set_params(**arg)))
                
            sclf = StackingCVClassifier(classifiers=all_classifiers,
                                use_probas=True,
                                meta_classifier=lr,
                                random_state=RANDOM_SEED,
                                n_jobs = -1)
    else: 
        Models = json.loads(Models)
        ModelsAll = preProceModels()
        for index, modHere in enumerate(ModelsAll):
            flag = 0
            for loop in Models['ClassifiersList']:
                temp = [int(s) for s in re.findall(r'\b\d+\b', loop)]
                if (int(temp[0]) == int(modHere)):
                    flag = 1
            if (flag is 0):
                all_classifiersSelection.append(all_classifiers[index])

        sclfStack = StackingCVClassifier(classifiers=all_classifiersSelection,
                            use_probas=True,
                            meta_classifier=lr,
                            random_state=RANDOM_SEED,
                            n_jobs = -1)
        
        #else:
        #    for index, eachelem in enumerate(algorithmsWithoutDuplicates):
        #        if (eachelem == 'KNN'):
        #            for j, each in enumerate(resultsList[index][1]):
        #                all_classifiersSelection.append(make_pipeline(ColumnSelector(cols=columnsReduce[j]), KNeighborsClassifier().set_params(**each)))
        #            del columnsReduce[0:len(resultsList[index][1])]
        #        else:
        #            for j, each in enumerate(resultsList[index][1]):
        #                all_classifiersSelection.append(make_pipeline(ColumnSelector(cols=columnsReduce[j]), RandomForestClassifier().set_params(**each)))
        #            del columnsReduce[0:len(resultsList[index][1])]
        #    sclf = StackingCVClassifier(classifiers=all_classifiersSelection,
        #                        use_probas=True,
        #                        meta_classifier=lr,
        #                        random_state=RANDOM_SEED,
        #                        n_jobs = -1)

    # parallelize all that 
    temp = model_selection.cross_val_score(sclf, XData, yData, cv=crossValidation, scoring='accuracy', n_jobs=-1)
    scores.append(temp.mean())
    scores.append(temp.std())

    # influence calculation for all the instances
    #DataHeatmap = []

    #for indexValue, row in XData.iterrows():
    #    XDataRemove = XData.copy()
    #    XDataRemove.drop(indexValue, inplace=True)
    #    yDataRemove = yData.copy()
    #    del yDataRemove[indexValue]
    #    tempRemove = model_selection.cross_val_score(sclf, XDataRemove, yDataRemove, cv=crossValidation, scoring='accuracy', n_jobs=-1)
    #    DataHeatmap.append(abs((tempRemove.mean()+tempRemove.std())-(temp.mean()+temp.std())))

    #print(DataHeatmap)

    #averageValueData = sum(DataHeatmap) / len(DataHeatmap) 

    #print(averageValueData)

    temp = model_selection.cross_val_score(sclf, XData, yData, cv=crossValidation, scoring='precision_weighted', n_jobs=-1)
    scores.append(temp.mean())
    scores.append(temp.std())
    temp = model_selection.cross_val_score(sclf, XData, yData, cv=crossValidation, scoring='recall_weighted', n_jobs=-1)
    scores.append(temp.mean())
    scores.append(temp.std())
    temp = model_selection.cross_val_score(sclfStack, XData, yData, cv=crossValidation, scoring='accuracy', n_jobs=-1)
    scores.append(temp.mean())
    scores.append(temp.std())
    temp = model_selection.cross_val_score(sclfStack, XData, yData, cv=crossValidation, scoring='precision_weighted', n_jobs=-1)
    scores.append(temp.mean())
    scores.append(temp.std())
    temp = model_selection.cross_val_score(sclfStack, XData, yData, cv=crossValidation, scoring='recall_weighted', n_jobs=-1)
    scores.append(temp.mean())
    scores.append(temp.std())

    return 'Okay'

# Sending the final results to be visualized as a line plot
@app.route('/data/SendFinalResultsBacktoVisualize', methods=["GET", "POST"])
def SendToPlotFinalResults():
    response = {    
        'FinalResults': scores
    }
    return jsonify(response)

# Retrieve data from client 
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/UpdateFilter', methods=["GET", "POST"])
def RetrieveFilter():
    filterData = request.get_data().decode('utf8').replace("'", '"')
    filterDataCleared = json.loads(filterData)
    global filterDataFinal
    filterDataFinal = filterDataCleared['filter']
    return 'Done'

# Retrieve data from client 
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/SendDataSpacPoints', methods=["GET", "POST"])
def RetrieveDataSpacePoints():
    dataSpacePoints = request.get_data().decode('utf8').replace("'", '"')
    dataSpacePointsCleared = json.loads(dataSpacePoints)
    global dataSpacePointsIDs
    dataSpacePointsIDs = dataSpacePointsCleared['points']
    return 'Done'

# Retrieve data from client 
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/UpdateAction', methods=["GET", "POST"])
def RetrieveAction():
    filterAction = request.get_data().decode('utf8').replace("'", '"')
    filterActionCleared = json.loads(filterAction)

    global filterActionFinal
    global dataSpacePointsIDs
    global filterDataFinal
    global XData
    global yData

    filterActionFinal = filterActionCleared['action']

    if (filterActionFinal == 'merge'): # fix merge
        if (filterDataFinal == 'mean' or filterDataFinal == ''):
            mean = XData.iloc[dataSpacePointsIDs, :].mean()
            XData.loc[len(XData)]= mean
        else:
            median = XData.iloc[dataSpacePointsIDs, :].median()
            XData.loc[len(XData)]= median
        yDataSelected = [yData[i] for i in dataSpacePointsIDs]
        storeMode = mode(yDataSelected)
        yData.append(storeMode)
        XData = XData.drop(dataSpacePointsIDs)
        yData = [i for j, i in enumerate(yData) if j not in dataSpacePointsIDs]
        XData.reset_index(drop=True, inplace=True)
    elif (filterActionFinal == 'compose'):
        if (filterDataFinal == 'mean' or filterDataFinal == ''):
            mean = XData.iloc[dataSpacePointsIDs, :].mean()
            XData.loc[len(XData)]= mean
        else:
            median = XData.iloc[dataSpacePointsIDs, :].median()
            XData.loc[len(XData)]= median
        yDataSelected = [yData[i] for i in dataSpacePointsIDs]
        storeMode = mode(yDataSelected)
        yData.append(storeMode)
    else:
        XData = XData.drop(dataSpacePointsIDs)
        yData = [i for j, i in enumerate(yData) if j not in dataSpacePointsIDs]

    

    return 'Done'

# Retrieve data from client 
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/UpdateProvenanceState', methods=["GET", "POST"])
def RetrieveProvenance():
    filterProvenance = request.get_data().decode('utf8').replace("'", '"')
    filterProvenanceCleared = json.loads(filterProvenance)
    global filterProvenanceFinal
    filterProvenanceFinal = filterProvenanceCleared['provenance']

    global XDataStored
    global XData
    global yDataStored
    global yData

    # fix save and restore

    if (filterProvenanceFinal == 'save'):
        XDataStored = XData
        yDataStored = yData
    else:
        XData = XDataStored.copy()
        yData = yDataStored.copy()
    return 'Done'