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

from sklearn.neighbors import KNeighborsClassifier # 1 neighbors
from sklearn.svm import SVC # 1 svm
from sklearn.naive_bayes import GaussianNB # 1 naive bayes
from sklearn.neural_network import MLPClassifier # 1 neural network
from sklearn.linear_model import LogisticRegression # 1 linear model
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis # 2 discriminant analysis
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, AdaBoostClassifier, GradientBoostingClassifier # 4 ensemble models
from joblib import Parallel, delayed
import multiprocessing

from sklearn.pipeline import make_pipeline
from sklearn import model_selection
from sklearn.manifold import MDS
from sklearn.manifold import TSNE
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import log_loss
from sklearn.metrics import fbeta_score
from imblearn.metrics import geometric_mean_score
import umap
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
    global previousState
    previousState = []

    global keySpecInternal
    keySpecInternal = 1

    global previousStateActive
    previousStateActive = []

    global RANDOM_SEED
    RANDOM_SEED = 42

    global factors
    factors = [1,0,0,1,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,1,1,1]

    global KNNModelsCount
    global SVCModelsCount
    global GausNBModelsCount
    global MLPModelsCount
    global LRModelsCount
    global LDAModelsCount
    global QDAModelsCount
    global RFModelsCount
    global ExtraTModelsCount
    global AdaBModelsCount
    global GradBModelsCount

    global keyData
    keyData = 0

    KNNModelsCount = 0
    SVCModelsCount = 576
    GausNBModelsCount = 736
    MLPModelsCount = 1236
    LRModelsCount = 1356
    LDAModelsCount = 1996
    QDAModelsCount = 2196
    RFModelsCount = 2446
    ExtraTModelsCount = 2606
    AdaBModelsCount = 2766
    GradBModelsCount = 2926

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
    crossValidation = 5
    
    # models
    global KNNModels
    KNNModels = []
    global RFModels
    RFModels = []

    global scoring
    scoring = {'accuracy': 'accuracy', 'precision_micro': 'precision_micro', 'precision_macro': 'precision_macro', 'precision_weighted': 'precision_weighted', 'recall_micro': 'recall_micro', 'recall_macro': 'recall_macro', 'recall_weighted': 'recall_weighted', 'roc_auc_ovo_weighted': 'roc_auc_ovo_weighted'}

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
    global DataRawLength
    global DataResultsRaw

    fileName = request.get_data().decode('utf8').replace("'", '"')

    global keySpecInternal
    keySpecInternal = 1

    global RANDOM_SEED
    RANDOM_SEED = 42

    global keyData
    keyData = 0

    global XData
    XData = []

    global previousState
    previousState = []

    global previousStateActive
    previousStateActive = []

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
    crossValidation = 5

    global scoring
    scoring = {'accuracy': 'accuracy', 'precision_micro': 'precision_micro', 'precision_macro': 'precision_macro', 'precision_weighted': 'precision_weighted', 'recall_micro': 'recall_micro', 'recall_macro': 'recall_macro', 'recall_weighted': 'recall_weighted', 'roc_auc_ovo_weighted': 'roc_auc_ovo_weighted'}

    global loopFeatures
    loopFeatures = 2

    # models
    global KNNModels
    global SVCModels
    global GausNBModels
    global MLPModels
    global LRModels
    global LDAModels
    global QDAModels 
    global RFModels
    global ExtraTModels
    global AdaBModels
    global GradBModels

    KNNModels = []
    SVCModels = []
    GausNBModels = []
    MLPModels = []
    LRModels = []
    LDAModels = []
    QDAModels = []
    RFModels = []
    ExtraTModels = []
    AdaBModels = []
    GradBModels = []

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
    if data['fileName'] == 'HeartC':
        CollectionDB = mongo.db.HeartC.find()
    elif data['fileName'] == 'StanceC':
        CollectionDB = mongo.db.StanceC.find()
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

def Convert(lst): 
    it = iter(lst) 
    res_dct = dict(zip(it, it)) 
    return res_dct 

# Retrieve data set from client
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/SendtoSeverDataSet', methods=["GET", "POST"])
def SendToServerData():

    uploadedData = request.get_data().decode('utf8').replace("'", '"')
    uploadedDataParsed = json.loads(uploadedData)
    DataResultsRaw = uploadedDataParsed['uploadedData']

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
        del dictionary[target]

    global AllTargets
    global target_names
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
    
    return 'Processed uploaded data set'

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

    global AllTargets
    global target_names
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

    warnings.simplefilter('ignore')
    return 'Everything is okay'

def callPreResults():

    global XData
    global yData
    global target_names
    global impDataInst

    DataSpaceResMDS = FunMDS(XData)
    DataSpaceResTSNE = FunTsne(XData)
    DataSpaceResTSNE = DataSpaceResTSNE.tolist()
    DataSpaceUMAP = FunUMAP(XData)

    XDataJSONEntireSetRes = XData.to_json(orient='records')

    global preResults 
    preResults = []

    preResults.append(json.dumps(target_names)) # Position: 0
    preResults.append(json.dumps(DataSpaceResMDS)) # Position: 1
    preResults.append(json.dumps(XDataJSONEntireSetRes)) # Position: 2
    preResults.append(json.dumps(yData)) # Position: 3
    preResults.append(json.dumps(AllTargets)) # Position: 4
    preResults.append(json.dumps(DataSpaceResTSNE)) # Position: 5
    preResults.append(json.dumps(DataSpaceUMAP)) # Position: 6
    preResults.append(json.dumps(impDataInst)) # Position: 7

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
    toggle = RetrievedModel['Toggle']

    global XData
    global yData
    global SVCModelsCount
    global GausNBModelsCount
    global MLPModelsCount
    global LRModelsCount
    global LDAModelsCount
    global QDAModelsCount
    global RFModelsCount
    global ExtraTModelsCount
    global AdaBModelsCount
    global GradBModelsCount

    # loop through the algorithms
    global allParametersPerformancePerModel
    for eachAlgor in algorithms:
        if (eachAlgor) == 'KNN':
            clf = KNeighborsClassifier()
            params = {'n_neighbors': list(range(1, 25)), 'metric': ['chebyshev', 'manhattan', 'euclidean', 'minkowski'], 'algorithm': ['brute', 'kd_tree', 'ball_tree'], 'weights': ['uniform', 'distance']}
            AlgorithmsIDsEnd = 0
        elif (eachAlgor) == 'SVC':
            clf = SVC(probability=True,random_state=RANDOM_SEED)
            params = {'C': list(np.arange(0.1,4.43,0.11)), 'kernel': ['rbf','linear', 'poly', 'sigmoid']}
            AlgorithmsIDsEnd = SVCModelsCount
        elif (eachAlgor) == 'GausNB':
            clf = GaussianNB()
            params = {'var_smoothing': list(np.arange(0.00000000001,0.0000001,0.0000000002))}
            AlgorithmsIDsEnd = GausNBModelsCount
        elif (eachAlgor) == 'MLP':
            clf = MLPClassifier(random_state=RANDOM_SEED)
            params = {'alpha': list(np.arange(0.00001,0.001,0.0002)), 'tol': list(np.arange(0.00001,0.001,0.0004)), 'max_iter': list(np.arange(100,200,100)), 'activation': ['relu', 'identity', 'logistic', 'tanh'], 'solver' : ['adam', 'sgd']}
            AlgorithmsIDsEnd = MLPModelsCount
        elif (eachAlgor) == 'LR':
            clf = LogisticRegression(random_state=RANDOM_SEED)
            params = {'C': list(np.arange(0.5,2,0.075)), 'max_iter': list(np.arange(50,250,50)), 'solver': ['lbfgs', 'newton-cg', 'sag', 'saga'], 'penalty': ['l2', 'none']}
            AlgorithmsIDsEnd = LRModelsCount
        elif (eachAlgor) == 'LDA':
            clf = LinearDiscriminantAnalysis()
            params = {'shrinkage': list(np.arange(0,1,0.01)), 'solver': ['lsqr', 'eigen']}
            AlgorithmsIDsEnd = LDAModelsCount
        elif (eachAlgor) == 'QDA':
            clf = QuadraticDiscriminantAnalysis()
            params = {'reg_param': list(np.arange(0,1,0.02)), 'tol': list(np.arange(0.00001,0.001,0.0002))}
            AlgorithmsIDsEnd = QDAModelsCount
        elif (eachAlgor) == 'RF':
            clf = RandomForestClassifier(random_state=RANDOM_SEED)
            params = {'n_estimators': list(range(60, 140)), 'criterion': ['gini', 'entropy']}
            AlgorithmsIDsEnd = RFModelsCount
        elif (eachAlgor) == 'ExtraT':
            clf = ExtraTreesClassifier(random_state=RANDOM_SEED)
            params = {'n_estimators': list(range(60, 140)), 'criterion': ['gini', 'entropy']}
            AlgorithmsIDsEnd = ExtraTModelsCount
        elif (eachAlgor) == 'AdaB':
            clf = AdaBoostClassifier(random_state=RANDOM_SEED)
            params = {'n_estimators': list(range(40, 80)), 'learning_rate': list(np.arange(0.1,2.3,1.1)), 'algorithm': ['SAMME.R', 'SAMME']}
            AlgorithmsIDsEnd = AdaBModelsCount
        else: 
            clf = GradientBoostingClassifier(random_state=RANDOM_SEED)
            params = {'n_estimators': list(range(85, 115)), 'learning_rate': list(np.arange(0.01,0.23,0.11)), 'criterion': ['friedman_mse', 'mse', 'mae']}
            AlgorithmsIDsEnd = GradBModelsCount
        allParametersPerformancePerModel = GridSearchForModels(XData, yData, clf, params, eachAlgor, AlgorithmsIDsEnd, toggle)
    # call the function that sends the results to the frontend 
    SendEachClassifiersPerformanceToVisualize()

    return 'Everything Okay'

location = './cachedir'
memory = Memory(location, verbose=0)

# calculating for all algorithms and models the performance and other results
@memory.cache
def GridSearchForModels(XData, yData, clf, params, eachAlgor, AlgorithmsIDsEnd, toggle):
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

    metrics = metrics.filter(['mean_test_accuracy','mean_test_precision_micro','mean_test_precision_macro','mean_test_precision_weighted','mean_test_recall_micro','mean_test_recall_macro','mean_test_recall_weighted','mean_test_roc_auc_ovo_weighted']) 

    # concat parameters and performance
    parametersPerformancePerModel = pd.DataFrame(df_cv_results_classifiers['params'])
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
    
    perModelPrediction = []
    resultsMicro = []
    resultsMacro = []
    resultsWeighted = []
    resultsCorrCoef = []
    resultsMicroBeta5 = []
    resultsMacroBeta5 = []
    resultsWeightedBeta5 = []
    resultsMicroBeta1 = []
    resultsMacroBeta1 = []
    resultsWeightedBeta1 = []
    resultsMicroBeta2 = []
    resultsMacroBeta2 = []
    resultsWeightedBeta2 = []
    resultsLogLoss = []
    resultsLogLossFinal = []

    loop = 8

    # influence calculation for all the instances
    inputs = range(len(XData))
    num_cores = multiprocessing.cpu_count()
    
    #impDataInst = Parallel(n_jobs=num_cores)(delayed(processInput)(i,XData,yData,crossValidation,clf) for i in inputs)
    
    for eachModelParameters in parametersLocalNew:
        clf.set_params(**eachModelParameters)
        if (toggle == 1):
            perm = PermutationImportance(clf, cv = None, refit = True, n_iter = 25).fit(XData, yData)
            permList.append(perm.feature_importances_)
            n_feats = XData.shape[1]
            PerFeatureAccuracy = []
            for i in range(n_feats):
                scores = model_selection.cross_val_score(clf, XData.values[:, i].reshape(-1, 1), yData, cv=crossValidation)
                PerFeatureAccuracy.append(scores.mean())
            PerFeatureAccuracyAll.append(PerFeatureAccuracy)
        else:
            permList.append(0)
            PerFeatureAccuracyAll.append(0)
        clf.fit(XData, yData) 
        yPredict = clf.predict(XData)
        yPredict = np.nan_to_num(yPredict)
        perModelPrediction.append(yPredict)
        # retrieve target names (class names)
        PerClassMetric.append(classification_report(yData, yPredict, target_names=target_names, digits=2, output_dict=True))
        yPredictProb = clf.predict_proba(XData)
        yPredictProb = np.nan_to_num(yPredictProb)
        perModelProb.append(yPredictProb.tolist())

        resultsMicro.append(geometric_mean_score(yData, yPredict, average='micro'))
        resultsMacro.append(geometric_mean_score(yData, yPredict, average='macro'))
        resultsWeighted.append(geometric_mean_score(yData, yPredict, average='weighted'))

        resultsCorrCoef.append(matthews_corrcoef(yData, yPredict))

        resultsMicroBeta5.append(fbeta_score(yData, yPredict, average='micro', beta=0.5))
        resultsMacroBeta5.append(fbeta_score(yData, yPredict, average='macro', beta=0.5))
        resultsWeightedBeta5.append(fbeta_score(yData, yPredict, average='weighted', beta=0.5))

        resultsMicroBeta1.append(fbeta_score(yData, yPredict, average='micro', beta=1))
        resultsMacroBeta1.append(fbeta_score(yData, yPredict, average='macro', beta=1))
        resultsWeightedBeta1.append(fbeta_score(yData, yPredict, average='weighted', beta=1))
        
        resultsMicroBeta2.append(fbeta_score(yData, yPredict, average='micro', beta=2))
        resultsMacroBeta2.append(fbeta_score(yData, yPredict, average='macro', beta=2))
        resultsWeightedBeta2.append(fbeta_score(yData, yPredict, average='weighted', beta=2))
  
        resultsLogLoss.append(log_loss(yData, yPredictProb, normalize=True))

    maxLog = max(resultsLogLoss)
    minLog = min(resultsLogLoss)
    for each in resultsLogLoss:
        resultsLogLossFinal.append((each-minLog)/(maxLog-minLog))

    metrics.insert(loop,'geometric_mean_score_micro',resultsMicro)
    metrics.insert(loop+1,'geometric_mean_score_macro',resultsMacro)
    metrics.insert(loop+2,'geometric_mean_score_weighted',resultsWeighted)

    metrics.insert(loop+3,'matthews_corrcoef',resultsCorrCoef)

    metrics.insert(loop+4,'f5_micro',resultsMicroBeta5)
    metrics.insert(loop+5,'f5_macro',resultsMacroBeta5)
    metrics.insert(loop+6,'f5_weighted',resultsWeightedBeta5)
    
    metrics.insert(loop+7,'f1_micro',resultsMicroBeta1)
    metrics.insert(loop+8,'f1_macro',resultsMacroBeta1)
    metrics.insert(loop+9,'f1_weighted',resultsWeightedBeta1)

    metrics.insert(loop+10,'f2_micro',resultsMicroBeta2)
    metrics.insert(loop+11,'f2_macro',resultsMacroBeta2)
    metrics.insert(loop+12,'f2_weighted',resultsWeightedBeta2)

    metrics.insert(loop+13,'log_loss',resultsLogLossFinal)

    perModelPredPandas = pd.DataFrame(perModelPrediction)
    print(perModelPredPandas)
    perModelPredPandas = perModelPredPandas.to_json()

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
    results.append(json.dumps(perModelPredPandas)) # Position: 8 and so on

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
                    final_list.append(float(num)) 
            else:
                final_list.append(num) 
    return final_list 

# Retrieve data from client 
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/SendBrushedParam', methods=["GET", "POST"])
def RetrieveModelsParam():
    RetrieveModelsPar = request.get_data().decode('utf8').replace("'", '"')
    RetrieveModelsPar = json.loads(RetrieveModelsPar)

    counterKNN = 0
    counterSVC = 0
    counterGausNB = 0
    counterMLP = 0
    counterLR = 0
    counterLDA = 0
    counterQDA = 0
    counterRF = 0
    counterExtraT = 0
    counterAdaB = 0
    counterGradB = 0

    global KNNModels
    global SVCModels
    global GausNBModels
    global MLPModels
    global LRModels
    global LDAModels
    global QDAModels
    global RFModels
    global ExtraTModels
    global AdaBModels
    global GradBModels

    global algorithmsList

    algorithmsList = RetrieveModelsPar['algorithms']
    for index, items in enumerate(algorithmsList):
        if (items == 'KNN'):
            counterKNN += 1
            KNNModels.append(int(RetrieveModelsPar['models'][index]))
        elif (items == 'SVC'):
            counterSVC += 1
            SVCModels.append(int(RetrieveModelsPar['models'][index]))
        elif (items == 'GausNB'):
            counterGausNB += 1
            GausNBModels.append(int(RetrieveModelsPar['models'][index]))
        elif (items == 'MLP'):
            counterMLP += 1
            MLPModels.append(int(RetrieveModelsPar['models'][index]))
        elif (items == 'LR'):
            counterLR += 1
            LRModels.append(int(RetrieveModelsPar['models'][index]))
        elif (items == 'LDA'):
            counterLDA += 1
            LDAModels.append(int(RetrieveModelsPar['models'][index]))
        elif (items == 'QDA'):
            counterQDA += 1
            QDAModels.append(int(RetrieveModelsPar['models'][index]))
        elif (items == 'RF'):
            counterRF += 1
            RFModels.append(int(RetrieveModelsPar['models'][index]))
        elif (items == 'ExtraT'):
            counterExtraT += 1
            ExtraTModels.append(int(RetrieveModelsPar['models'][index]))
        elif (items == 'AdaB'):
            counterAdaB += 1
            AdaBModels.append(int(RetrieveModelsPar['models'][index]))
        else:
            counterGradB += 1
            GradBModels.append(int(RetrieveModelsPar['models'][index]))

    return 'Everything Okay'

# Retrieve data from client 
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/factors', methods=["GET", "POST"])
def RetrieveFactors():
    global factors
    global allParametersPerformancePerModel
    Factors = request.get_data().decode('utf8').replace("'", '"')
    FactorsInt = json.loads(Factors)
    factors = FactorsInt['Factors']

    # this is if we want to change the factors before running the search
    #if (len(allParametersPerformancePerModel) == 0):
    #    pass
    #else:
    global sumPerClassifierSel
    global ModelSpaceMDSNew
    global ModelSpaceTSNENew
    global metricsPerModel
    sumPerClassifierSel = []
    sumPerClassifierSel = preProcsumPerMetric(factors)
    ModelSpaceMDSNew = []
    ModelSpaceTSNENew = []
    loopThroughMetrics = PreprocessingMetrics()
    loopThroughMetrics = loopThroughMetrics.fillna(0)
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
    dicSVC = json.loads(allParametersPerformancePerModel[15])
    dicGausNB = json.loads(allParametersPerformancePerModel[24])
    dicMLP = json.loads(allParametersPerformancePerModel[33])
    dicLR = json.loads(allParametersPerformancePerModel[42])
    dicLDA = json.loads(allParametersPerformancePerModel[51])
    dicQDA = json.loads(allParametersPerformancePerModel[60])
    dicRF = json.loads(allParametersPerformancePerModel[69])
    dicExtraT = json.loads(allParametersPerformancePerModel[78])
    dicAdaB = json.loads(allParametersPerformancePerModel[87])
    dicGradB = json.loads(allParametersPerformancePerModel[96])

    dfKNN = pd.DataFrame.from_dict(dicKNN)
    dfSVC = pd.DataFrame.from_dict(dicSVC)
    dfGausNB = pd.DataFrame.from_dict(dicGausNB)
    dfMLP = pd.DataFrame.from_dict(dicMLP)
    dfLR = pd.DataFrame.from_dict(dicLR)
    dfLDA = pd.DataFrame.from_dict(dicLDA)
    dfQDA = pd.DataFrame.from_dict(dicQDA)
    dfRF = pd.DataFrame.from_dict(dicRF)
    dfExtraT = pd.DataFrame.from_dict(dicExtraT)
    dfAdaB = pd.DataFrame.from_dict(dicAdaB)
    dfGradB = pd.DataFrame.from_dict(dicGradB)

    dfKNN.index = dfKNN.index.astype(int)
    dfSVC.index = dfSVC.index.astype(int) + SVCModelsCount
    dfGausNB.index = dfGausNB.index.astype(int) + GausNBModelsCount
    dfMLP.index = dfMLP.index.astype(int) + MLPModelsCount
    dfLR.index = dfLR.index.astype(int) + LRModelsCount
    dfLDA.index = dfLDA.index.astype(int) + LDAModelsCount
    dfQDA.index = dfQDA.index.astype(int) + QDAModelsCount
    dfRF.index = dfRF.index.astype(int) + RFModelsCount
    dfExtraT.index = dfExtraT.index.astype(int) + ExtraTModelsCount
    dfAdaB.index = dfAdaB.index.astype(int) + AdaBModelsCount
    dfGradB.index = dfGradB.index.astype(int) + GradBModelsCount
    dfKNNFiltered = dfKNN.loc[KNNModels, :]
    dfSVCFiltered = dfSVC.loc[SVCModels, :]
    dfGausNBFiltered = dfGausNB.loc[GausNBModels, :]
    dfMLPFiltered = dfMLP.loc[MLPModels, :]
    dfLRFiltered = dfLR.loc[LRModels, :]
    dfLDAFiltered = dfLDA.loc[LDAModels, :]
    dfQDAFiltered = dfQDA.loc[QDAModels, :]
    dfRFFiltered = dfRF.loc[RFModels, :]
    dfExtraTFiltered = dfExtraT.loc[ExtraTModels, :]
    dfAdaBFiltered = dfAdaB.loc[AdaBModels, :]
    dfGradBFiltered = dfGradB.loc[GradBModels, :]

    df_concatMetrics = pd.concat([dfKNNFiltered, dfSVCFiltered, dfGausNBFiltered, dfMLPFiltered, dfLRFiltered, dfLDAFiltered, dfQDAFiltered, dfRFFiltered, dfExtraTFiltered, dfAdaBFiltered, dfGradBFiltered])
    return df_concatMetrics

def PreprocessingPred():
    dicKNN = json.loads(allParametersPerformancePerModel[7])
    dicSVC = json.loads(allParametersPerformancePerModel[16])
    dicGausNB = json.loads(allParametersPerformancePerModel[25])
    dicMLP = json.loads(allParametersPerformancePerModel[34])
    dicLR = json.loads(allParametersPerformancePerModel[43])
    dicLDA = json.loads(allParametersPerformancePerModel[52])
    dicQDA = json.loads(allParametersPerformancePerModel[61])
    dicRF = json.loads(allParametersPerformancePerModel[70])
    dicExtraT = json.loads(allParametersPerformancePerModel[79])
    dicAdaB = json.loads(allParametersPerformancePerModel[88])
    dicGradB = json.loads(allParametersPerformancePerModel[97])

    dfKNN = pd.DataFrame.from_dict(dicKNN)
    dfSVC = pd.DataFrame.from_dict(dicSVC)
    dfGausNB = pd.DataFrame.from_dict(dicGausNB)
    dfMLP = pd.DataFrame.from_dict(dicMLP)
    dfLR = pd.DataFrame.from_dict(dicLR)
    dfLDA = pd.DataFrame.from_dict(dicLDA)
    dfQDA = pd.DataFrame.from_dict(dicQDA)
    dfRF = pd.DataFrame.from_dict(dicRF)
    dfExtraT = pd.DataFrame.from_dict(dicExtraT)
    dfAdaB = pd.DataFrame.from_dict(dicAdaB)
    dfGradB = pd.DataFrame.from_dict(dicGradB)

    dfKNN.index = dfKNN.index.astype(int)
    dfSVC.index = dfSVC.index.astype(int) + SVCModelsCount
    dfGausNB.index = dfGausNB.index.astype(int) + GausNBModelsCount
    dfMLP.index = dfMLP.index.astype(int) + MLPModelsCount
    dfLR.index = dfLR.index.astype(int) + LRModelsCount
    dfLDA.index = dfLDA.index.astype(int) + LDAModelsCount
    dfQDA.index = dfQDA.index.astype(int) + QDAModelsCount
    dfRF.index = dfRF.index.astype(int) + RFModelsCount
    dfExtraT.index = dfExtraT.index.astype(int) + ExtraTModelsCount
    dfAdaB.index = dfAdaB.index.astype(int) + AdaBModelsCount
    dfGradB.index = dfGradB.index.astype(int) + GradBModelsCount
    
    dfKNNFiltered = dfKNN.loc[KNNModels, :]
    dfSVCFiltered = dfSVC.loc[SVCModels, :]
    dfGausNBFiltered = dfGausNB.loc[GausNBModels, :]
    dfMLPFiltered = dfMLP.loc[MLPModels, :]
    dfLRFiltered = dfLR.loc[LRModels, :]
    dfLDAFiltered = dfLDA.loc[LDAModels, :]
    dfQDAFiltered = dfQDA.loc[QDAModels, :]
    dfRFFiltered = dfRF.loc[RFModels, :]
    dfExtraTFiltered = dfExtraT.loc[ExtraTModels, :]
    dfAdaBFiltered = dfAdaB.loc[AdaBModels, :]
    dfGradBFiltered = dfGradB.loc[GradBModels, :]

    df_concatProbs = pd.concat([dfKNNFiltered, dfSVCFiltered, dfGausNBFiltered, dfMLPFiltered, dfLRFiltered, dfLDAFiltered, dfQDAFiltered, dfRFFiltered, dfExtraTFiltered, dfAdaBFiltered, dfGradBFiltered])
    predictions = []
    for column, content in df_concatProbs.items():
        el = [sum(x)/len(x) for x in zip(*content)]
        predictions.append(el)

    return predictions

def PreprocessingPredUpdate(Models):
    Models = json.loads(Models)
    ModelsList= []
    for loop in Models['ClassifiersList']:
        ModelsList.append(loop)

    dicKNN = json.loads(allParametersPerformancePerModel[7])
    dicSVC = json.loads(allParametersPerformancePerModel[16])
    dicGausNB = json.loads(allParametersPerformancePerModel[25])
    dicMLP = json.loads(allParametersPerformancePerModel[34])
    dicLR = json.loads(allParametersPerformancePerModel[43])
    dicLDA = json.loads(allParametersPerformancePerModel[52])
    dicQDA = json.loads(allParametersPerformancePerModel[61])
    dicRF = json.loads(allParametersPerformancePerModel[70])
    dicExtraT = json.loads(allParametersPerformancePerModel[79])
    dicAdaB = json.loads(allParametersPerformancePerModel[88])
    dicGradB = json.loads(allParametersPerformancePerModel[97])

    dfKNN = pd.DataFrame.from_dict(dicKNN)
    dfSVC = pd.DataFrame.from_dict(dicSVC)
    dfGausNB = pd.DataFrame.from_dict(dicGausNB)
    dfMLP = pd.DataFrame.from_dict(dicMLP)
    dfLR = pd.DataFrame.from_dict(dicLR)
    dfLDA = pd.DataFrame.from_dict(dicLDA)
    dfQDA = pd.DataFrame.from_dict(dicQDA)
    dfRF = pd.DataFrame.from_dict(dicRF)
    dfExtraT = pd.DataFrame.from_dict(dicExtraT)
    dfAdaB = pd.DataFrame.from_dict(dicAdaB)
    dfGradB = pd.DataFrame.from_dict(dicGradB)

    dfKNN.index = dfKNN.index.astype(int)
    dfSVC.index = dfSVC.index.astype(int) + SVCModelsCount
    dfGausNB.index = dfGausNB.index.astype(int) + GausNBModelsCount
    dfMLP.index = dfMLP.index.astype(int) + MLPModelsCount
    dfLR.index = dfLR.index.astype(int) + LRModelsCount
    dfLDA.index = dfLDA.index.astype(int) + LDAModelsCount
    dfQDA.index = dfQDA.index.astype(int) + QDAModelsCount
    dfRF.index = dfRF.index.astype(int) + RFModelsCount
    dfExtraT.index = dfExtraT.index.astype(int) + ExtraTModelsCount
    dfAdaB.index = dfAdaB.index.astype(int) + AdaBModelsCount
    dfGradB.index = dfGradB.index.astype(int) + GradBModelsCount
    
    dfKNNFiltered = dfKNN.loc[KNNModels, :]
    dfSVCFiltered = dfSVC.loc[SVCModels, :]
    dfGausNBFiltered = dfGausNB.loc[GausNBModels, :]
    dfMLPFiltered = dfMLP.loc[MLPModels, :]
    dfLRFiltered = dfLR.loc[LRModels, :]
    dfLDAFiltered = dfLDA.loc[LDAModels, :]
    dfQDAFiltered = dfQDA.loc[QDAModels, :]
    dfRFFiltered = dfRF.loc[RFModels, :]
    dfExtraTFiltered = dfExtraT.loc[ExtraTModels, :]
    dfAdaBFiltered = dfAdaB.loc[AdaBModels, :]
    dfGradBFiltered = dfGradB.loc[GradBModels, :]

    df_concatProbs = pd.concat([dfKNNFiltered, dfSVCFiltered, dfGausNBFiltered, dfMLPFiltered, dfLRFiltered, dfLDAFiltered, dfQDAFiltered, dfRFFiltered, dfExtraTFiltered, dfAdaBFiltered, dfGradBFiltered])
    listProbs = df_concatProbs.index.values.tolist()
    deletedElements = 0
    for index, element in enumerate(listProbs):
        if element in ModelsList:
            index = index - deletedElements
            df_concatProbs = df_concatProbs.drop(df_concatProbs.index[index])
            deletedElements = deletedElements + 1
    df_concatProbsCleared = df_concatProbs
    listIDsRemoved = df_concatProbsCleared.index.values.tolist()
    predictionsAll = PreprocessingPred()
    PredictionSpaceAll = FunMDS(predictionsAll)

    predictionsSel = []
    for column, content in df_concatProbsCleared.items():
        el = [sum(x)/len(x) for x in zip(*content)]
        predictionsSel.append(el)

    PredictionSpaceSel = FunMDS(predictionsSel)

    mtx2PredFinal = []
    mtx1Pred, mtx2Pred, disparity2 = procrustes(PredictionSpaceAll, PredictionSpaceSel)

    a1 = [i[1] for i in mtx2Pred]
    b1 = [i[0] for i in mtx2Pred]
    mtx2PredFinal.append(a1)
    mtx2PredFinal.append(b1)
    return [mtx2PredFinal,listIDsRemoved]

def PreprocessingParam():
    dicKNN = json.loads(allParametersPerformancePerModel[1])
    dicSVC = json.loads(allParametersPerformancePerModel[10])
    dicGausNB = json.loads(allParametersPerformancePerModel[19])
    dicMLP = json.loads(allParametersPerformancePerModel[28])
    dicLR = json.loads(allParametersPerformancePerModel[37])
    dicLDA = json.loads(allParametersPerformancePerModel[46])
    dicQDA = json.loads(allParametersPerformancePerModel[55])
    dicRF = json.loads(allParametersPerformancePerModel[64])
    dicExtraT = json.loads(allParametersPerformancePerModel[73])
    dicAdaB = json.loads(allParametersPerformancePerModel[82])
    dicGradB = json.loads(allParametersPerformancePerModel[91])

    dicKNN = dicKNN['params']
    dicSVC = dicSVC['params']
    dicGausNB = dicGausNB['params']
    dicMLP = dicMLP['params']
    dicLR = dicLR['params']
    dicLDA = dicLDA['params']
    dicQDA = dicQDA['params']
    dicRF = dicRF['params']
    dicExtraT = dicExtraT['params']
    dicAdaB = dicAdaB['params']
    dicGradB = dicGradB['params']
    
    dicKNN = {int(k):v for k,v in dicKNN.items()}
    dicSVC = {int(k):v for k,v in dicSVC.items()}
    dicGausNB = {int(k):v for k,v in dicGausNB.items()}
    dicMLP = {int(k):v for k,v in dicMLP.items()}
    dicLR = {int(k):v for k,v in dicLR.items()}
    dicLDA = {int(k):v for k,v in dicLDA.items()}
    dicQDA = {int(k):v for k,v in dicQDA.items()}
    dicRF = {int(k):v for k,v in dicRF.items()}
    dicExtraT = {int(k):v for k,v in dicExtraT.items()}
    dicAdaB = {int(k):v for k,v in dicAdaB.items()}
    dicGradB = {int(k):v for k,v in dicGradB.items()}


    dfKNN = pd.DataFrame.from_dict(dicKNN)
    dfSVC = pd.DataFrame.from_dict(dicSVC)
    dfGausNB = pd.DataFrame.from_dict(dicGausNB)
    dfMLP = pd.DataFrame.from_dict(dicMLP)
    dfLR = pd.DataFrame.from_dict(dicLR)
    dfLDA = pd.DataFrame.from_dict(dicLDA)
    dfQDA = pd.DataFrame.from_dict(dicQDA)
    dfRF = pd.DataFrame.from_dict(dicRF)
    dfExtraT = pd.DataFrame.from_dict(dicExtraT)
    dfAdaB = pd.DataFrame.from_dict(dicAdaB)
    dfGradB = pd.DataFrame.from_dict(dicGradB)

    dfKNN = dfKNN.T
    dfSVC = dfSVC.T
    dfGausNB = dfGausNB.T
    dfMLP = dfMLP.T
    dfLR = dfLR.T
    dfLDA = dfLDA.T
    dfQDA = dfQDA.T
    dfRF = dfRF.T
    dfExtraT = dfExtraT.T
    dfAdaB = dfAdaB.T
    dfGradB = dfGradB.T

    dfKNN.index = dfKNN.index.astype(int)
    dfSVC.index = dfSVC.index.astype(int) + SVCModelsCount
    dfGausNB.index = dfGausNB.index.astype(int) + GausNBModelsCount
    dfMLP.index = dfMLP.index.astype(int) + MLPModelsCount
    dfLR.index = dfLR.index.astype(int) + LRModelsCount
    dfLDA.index = dfLDA.index.astype(int) + LDAModelsCount
    dfQDA.index = dfQDA.index.astype(int) + QDAModelsCount
    dfRF.index = dfRF.index.astype(int) + RFModelsCount
    dfExtraT.index = dfExtraT.index.astype(int) + ExtraTModelsCount
    dfAdaB.index = dfAdaB.index.astype(int) + AdaBModelsCount
    dfGradB.index = dfGradB.index.astype(int) + GradBModelsCount
    
    dfKNNFiltered = dfKNN.loc[KNNModels, :]
    dfSVCFiltered = dfSVC.loc[SVCModels, :]
    dfGausNBFiltered = dfGausNB.loc[GausNBModels, :]
    dfMLPFiltered = dfMLP.loc[MLPModels, :]
    dfLRFiltered = dfLR.loc[LRModels, :]
    dfLDAFiltered = dfLDA.loc[LDAModels, :]
    dfQDAFiltered = dfQDA.loc[QDAModels, :]
    dfRFFiltered = dfRF.loc[RFModels, :]
    dfExtraTFiltered = dfExtraT.loc[ExtraTModels, :]
    dfAdaBFiltered = dfAdaB.loc[AdaBModels, :]
    dfGradBFiltered = dfGradB.loc[GradBModels, :]

    df_params = pd.concat([dfKNNFiltered, dfSVCFiltered, dfGausNBFiltered, dfMLPFiltered, dfLRFiltered, dfLDAFiltered, dfQDAFiltered, dfRFFiltered, dfExtraTFiltered, dfAdaBFiltered, dfGradBFiltered])
    return df_params

def PreprocessingParamSep():
    dicKNN = json.loads(allParametersPerformancePerModel[1])
    dicSVC = json.loads(allParametersPerformancePerModel[10])
    dicGausNB = json.loads(allParametersPerformancePerModel[19])
    dicMLP = json.loads(allParametersPerformancePerModel[28])
    dicLR = json.loads(allParametersPerformancePerModel[37])
    dicLDA = json.loads(allParametersPerformancePerModel[46])
    dicQDA = json.loads(allParametersPerformancePerModel[55])
    dicRF = json.loads(allParametersPerformancePerModel[64])
    dicExtraT = json.loads(allParametersPerformancePerModel[73])
    dicAdaB = json.loads(allParametersPerformancePerModel[82])
    dicGradB = json.loads(allParametersPerformancePerModel[91])

    dicKNN = dicKNN['params']
    dicSVC = dicSVC['params']
    dicGausNB = dicGausNB['params']
    dicMLP = dicMLP['params']
    dicLR = dicLR['params']
    dicLDA = dicLDA['params']
    dicQDA = dicQDA['params']
    dicRF = dicRF['params']
    dicExtraT = dicExtraT['params']
    dicAdaB = dicAdaB['params']
    dicGradB = dicGradB['params']

    dicKNN = {int(k):v for k,v in dicKNN.items()}
    dicSVC = {int(k):v for k,v in dicSVC.items()}
    dicGausNB = {int(k):v for k,v in dicGausNB.items()}
    dicMLP = {int(k):v for k,v in dicMLP.items()}
    dicLR = {int(k):v for k,v in dicLR.items()}
    dicLDA = {int(k):v for k,v in dicLDA.items()}
    dicQDA = {int(k):v for k,v in dicQDA.items()}
    dicRF = {int(k):v for k,v in dicRF.items()}
    dicExtraT = {int(k):v for k,v in dicExtraT.items()}
    dicAdaB = {int(k):v for k,v in dicAdaB.items()}
    dicGradB = {int(k):v for k,v in dicGradB.items()}

    dfKNN = pd.DataFrame.from_dict(dicKNN)
    dfSVC = pd.DataFrame.from_dict(dicSVC)
    dfGausNB = pd.DataFrame.from_dict(dicGausNB)
    dfMLP = pd.DataFrame.from_dict(dicMLP)
    dfLR = pd.DataFrame.from_dict(dicLR)
    dfLDA = pd.DataFrame.from_dict(dicLDA)
    dfQDA = pd.DataFrame.from_dict(dicQDA)
    dfRF = pd.DataFrame.from_dict(dicRF)
    dfExtraT = pd.DataFrame.from_dict(dicExtraT)
    dfAdaB = pd.DataFrame.from_dict(dicAdaB)
    dfGradB = pd.DataFrame.from_dict(dicGradB)

    dfKNN = dfKNN.T
    dfSVC = dfSVC.T
    dfGausNB = dfGausNB.T
    dfMLP = dfMLP.T
    dfLR = dfLR.T
    dfLDA = dfLDA.T
    dfQDA = dfQDA.T
    dfRF = dfRF.T
    dfExtraT = dfExtraT.T
    dfAdaB = dfAdaB.T
    dfGradB = dfGradB.T

    dfKNN.index = dfKNN.index.astype(int)
    dfSVC.index = dfSVC.index.astype(int) + SVCModelsCount
    dfGausNB.index = dfGausNB.index.astype(int) + GausNBModelsCount
    dfMLP.index = dfMLP.index.astype(int) + MLPModelsCount
    dfLR.index = dfLR.index.astype(int) + LRModelsCount
    dfLDA.index = dfLDA.index.astype(int) + LDAModelsCount
    dfQDA.index = dfQDA.index.astype(int) + QDAModelsCount
    dfRF.index = dfRF.index.astype(int) + RFModelsCount
    dfExtraT.index = dfExtraT.index.astype(int) + ExtraTModelsCount
    dfAdaB.index = dfAdaB.index.astype(int) + AdaBModelsCount
    dfGradB.index = dfGradB.index.astype(int) + GradBModelsCount
    
    dfKNNFiltered = dfKNN.loc[KNNModels, :]
    dfSVCFiltered = dfSVC.loc[SVCModels, :]
    dfGausNBFiltered = dfGausNB.loc[GausNBModels, :]
    dfMLPFiltered = dfMLP.loc[MLPModels, :]
    dfLRFiltered = dfLR.loc[LRModels, :]
    dfLDAFiltered = dfLDA.loc[LDAModels, :]
    dfQDAFiltered = dfQDA.loc[QDAModels, :]
    dfRFFiltered = dfRF.loc[RFModels, :]
    dfExtraTFiltered = dfExtraT.loc[ExtraTModels, :]
    dfAdaBFiltered = dfAdaB.loc[AdaBModels, :]
    dfGradBFiltered = dfGradB.loc[GradBModels, :]

    return [dfKNNFiltered, dfSVCFiltered, dfGausNBFiltered, dfMLPFiltered, dfLRFiltered, dfLDAFiltered, dfQDAFiltered, dfRFFiltered, dfExtraTFiltered, dfAdaBFiltered, dfGradBFiltered]

def preProcessPerClassM():
    dicKNN = json.loads(allParametersPerformancePerModel[2])
    dicSVC = json.loads(allParametersPerformancePerModel[11])
    dicGausNB = json.loads(allParametersPerformancePerModel[20])
    dicMLP = json.loads(allParametersPerformancePerModel[29])
    dicLR = json.loads(allParametersPerformancePerModel[38])
    dicLDA = json.loads(allParametersPerformancePerModel[47])
    dicQDA = json.loads(allParametersPerformancePerModel[56])
    dicRF = json.loads(allParametersPerformancePerModel[65])
    dicExtraT = json.loads(allParametersPerformancePerModel[74])
    dicAdaB = json.loads(allParametersPerformancePerModel[83])
    dicGradB = json.loads(allParametersPerformancePerModel[92])

    dfKNN = pd.DataFrame.from_dict(dicKNN)
    dfSVC = pd.DataFrame.from_dict(dicSVC)
    dfGausNB = pd.DataFrame.from_dict(dicGausNB)
    dfMLP = pd.DataFrame.from_dict(dicMLP)
    dfLR = pd.DataFrame.from_dict(dicLR)
    dfLDA = pd.DataFrame.from_dict(dicLDA)
    dfQDA = pd.DataFrame.from_dict(dicQDA)
    dfRF = pd.DataFrame.from_dict(dicRF)
    dfExtraT = pd.DataFrame.from_dict(dicExtraT)
    dfAdaB = pd.DataFrame.from_dict(dicAdaB)
    dfGradB = pd.DataFrame.from_dict(dicGradB)

    dfKNN.index = dfKNN.index.astype(int)
    dfSVC.index = dfSVC.index.astype(int) + SVCModelsCount
    dfGausNB.index = dfGausNB.index.astype(int) + GausNBModelsCount
    dfMLP.index = dfMLP.index.astype(int) + MLPModelsCount
    dfLR.index = dfLR.index.astype(int) + LRModelsCount
    dfLDA.index = dfLDA.index.astype(int) + LDAModelsCount
    dfQDA.index = dfQDA.index.astype(int) + QDAModelsCount
    dfRF.index = dfRF.index.astype(int) + RFModelsCount
    dfExtraT.index = dfExtraT.index.astype(int) + ExtraTModelsCount
    dfAdaB.index = dfAdaB.index.astype(int) + AdaBModelsCount
    dfGradB.index = dfGradB.index.astype(int) + GradBModelsCount
    
    dfKNNFiltered = dfKNN.loc[KNNModels, :]
    dfSVCFiltered = dfSVC.loc[SVCModels, :]
    dfGausNBFiltered = dfGausNB.loc[GausNBModels, :]
    dfMLPFiltered = dfMLP.loc[MLPModels, :]
    dfLRFiltered = dfLR.loc[LRModels, :]
    dfLDAFiltered = dfLDA.loc[LDAModels, :]
    dfQDAFiltered = dfQDA.loc[QDAModels, :]
    dfRFFiltered = dfRF.loc[RFModels, :]
    dfExtraTFiltered = dfExtraT.loc[ExtraTModels, :]
    dfAdaBFiltered = dfAdaB.loc[AdaBModels, :]
    dfGradBFiltered = dfGradB.loc[GradBModels, :]

    df_concatParams = pd.concat([dfKNNFiltered, dfSVCFiltered, dfGausNBFiltered, dfMLPFiltered, dfLRFiltered, dfLDAFiltered, dfQDAFiltered, dfRFFiltered, dfExtraTFiltered, dfAdaBFiltered, dfGradBFiltered])
    return df_concatParams

def preProcessFeatAcc():
    dicKNN = json.loads(allParametersPerformancePerModel[3])
    dicSVC = json.loads(allParametersPerformancePerModel[12])
    dicGausNB = json.loads(allParametersPerformancePerModel[21])
    dicMLP = json.loads(allParametersPerformancePerModel[30])
    dicLR = json.loads(allParametersPerformancePerModel[39])
    dicLDA = json.loads(allParametersPerformancePerModel[48])
    dicQDA = json.loads(allParametersPerformancePerModel[57])
    dicRF = json.loads(allParametersPerformancePerModel[66])
    dicExtraT = json.loads(allParametersPerformancePerModel[75])
    dicAdaB = json.loads(allParametersPerformancePerModel[84])
    dicGradB = json.loads(allParametersPerformancePerModel[93])

    dfKNN = pd.DataFrame.from_dict(dicKNN)
    dfSVC = pd.DataFrame.from_dict(dicSVC)
    dfGausNB = pd.DataFrame.from_dict(dicGausNB)
    dfMLP = pd.DataFrame.from_dict(dicMLP)
    dfLR = pd.DataFrame.from_dict(dicLR)
    dfLDA = pd.DataFrame.from_dict(dicLDA)
    dfQDA = pd.DataFrame.from_dict(dicQDA)
    dfRF = pd.DataFrame.from_dict(dicRF)
    dfExtraT = pd.DataFrame.from_dict(dicExtraT)
    dfAdaB = pd.DataFrame.from_dict(dicAdaB)
    dfGradB = pd.DataFrame.from_dict(dicGradB)

    dfKNN.index = dfKNN.index.astype(int)
    dfSVC.index = dfSVC.index.astype(int) + SVCModelsCount
    dfGausNB.index = dfGausNB.index.astype(int) + GausNBModelsCount
    dfMLP.index = dfMLP.index.astype(int) + MLPModelsCount
    dfLR.index = dfLR.index.astype(int) + LRModelsCount
    dfLDA.index = dfLDA.index.astype(int) + LDAModelsCount
    dfQDA.index = dfQDA.index.astype(int) + QDAModelsCount
    dfRF.index = dfRF.index.astype(int) + RFModelsCount
    dfExtraT.index = dfExtraT.index.astype(int) + ExtraTModelsCount
    dfAdaB.index = dfAdaB.index.astype(int) + AdaBModelsCount
    dfGradB.index = dfGradB.index.astype(int) + GradBModelsCount
    
    dfKNNFiltered = dfKNN.loc[KNNModels, :]
    dfSVCFiltered = dfSVC.loc[SVCModels, :]
    dfGausNBFiltered = dfGausNB.loc[GausNBModels, :]
    dfMLPFiltered = dfMLP.loc[MLPModels, :]
    dfLRFiltered = dfLR.loc[LRModels, :]
    dfLDAFiltered = dfLDA.loc[LDAModels, :]
    dfQDAFiltered = dfQDA.loc[QDAModels, :]
    dfRFFiltered = dfRF.loc[RFModels, :]
    dfExtraTFiltered = dfExtraT.loc[ExtraTModels, :]
    dfAdaBFiltered = dfAdaB.loc[AdaBModels, :]
    dfGradBFiltered = dfGradB.loc[GradBModels, :]

    df_featAcc = pd.concat([dfKNNFiltered, dfSVCFiltered, dfGausNBFiltered, dfMLPFiltered, dfLRFiltered, dfLDAFiltered, dfQDAFiltered, dfRFFiltered, dfExtraTFiltered, dfAdaBFiltered, dfGradBFiltered])
    return df_featAcc

def preProcessPerm():
    dicKNN = json.loads(allParametersPerformancePerModel[4])
    dicSVC = json.loads(allParametersPerformancePerModel[13])
    dicGausNB = json.loads(allParametersPerformancePerModel[22])
    dicMLP = json.loads(allParametersPerformancePerModel[31])
    dicLR = json.loads(allParametersPerformancePerModel[40])
    dicLDA = json.loads(allParametersPerformancePerModel[49])
    dicQDA = json.loads(allParametersPerformancePerModel[58])
    dicRF = json.loads(allParametersPerformancePerModel[67])
    dicExtraT = json.loads(allParametersPerformancePerModel[76])
    dicAdaB = json.loads(allParametersPerformancePerModel[85])
    dicGradB = json.loads(allParametersPerformancePerModel[94])

    dfKNN = pd.DataFrame.from_dict(dicKNN)
    dfSVC = pd.DataFrame.from_dict(dicSVC)
    dfGausNB = pd.DataFrame.from_dict(dicGausNB)
    dfMLP = pd.DataFrame.from_dict(dicMLP)
    dfLR = pd.DataFrame.from_dict(dicLR)
    dfLDA = pd.DataFrame.from_dict(dicLDA)
    dfQDA = pd.DataFrame.from_dict(dicQDA)
    dfRF = pd.DataFrame.from_dict(dicRF)
    dfExtraT = pd.DataFrame.from_dict(dicExtraT)
    dfAdaB = pd.DataFrame.from_dict(dicAdaB)
    dfGradB = pd.DataFrame.from_dict(dicGradB)

    dfKNN.index = dfKNN.index.astype(int)
    dfSVC.index = dfSVC.index.astype(int) + SVCModelsCount
    dfGausNB.index = dfGausNB.index.astype(int) + GausNBModelsCount
    dfMLP.index = dfMLP.index.astype(int) + MLPModelsCount
    dfLR.index = dfLR.index.astype(int) + LRModelsCount
    dfLDA.index = dfLDA.index.astype(int) + LDAModelsCount
    dfQDA.index = dfQDA.index.astype(int) + QDAModelsCount
    dfRF.index = dfRF.index.astype(int) + RFModelsCount
    dfExtraT.index = dfExtraT.index.astype(int) + ExtraTModelsCount
    dfAdaB.index = dfAdaB.index.astype(int) + AdaBModelsCount
    dfGradB.index = dfGradB.index.astype(int) + GradBModelsCount
    
    dfKNNFiltered = dfKNN.loc[KNNModels, :]
    dfSVCFiltered = dfSVC.loc[SVCModels, :]
    dfGausNBFiltered = dfGausNB.loc[GausNBModels, :]
    dfMLPFiltered = dfMLP.loc[MLPModels, :]
    dfLRFiltered = dfLR.loc[LRModels, :]
    dfLDAFiltered = dfLDA.loc[LDAModels, :]
    dfQDAFiltered = dfQDA.loc[QDAModels, :]
    dfRFFiltered = dfRF.loc[RFModels, :]
    dfExtraTFiltered = dfExtraT.loc[ExtraTModels, :]
    dfAdaBFiltered = dfAdaB.loc[AdaBModels, :]
    dfGradBFiltered = dfGradB.loc[GradBModels, :]

    df_perm = pd.concat([dfKNNFiltered, dfSVCFiltered, dfGausNBFiltered, dfMLPFiltered, dfLRFiltered, dfLDAFiltered, dfQDAFiltered, dfRFFiltered, dfExtraTFiltered, dfAdaBFiltered, dfGradBFiltered])
    return df_perm

def preProcessFeatSc():
    dicKNN = json.loads(allParametersPerformancePerModel[5])
    dfKNN = pd.DataFrame.from_dict(dicKNN)
    return dfKNN

# remove that maybe!
def preProcsumPerMetric(factors):
    sumPerClassifier = []
    loopThroughMetrics = PreprocessingMetrics()
    loopThroughMetrics = loopThroughMetrics.fillna(0)
    loopThroughMetrics.loc[:, 'log_loss'] = 1 - loopThroughMetrics.loc[:, 'log_loss']
    for row in loopThroughMetrics.iterrows():
        rowSum = 0
        name, values = row
        for loop, elements in enumerate(values):
            rowSum = elements*factors[loop] + rowSum
        if sum(factors) is 0:
            sumPerClassifier = 0
        else:
            sumPerClassifier.append(rowSum/sum(factors) * 100)
    return sumPerClassifier

def preProcMetricsAllAndSel():
    loopThroughMetrics = PreprocessingMetrics()
    loopThroughMetrics = loopThroughMetrics.fillna(0)
    global factors
    metricsPerModelColl = []
    metricsPerModelColl.append(loopThroughMetrics['mean_test_accuracy'])
    metricsPerModelColl.append(loopThroughMetrics['geometric_mean_score_micro'])
    metricsPerModelColl.append(loopThroughMetrics['geometric_mean_score_macro'])
    metricsPerModelColl.append(loopThroughMetrics['geometric_mean_score_weighted'])
    metricsPerModelColl.append(loopThroughMetrics['mean_test_precision_micro'])
    metricsPerModelColl.append(loopThroughMetrics['mean_test_precision_macro'])
    metricsPerModelColl.append(loopThroughMetrics['mean_test_precision_weighted'])
    metricsPerModelColl.append(loopThroughMetrics['mean_test_recall_micro'])
    metricsPerModelColl.append(loopThroughMetrics['mean_test_recall_macro'])
    metricsPerModelColl.append(loopThroughMetrics['mean_test_recall_weighted'])
    metricsPerModelColl.append(loopThroughMetrics['f5_micro'])
    metricsPerModelColl.append(loopThroughMetrics['f5_macro'])
    metricsPerModelColl.append(loopThroughMetrics['f5_weighted'])
    metricsPerModelColl.append(loopThroughMetrics['f1_micro'])
    metricsPerModelColl.append(loopThroughMetrics['f1_macro'])
    metricsPerModelColl.append(loopThroughMetrics['f1_weighted'])
    metricsPerModelColl.append(loopThroughMetrics['f2_micro'])
    metricsPerModelColl.append(loopThroughMetrics['f2_macro'])
    metricsPerModelColl.append(loopThroughMetrics['f2_weighted'])
    metricsPerModelColl.append(loopThroughMetrics['matthews_corrcoef'])
    metricsPerModelColl.append(loopThroughMetrics['mean_test_roc_auc_ovo_weighted'])
    metricsPerModelColl.append(loopThroughMetrics['log_loss'])
    f=lambda a: (abs(a)+a)/2
    for index, metric in enumerate(metricsPerModelColl):
        if (index == 19):
            metricsPerModelColl[index] = ((f(metric))*factors[index]) * 100
        elif (index == 21):
            metricsPerModelColl[index] = ((1 - metric)*factors[index] ) * 100
        else:  
            metricsPerModelColl[index] = (metric*factors[index]) * 100
        metricsPerModelColl[index] = metricsPerModelColl[index].to_json()
    return metricsPerModelColl

def preProceModels():
    models = KNNModels + SVCModels + GausNBModels + MLPModels + LRModels + LDAModels + QDAModels + RFModels + ExtraTModels + AdaBModels + GradBModels
    return models

def FunMDS (data):
    mds = MDS(n_components=2, random_state=RANDOM_SEED)
    XTransformed = mds.fit_transform(data).T
    XTransformed = XTransformed.tolist()
    return XTransformed

def FunTsne (data):
    tsne = TSNE(n_components=2, random_state=RANDOM_SEED).fit_transform(data)
    tsne.shape
    return tsne

def FunUMAP (data):
    trans = umap.UMAP(n_neighbors=15, random_state=RANDOM_SEED).fit(data)
    Xpos = trans.embedding_[:, 0].tolist()
    Ypos = trans.embedding_[:, 1].tolist()
    return [Xpos,Ypos]

def InitializeEnsemble(): 
    XModels = PreprocessingMetrics()
    global ModelSpaceMDS
    global ModelSpaceTSNE
    global allParametersPerformancePerModel
    global impDataInst
    
    XModels = XModels.fillna(0)

    ModelSpaceMDS = FunMDS(XModels)
    ModelSpaceTSNE = FunTsne(XModels)
    ModelSpaceTSNE = ModelSpaceTSNE.tolist()
    ModelSpaceUMAP = FunUMAP(XModels)

    PredictionProbSel = PreprocessingPred()
    PredictionSpaceMDS = FunMDS(PredictionProbSel)
    PredictionSpaceTSNE = FunTsne(PredictionProbSel)
    PredictionSpaceTSNE = PredictionSpaceTSNE.tolist()
    PredictionSpaceUMAP = FunUMAP(PredictionProbSel)

    ModelsIDs = preProceModels()
    
    impDataInst = processDataInstance(ModelsIDs,allParametersPerformancePerModel)

    callPreResults()

    key = 0
    EnsembleModel(ModelsIDs, key)

    ReturnResults(ModelSpaceMDS,ModelSpaceTSNE,ModelSpaceUMAP,PredictionSpaceMDS,PredictionSpaceTSNE,PredictionSpaceUMAP)

def processDataInstance(ModelsIDs, allParametersPerformancePerModel):
    dicKNN = json.loads(allParametersPerformancePerModel[8])
    dicKNN = json.loads(dicKNN)
    dicSVC = json.loads(allParametersPerformancePerModel[17])
    dicSVC = json.loads(dicSVC)
    dicGausNB = json.loads(allParametersPerformancePerModel[26])
    dicGausNB = json.loads(dicGausNB)
    dicMLP = json.loads(allParametersPerformancePerModel[35])
    dicMLP = json.loads(dicMLP)
    dicLR = json.loads(allParametersPerformancePerModel[44])
    dicLR = json.loads(dicLR)
    dicLDA = json.loads(allParametersPerformancePerModel[53])
    dicLDA = json.loads(dicLDA)
    dicQDA = json.loads(allParametersPerformancePerModel[62])
    dicQDA = json.loads(dicQDA)
    dicRF = json.loads(allParametersPerformancePerModel[71])
    dicRF = json.loads(dicRF)
    dicExtraT = json.loads(allParametersPerformancePerModel[80])
    dicExtraT = json.loads(dicExtraT)
    dicAdaB = json.loads(allParametersPerformancePerModel[89])
    dicAdaB = json.loads(dicAdaB)
    dicGradB = json.loads(allParametersPerformancePerModel[98])
    dicGradB = json.loads(dicGradB)

    dfKNN = pd.DataFrame.from_dict(dicKNN)
    dfSVC = pd.DataFrame.from_dict(dicSVC)
    dfGausNB = pd.DataFrame.from_dict(dicGausNB)
    dfMLP = pd.DataFrame.from_dict(dicMLP)
    dfLR = pd.DataFrame.from_dict(dicLR)
    dfLDA = pd.DataFrame.from_dict(dicLDA)
    dfQDA = pd.DataFrame.from_dict(dicQDA)
    dfRF = pd.DataFrame.from_dict(dicRF)
    dfExtraT = pd.DataFrame.from_dict(dicExtraT)
    dfAdaB = pd.DataFrame.from_dict(dicAdaB)
    dfGradB = pd.DataFrame.from_dict(dicGradB)

    dfKNN.index = dfKNN.index.astype(int)
    dfSVC.index = dfSVC.index.astype(int) + SVCModelsCount
    dfGausNB.index = dfGausNB.index.astype(int) + GausNBModelsCount
    dfMLP.index = dfMLP.index.astype(int) + MLPModelsCount
    dfLR.index = dfLR.index.astype(int) + LRModelsCount
    dfLDA.index = dfLDA.index.astype(int) + LDAModelsCount
    dfQDA.index = dfQDA.index.astype(int) + QDAModelsCount
    dfRF.index = dfRF.index.astype(int) + RFModelsCount
    dfExtraT.index = dfExtraT.index.astype(int) + ExtraTModelsCount
    dfAdaB.index = dfAdaB.index.astype(int) + AdaBModelsCount
    dfGradB.index = dfGradB.index.astype(int) + GradBModelsCount

    dfKNNFiltered = dfKNN.loc[KNNModels, :]
    dfSVCFiltered = dfSVC.loc[SVCModels, :]
    dfGausNBFiltered = dfGausNB.loc[GausNBModels, :]
    dfMLPFiltered = dfMLP.loc[MLPModels, :]
    dfLRFiltered = dfLR.loc[LRModels, :]
    dfLDAFiltered = dfLDA.loc[LDAModels, :]
    dfQDAFiltered = dfQDA.loc[QDAModels, :]
    dfRFFiltered = dfRF.loc[RFModels, :]
    dfExtraTFiltered = dfExtraT.loc[ExtraTModels, :]
    dfAdaBFiltered = dfAdaB.loc[AdaBModels, :]
    dfGradBFiltered = dfGradB.loc[GradBModels, :]

    df_connect = pd.concat([dfKNNFiltered, dfSVCFiltered, dfGausNBFiltered, dfMLPFiltered, dfLRFiltered, dfLDAFiltered, dfQDAFiltered, dfRFFiltered, dfExtraTFiltered, dfAdaBFiltered, dfGradBFiltered])
    global yData
    countCorrect = []
    length = len(df_connect.index)
    for index, element in enumerate(yData):
        countTemp = 0
        dfPart = df_connect[[str(index)]]
        for indexdf, row in dfPart.iterrows():
            if (int(row.values[0]) == int(element)):
                countTemp += 1
        countCorrect.append(1 - (countTemp/length))
    return countCorrect

def ReturnResults(ModelSpaceMDS,ModelSpaceTSNE,ModelSpaceUMAP,PredictionSpaceMDS,PredictionSpaceTSNE,PredictionSpaceUMAP):

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
    Results.append(0) # Position: 7
    Results.append(json.dumps(PredictionSpaceMDS)) # Position: 8 
    Results.append(json.dumps(metricsPerModel)) # Position: 9
    Results.append(perm_imp_eli5PDCon) # Position: 10
    Results.append(featureScoresCon) # Position: 11
    Results.append(json.dumps(ModelSpaceTSNE)) # Position: 12
    Results.append(json.dumps(ModelsIDs)) # Position: 13
    Results.append(json.dumps(XDataJSONEntireSet)) # Position: 14
    Results.append(json.dumps(yData)) # Position: 15
    Results.append(json.dumps(AllTargets)) # Position: 16
    Results.append(json.dumps(ModelSpaceUMAP)) # Position: 17
    Results.append(json.dumps(PredictionSpaceTSNE)) # Position: 18
    Results.append(json.dumps(PredictionSpaceUMAP)) # Position: 19

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
    print(ClassifierIDsList)
    print(PredictionProbSelUpdate)

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
    ClassifierIDCleaned = json.loads(ClassifierIDsList)
    
    global keySpecInternal
    keySpecInternal = 1
    keySpecInternal = ClassifierIDCleaned['keyNow']

    EnsembleModel(ClassifierIDsList, 1)
    return 'Everything Okay'

def ComputeMetricsForSel(Models):
    Models = json.loads(Models)
    MetricsAlltoSel = PreprocessingMetrics()

    listofModels = []
    for loop in Models['ClassifiersList']:
        listofModels.append(loop)
    MetricsAlltoSel = MetricsAlltoSel.loc[listofModels,:]

    global metricsPerModelCollSel
    global factors
    metricsPerModelCollSel = []
    metricsPerModelCollSel.append(MetricsAlltoSel['mean_test_accuracy'])
    metricsPerModelCollSel.append(MetricsAlltoSel['geometric_mean_score_micro'])
    metricsPerModelCollSel.append(MetricsAlltoSel['geometric_mean_score_macro'])
    metricsPerModelCollSel.append(MetricsAlltoSel['geometric_mean_score_weighted'])
    metricsPerModelCollSel.append(MetricsAlltoSel['mean_test_precision_micro'])
    metricsPerModelCollSel.append(MetricsAlltoSel['mean_test_precision_macro'])
    metricsPerModelCollSel.append(MetricsAlltoSel['mean_test_precision_weighted'])
    metricsPerModelCollSel.append(MetricsAlltoSel['mean_test_recall_micro'])
    metricsPerModelCollSel.append(MetricsAlltoSel['mean_test_recall_macro'])
    metricsPerModelCollSel.append(MetricsAlltoSel['mean_test_recall_weighted'])
    metricsPerModelCollSel.append(MetricsAlltoSel['f5_micro'])
    metricsPerModelCollSel.append(MetricsAlltoSel['f5_macro'])
    metricsPerModelCollSel.append(MetricsAlltoSel['f5_weighted'])
    metricsPerModelCollSel.append(MetricsAlltoSel['f1_micro'])
    metricsPerModelCollSel.append(MetricsAlltoSel['f1_macro'])
    metricsPerModelCollSel.append(MetricsAlltoSel['f1_weighted'])
    metricsPerModelCollSel.append(MetricsAlltoSel['f2_micro'])
    metricsPerModelCollSel.append(MetricsAlltoSel['f2_macro'])
    metricsPerModelCollSel.append(MetricsAlltoSel['f2_weighted'])
    metricsPerModelCollSel.append(MetricsAlltoSel['matthews_corrcoef'])
    metricsPerModelCollSel.append(MetricsAlltoSel['mean_test_roc_auc_ovo_weighted'])
    metricsPerModelCollSel.append(MetricsAlltoSel['log_loss'])
    f=lambda a: (abs(a)+a)/2
    for index, metric in enumerate(metricsPerModelCollSel):
        if (index == 19):
            metricsPerModelCollSel[index] = ((f(metric))*factors[index]) * 100
        elif (index == 21):
            metricsPerModelCollSel[index] = (1 - metric)*factors[index] * 100
        else:  
            metricsPerModelCollSel[index] = metric*factors[index] * 100
        metricsPerModelCollSel[index] = metricsPerModelCollSel[index].to_json()
    return 'okay'

# function to get unique values 
def unique(list1): 
  
    # intilize a null list 
    unique_list = [] 
      
    # traverse for all elements 
    for x in list1: 
        # check if exists in unique_list or not 
        if x not in unique_list: 
            unique_list.append(x) 
    return unique_list

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
    global algorithmsList

    paramsListSepPD = []
    paramsListSepPD = PreprocessingParamSep()

    paramsListSeptoDicKNN = paramsListSepPD[0].to_dict(orient='list')
    paramsListSeptoDicSVC = paramsListSepPD[1].to_dict(orient='list')
    paramsListSeptoDicGausNB = paramsListSepPD[2].to_dict(orient='list')
    paramsListSeptoDicMLP = paramsListSepPD[3].to_dict(orient='list')
    paramsListSeptoDicLR = paramsListSepPD[4].to_dict(orient='list')
    paramsListSeptoDicLDA = paramsListSepPD[5].to_dict(orient='list')
    paramsListSeptoDicQDA = paramsListSepPD[6].to_dict(orient='list')
    paramsListSeptoDicRF = paramsListSepPD[7].to_dict(orient='list')
    paramsListSeptoDicExtraT = paramsListSepPD[8].to_dict(orient='list')
    paramsListSeptoDicAdaB = paramsListSepPD[9].to_dict(orient='list')
    paramsListSeptoDicGradB = paramsListSepPD[10].to_dict(orient='list')

    RetrieveParamsCleared = {}
    RetrieveParamsClearedListKNN = []
    for key, value in paramsListSeptoDicKNN.items():
        withoutDuplicates = Remove(value)
        RetrieveParamsCleared[key] = withoutDuplicates
    RetrieveParamsClearedListKNN.append(RetrieveParamsCleared)

    RetrieveParamsCleared = {}
    RetrieveParamsClearedListSVC = []
    for key, value in paramsListSeptoDicSVC.items():
        withoutDuplicates = Remove(value)
        RetrieveParamsCleared[key] = withoutDuplicates
    RetrieveParamsClearedListSVC.append(RetrieveParamsCleared)
    RetrieveParamsCleared = {}
    RetrieveParamsClearedListGausNB = []
    for key, value in paramsListSeptoDicGausNB.items():
        withoutDuplicates = Remove(value)
        RetrieveParamsCleared[key] = withoutDuplicates
    RetrieveParamsClearedListGausNB.append(RetrieveParamsCleared)

    RetrieveParamsCleared = {}
    RetrieveParamsClearedListMLP = []
    for key, value in paramsListSeptoDicMLP.items():
        withoutDuplicates = Remove(value)
        RetrieveParamsCleared[key] = withoutDuplicates
    RetrieveParamsClearedListMLP.append(RetrieveParamsCleared)

    RetrieveParamsCleared = {}
    RetrieveParamsClearedListLR = []
    for key, value in paramsListSeptoDicLR.items():
        withoutDuplicates = Remove(value)
        RetrieveParamsCleared[key] = withoutDuplicates
    RetrieveParamsClearedListLR.append(RetrieveParamsCleared)

    RetrieveParamsCleared = {}
    RetrieveParamsClearedListLDA = []
    for key, value in paramsListSeptoDicLDA.items():
        withoutDuplicates = Remove(value)
        RetrieveParamsCleared[key] = withoutDuplicates
    RetrieveParamsClearedListLDA.append(RetrieveParamsCleared)

    RetrieveParamsCleared = {}
    RetrieveParamsClearedListQDA = []
    for key, value in paramsListSeptoDicQDA.items():
        withoutDuplicates = Remove(value)
        RetrieveParamsCleared[key] = withoutDuplicates
    RetrieveParamsClearedListQDA.append(RetrieveParamsCleared)

    RetrieveParamsCleared = {}
    RetrieveParamsClearedListRF = []
    for key, value in paramsListSeptoDicRF.items():
        withoutDuplicates = Remove(value)
        RetrieveParamsCleared[key] = withoutDuplicates
    RetrieveParamsClearedListRF.append(RetrieveParamsCleared)

    RetrieveParamsCleared = {}
    RetrieveParamsClearedListExtraT = []
    for key, value in paramsListSeptoDicExtraT.items():
        withoutDuplicates = Remove(value)
        RetrieveParamsCleared[key] = withoutDuplicates
    RetrieveParamsClearedListExtraT.append(RetrieveParamsCleared)

    RetrieveParamsCleared = {}
    RetrieveParamsClearedListAdaB = []
    for key, value in paramsListSeptoDicAdaB.items():
        withoutDuplicates = Remove(value)
        RetrieveParamsCleared[key] = withoutDuplicates
    RetrieveParamsClearedListAdaB.append(RetrieveParamsCleared)

    RetrieveParamsCleared = {}
    RetrieveParamsClearedListGradB = []
    for key, value in paramsListSeptoDicGradB.items():
        withoutDuplicates = Remove(value)
        RetrieveParamsCleared[key] = withoutDuplicates
    RetrieveParamsClearedListGradB.append(RetrieveParamsCleared)

    if (len(paramsListSeptoDicKNN['n_neighbors']) is 0):
        RetrieveParamsClearedListKNN = []

    if (len(paramsListSeptoDicSVC['C']) is 0):
        RetrieveParamsClearedListSVC = []

    if (len(paramsListSeptoDicGausNB['var_smoothing']) is 0):
        RetrieveParamsClearedListGausNB = []

    if (len(paramsListSeptoDicMLP['alpha']) is 0):
        RetrieveParamsClearedListMLP = []

    if (len(paramsListSeptoDicLR['C']) is 0):
        RetrieveParamsClearedListLR = []

    if (len(paramsListSeptoDicLDA['shrinkage']) is 0):
        RetrieveParamsClearedListLDA = []

    if (len(paramsListSeptoDicQDA['reg_param']) is 0):
        RetrieveParamsClearedListQDA = []

    if (len(paramsListSeptoDicRF['n_estimators']) is 0):
        RetrieveParamsClearedListRF = []

    if (len(paramsListSeptoDicExtraT['n_estimators']) is 0):
        RetrieveParamsClearedListExtraT = []

    if (len(paramsListSeptoDicAdaB['n_estimators']) is 0):
        RetrieveParamsClearedListAdaB = []

    if (len(paramsListSeptoDicGradB['n_estimators']) is 0):
        RetrieveParamsClearedListGradB = []
    for eachAlgor in algorithms:
        if (eachAlgor) == 'KNN':
            clf = KNeighborsClassifier()
            params = RetrieveParamsClearedListKNN
            AlgorithmsIDsEnd = 0
        elif (eachAlgor) == 'SVC':
            clf = SVC(probability=True,random_state=RANDOM_SEED)
            params = RetrieveParamsClearedListSVC
            AlgorithmsIDsEnd = SVCModelsCount
        elif (eachAlgor) == 'GausNB':
            clf = GaussianNB()
            params = RetrieveParamsClearedListGausNB
            AlgorithmsIDsEnd = GausNBModelsCount
        elif (eachAlgor) == 'MLP':
            clf = MLPClassifier(random_state=RANDOM_SEED)
            params = RetrieveParamsClearedListMLP
            AlgorithmsIDsEnd = MLPModelsCount
        elif (eachAlgor) == 'LR':
            clf = LogisticRegression(random_state=RANDOM_SEED)
            params = RetrieveParamsClearedListLR
            AlgorithmsIDsEnd = LRModelsCount
        elif (eachAlgor) == 'LDA':
            clf = LinearDiscriminantAnalysis()
            params = RetrieveParamsClearedListLDA
            AlgorithmsIDsEnd = LDAModelsCount
        elif (eachAlgor) == 'QDA':
            clf = QuadraticDiscriminantAnalysis()
            params = RetrieveParamsClearedListQDA
            AlgorithmsIDsEnd = QDAModelsCount
        elif (eachAlgor) == 'RF':
            clf = RandomForestClassifier(random_state=RANDOM_SEED)
            params = RetrieveParamsClearedListRF
            AlgorithmsIDsEnd = RFModelsCount
        elif (eachAlgor) == 'ExtraT':
            clf = ExtraTreesClassifier(random_state=RANDOM_SEED)
            params = RetrieveParamsClearedListExtraT
            AlgorithmsIDsEnd = ExtraTModelsCount
        elif (eachAlgor) == 'AdaB':
            clf = AdaBoostClassifier(random_state=RANDOM_SEED)
            params = RetrieveParamsClearedListGradB
            AlgorithmsIDsEnd = AdaBModelsCount
        else: 
            clf = GradientBoostingClassifier(random_state=RANDOM_SEED)
            params = RetrieveParamsClearedListGradB
            AlgorithmsIDsEnd = GradBModelsCount
        metricsSelList = GridSearchSel(clf, params, factors, AlgorithmsIDsEnd, listofDataPoints)
    if (len(metricsSelList[0]) != 0 and len(metricsSelList[1]) != 0 and len(metricsSelList[2]) != 0 and len(metricsSelList[3]) != 0 and len(metricsSelList[4]) != 0 and len(metricsSelList[5]) != 0 and len(metricsSelList[6]) != 0 and len(metricsSelList[7]) != 0 and len(metricsSelList[8]) != 0 and len(metricsSelList[9]) != 0 and len(metricsSelList[10]) != 0):
        dicKNN = json.loads(metricsSelList[0])
        dfKNN = pd.DataFrame.from_dict(dicKNN)
        parametersSelDataPD = parametersSelData[0].apply(pd.Series)
        set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[0], paramsListSepPD[0]]).drop_duplicates(keep=False)
        set_diff_df = set_diff_df.index.tolist()
        if (len(set_diff_df) == 0):
            dfKNNCleared = dfKNN
        else:
            dfKNNCleared = dfKNN.drop(dfKNN.index[set_diff_df])

        dicSVC = json.loads(metricsSelList[1])
        dfSVC = pd.DataFrame.from_dict(dicSVC)
        parametersSelDataPD = parametersSelData[1].apply(pd.Series)
        set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[1], paramsListSepPD[1]]).drop_duplicates(keep=False)
        set_diff_df = set_diff_df.index.tolist()
        if (len(set_diff_df) == 0):
            dfSVCCleared = dfSVC
        else:
            dfSVCCleared = dfSVC.drop(dfSVC.index[set_diff_df])

        dicGausNB = json.loads(metricsSelList[2])
        dfGausNB = pd.DataFrame.from_dict(dicGausNB)
        parametersSelDataPD = parametersSelData[2].apply(pd.Series)
        set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[2], paramsListSepPD[2]]).drop_duplicates(keep=False)
        set_diff_df = set_diff_df.index.tolist()
        if (len(set_diff_df) == 0):
            dfGausNBCleared = dfGausNB
        else:
            dfGausNBCleared = dfGausNB.drop(dfGausNB.index[set_diff_df])

        dicMLP = json.loads(metricsSelList[3])
        dfMLP = pd.DataFrame.from_dict(dicMLP)
        parametersSelDataPD = parametersSelData[3].apply(pd.Series)
        set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[3], paramsListSepPD[3]]).drop_duplicates(keep=False)
        set_diff_df = set_diff_df.index.tolist()
        if (len(set_diff_df) == 0):
            dfMLPCleared = dfMLP
        else:
            dfMLPCleared = dfMLP.drop(dfMLP.index[set_diff_df])

        dicLR = json.loads(metricsSelList[4])
        dfLR = pd.DataFrame.from_dict(dicLR)
        parametersSelDataPD = parametersSelData[4].apply(pd.Series)
        set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[4], paramsListSepPD[4]]).drop_duplicates(keep=False)
        set_diff_df = set_diff_df.index.tolist()
        if (len(set_diff_df) == 0):
            dfLRCleared = dfLR
        else:
            dfLRCleared = dfLR.drop(dfLR.index[set_diff_df])

        dicLDA = json.loads(metricsSelList[5])
        dfLDA = pd.DataFrame.from_dict(dicLDA)
        parametersSelDataPD = parametersSelData[5].apply(pd.Series)
        set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[5], paramsListSepPD[5]]).drop_duplicates(keep=False)
        set_diff_df = set_diff_df.index.tolist()
        if (len(set_diff_df) == 0):
            dfLDACleared = dfLDA
        else:
            dfLDACleared = dfLDA.drop(dfLDA.index[set_diff_df])

        dicQDA = json.loads(metricsSelList[6])
        dfQDA = pd.DataFrame.from_dict(dicQDA)
        parametersSelDataPD = parametersSelData[6].apply(pd.Series)
        set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[6], paramsListSepPD[6]]).drop_duplicates(keep=False)
        set_diff_df = set_diff_df.index.tolist()
        if (len(set_diff_df) == 0):
            dfQDACleared = dfQDA
        else:
            dfQDACleared = dfQDA.drop(dfQDA.index[set_diff_df])

        dicRF = json.loads(metricsSelList[7])
        dfRF = pd.DataFrame.from_dict(dicRF)
        parametersSelDataPD = parametersSelData[7].apply(pd.Series)
        set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[7], paramsListSepPD[7]]).drop_duplicates(keep=False)
        set_diff_df = set_diff_df.index.tolist()
        if (len(set_diff_df) == 0):
            dfRFCleared = dfRF
        else:
            dfRFCleared = dfRF.drop(dfRF.index[set_diff_df])

        dicExtraT = json.loads(metricsSelList[8])
        dfExtraT = pd.DataFrame.from_dict(dicExtraT)
        parametersSelDataPD = parametersSelData[8].apply(pd.Series)
        set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[8], paramsListSepPD[8]]).drop_duplicates(keep=False)
        set_diff_df = set_diff_df.index.tolist()
        if (len(set_diff_df) == 0):
            dfExtraTCleared = dfExtraT
        else:
            dfExtraTCleared = dfExtraT.drop(dfExtraT.index[set_diff_df])

        dicAdaB = json.loads(metricsSelList[9])
        dfAdaB = pd.DataFrame.from_dict(dicAdaB)
        parametersSelDataPD = parametersSelData[9].apply(pd.Series)
        set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[9], paramsListSepPD[9]]).drop_duplicates(keep=False)
        set_diff_df = set_diff_df.index.tolist()
        if (len(set_diff_df) == 0):
            dfAdaBCleared = dfAdaB
        else:
            dfAdaBCleared = dfAdaB.drop(dfAdaB.index[set_diff_df])

        dicGradB = json.loads(metricsSelList[10])
        dfGradB = pd.DataFrame.from_dict(dicGradB)
        parametersSelDataPD = parametersSelData[10].apply(pd.Series)
        set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[10], paramsListSepPD[10]]).drop_duplicates(keep=False)
        set_diff_df = set_diff_df.index.tolist()
        if (len(set_diff_df) == 0):
            dfGradBCleared = dfGradB
        else:
            dfGradBCleared = dfGradB.drop(dfGradB.index[set_diff_df])

        df_concatMetrics = pd.concat([dfKNNCleared, dfSVCCleared, dfGausNBCleared, dfMLPCleared, dfLRCleared, dfLDACleared, dfQDACleared, dfRFCleared, dfExtraTCleared, dfAdaBCleared, dfGradBCleared])
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
        elif (len(metricsSelList[1]) != 0):
            dicSVC = json.loads(metricsSelList[1])
            dfSVC = pd.DataFrame.from_dict(dicSVC)
            parametersSelDataPD = parametersSelData[1].apply(pd.Series)
            set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[1], paramsListSepPD[1]]).drop_duplicates(keep=False)
            set_diff_df = set_diff_df.index.tolist()
            if (len(set_diff_df) == 0):
                dfSVCCleared = dfSVC
            else:
                dfSVCCleared = dfSVC.drop(dfSVC.index[set_diff_df])
            df_concatMetrics = dfSVCCleared
        elif (len(metricsSelList[2]) != 0):
            dicGausNB = json.loads(metricsSelList[2])
            dfGausNB = pd.DataFrame.from_dict(dicGausNB)
            parametersSelDataPD = parametersSelData[2].apply(pd.Series)
            set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[2], paramsListSepPD[2]]).drop_duplicates(keep=False)
            set_diff_df = set_diff_df.index.tolist()
            if (len(set_diff_df) == 0):
                dfGausNBCleared = dfGausNB
            else:
                dfGausNBCleared = dfGausNB.drop(dfGausNB.index[set_diff_df])
            df_concatMetrics = dfGausNBCleared
        elif (len(metricsSelList[3]) != 0):
            dicMLP = json.loads(metricsSelList[3])
            dfMLP = pd.DataFrame.from_dict(dicMLP)
            parametersSelDataPD = parametersSelData[3].apply(pd.Series)
            set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[3], paramsListSepPD[3]]).drop_duplicates(keep=False)
            set_diff_df = set_diff_df.index.tolist()
            if (len(set_diff_df) == 0):
                dfMLPCleared = dfMLP
            else:
                dfMLPCleared = dfMLP.drop(dfMLP.index[set_diff_df])
            df_concatMetrics = dfMLPCleared
        elif (len(metricsSelList[4]) != 0):
            dicLR = json.loads(metricsSelList[4])
            dfLR = pd.DataFrame.from_dict(dicLR)
            parametersSelDataPD = parametersSelData[4].apply(pd.Series)
            set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[4], paramsListSepPD[4]]).drop_duplicates(keep=False)
            set_diff_df = set_diff_df.index.tolist()
            if (len(set_diff_df) == 0):
                dfLRCleared = dfLR
            else:
                dfLRCleared = dfLR.drop(dfLR.index[set_diff_df])
            df_concatMetrics = dfLRCleared
        elif (len(metricsSelList[5]) != 0):
            dicLDA = json.loads(metricsSelList[5])
            dfLDA = pd.DataFrame.from_dict(dicLDA)
            parametersSelDataPD = parametersSelData[5].apply(pd.Series)
            set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[5], paramsListSepPD[5]]).drop_duplicates(keep=False)
            set_diff_df = set_diff_df.index.tolist()
            if (len(set_diff_df) == 0):
                dfLDACleared = dfLDA
            else:
                dfLDACleared = dfLDA.drop(dfLDA.index[set_diff_df])
            df_concatMetrics = dfLDACleared
        elif (len(metricsSelList[6]) != 0):
            dicQDA = json.loads(metricsSelList[6])
            dfQDA = pd.DataFrame.from_dict(dicQDA)
            parametersSelDataPD = parametersSelData[6].apply(pd.Series)
            set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[6], paramsListSepPD[6]]).drop_duplicates(keep=False)
            set_diff_df = set_diff_df.index.tolist()
            if (len(set_diff_df) == 0):
                dfQDACleared = dfQDA
            else:
                dfQDACleared = dfQDA.drop(dfQDA.index[set_diff_df])
            df_concatMetrics = dfQDACleared
        elif (len(metricsSelList[7]) != 0):
            dicRF = json.loads(metricsSelList[7])
            dfRF = pd.DataFrame.from_dict(dicRF)
            parametersSelDataPD = parametersSelData[7].apply(pd.Series)
            set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[7], paramsListSepPD[7]]).drop_duplicates(keep=False)
            set_diff_df = set_diff_df.index.tolist()
            if (len(set_diff_df) == 0):
                dfRFCleared = dfRF
            else:
                dfRFCleared = dfRF.drop(dfRF.index[set_diff_df])
            df_concatMetrics = dfRFCleared
        elif (len(metricsSelList[8]) != 0):
            dicExtraT = json.loads(metricsSelList[8])
            dfExtraT = pd.DataFrame.from_dict(dicExtraT)
            parametersSelDataPD = parametersSelData[8].apply(pd.Series)
            set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[8], paramsListSepPD[8]]).drop_duplicates(keep=False)
            set_diff_df = set_diff_df.index.tolist()
            if (len(set_diff_df) == 0):
                dfExtraTCleared = dfExtraT
            else:
                dfExtraTCleared = dfExtraT.drop(dfExtraT.index[set_diff_df])
            df_concatMetrics = dfExtraTCleared
        elif (len(metricsSelList[9]) != 0):
            dicAdaB = json.loads(metricsSelList[9])
            dfAdaB = pd.DataFrame.from_dict(dicAdaB)
            parametersSelDataPD = parametersSelData[9].apply(pd.Series)
            set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[9], paramsListSepPD[9]]).drop_duplicates(keep=False)
            set_diff_df = set_diff_df.index.tolist()
            if (len(set_diff_df) == 0):
                dfAdaBCleared = dfAdaB
            else:
                dfAdaBCleared = dfAdaB.drop(dfAdaB.index[set_diff_df])
            df_concatMetrics = dfAdaBCleared
        else:
            dicGradB = json.loads(metricsSelList[10])
            dfGradB = pd.DataFrame.from_dict(dicGradB)
            parametersSelDataPD = parametersSelData[10].apply(pd.Series)
            set_diff_df = pd.concat([parametersSelDataPD, paramsListSepPD[10], paramsListSepPD[10]]).drop_duplicates(keep=False)
            set_diff_df = set_diff_df.index.tolist()
            if (len(set_diff_df) == 0):
                dfAdaBCleared = dfGradB
            else:
                dfAdaBCleared = dfGradB.drop(dfGradB.index[set_diff_df])
            df_concatMetrics = dfAdaBCleared
    
    global foreachMetricResults
    foreachMetricResults = []
    foreachMetricResults = preProcSumForEachMetric(factors, df_concatMetrics)

    df_concatMetrics.loc[:, 'log_loss'] = 1 - df_concatMetrics.loc[:, 'log_loss']

    global sumPerClassifierSelUpdate
    sumPerClassifierSelUpdate = []
    sumPerClassifierSelUpdate = preProcsumPerMetricAccordingtoData(factors, df_concatMetrics)

    ModelSpaceMDSNewComb = [list(a) for a in  zip(ModelSpaceMDS[0], ModelSpaceMDS[1])]
    # fix that for tsne and UMAP
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
        metrics = metrics.filter(['mean_test_accuracy','mean_test_precision_micro','mean_test_precision_macro','mean_test_precision_weighted','mean_test_recall_micro','mean_test_recall_macro','mean_test_recall_weighted','mean_test_roc_auc_ovo_weighted']) 
        
        # concat parameters and performance
        parametersPerformancePerModel = pd.DataFrame(df_cv_results_classifiers['params'])
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
        resultsMicro = []
        resultsMacro = []
        resultsWeighted = []
        resultsCorrCoef = []
        resultsMicroBeta5 = []
        resultsMacroBeta5 = []
        resultsWeightedBeta5 = []
        resultsMicroBeta1 = []
        resultsMacroBeta1 = []
        resultsWeightedBeta1 = []
        resultsMicroBeta2 = []
        resultsMacroBeta2 = []
        resultsWeightedBeta2 = []
        resultsLogLoss = []
        resultsLogLossFinal = []

        loop = 8

        for eachModelParameters in parametersLocalNew:
            clf.set_params(**eachModelParameters)
            
            clf.fit(XData, yData) 
            yPredict = clf.predict(XData)
            yPredictProb = clf.predict_proba(XData)

            resultsMicro.append(geometric_mean_score(yData, yPredict, average='micro'))
            resultsMacro.append(geometric_mean_score(yData, yPredict, average='macro'))
            resultsWeighted.append(geometric_mean_score(yData, yPredict, average='weighted'))

            resultsCorrCoef.append(matthews_corrcoef(yData, yPredict))

            resultsMicroBeta5.append(fbeta_score(yData, yPredict, average='micro', beta=0.5))
            resultsMacroBeta5.append(fbeta_score(yData, yPredict, average='macro', beta=0.5))
            resultsWeightedBeta5.append(fbeta_score(yData, yPredict, average='weighted', beta=0.5))

            resultsMicroBeta1.append(fbeta_score(yData, yPredict, average='micro', beta=1))
            resultsMacroBeta1.append(fbeta_score(yData, yPredict, average='macro', beta=1))
            resultsWeightedBeta1.append(fbeta_score(yData, yPredict, average='weighted', beta=1))

            resultsMicroBeta2.append(fbeta_score(yData, yPredict, average='micro', beta=2))
            resultsMacroBeta2.append(fbeta_score(yData, yPredict, average='macro', beta=2))
            resultsWeightedBeta2.append(fbeta_score(yData, yPredict, average='weighted', beta=2))
    
            resultsLogLoss.append(log_loss(yData, yPredictProb, normalize=True))

        maxLog = abs(max(resultsLogLoss))
        minLog = abs(min(resultsLogLoss))
        for each in resultsLogLoss:
            resultsLogLossFinal.append((abs(each)-minLog)/(maxLog-minLog))

        metrics.insert(loop,'geometric_mean_score_micro',resultsMicro)
        metrics.insert(loop+1,'geometric_mean_score_macro',resultsMacro)
        metrics.insert(loop+2,'geometric_mean_score_weighted',resultsWeighted)

        metrics.insert(loop+3,'matthews_corrcoef',resultsCorrCoef)

        metrics.insert(loop+4,'f5_micro',resultsMicroBeta5)
        metrics.insert(loop+5,'f5_macro',resultsMacroBeta5)
        metrics.insert(loop+6,'f5_weighted',resultsWeightedBeta5)
        
        metrics.insert(loop+7,'f1_micro',resultsMicroBeta1)
        metrics.insert(loop+8,'f1_macro',resultsMacroBeta1)
        metrics.insert(loop+9,'f1_weighted',resultsWeightedBeta1)

        metrics.insert(loop+10,'f2_micro',resultsMicroBeta2)
        metrics.insert(loop+11,'f2_macro',resultsMacroBeta2)
        metrics.insert(loop+12,'f2_weighted',resultsWeightedBeta2)

        metrics.insert(loop+13,'log_loss',resultsLogLossFinal)

        metrics = metrics.to_json()

        resultsMetrics.append(metrics) # Position: 0 and so on 

    return resultsMetrics


def preProcsumPerMetricAccordingtoData(factors, loopThroughMetrics):
    sumPerClassifier = []
    loopThroughMetrics = loopThroughMetrics.fillna(0)
    for row in loopThroughMetrics.iterrows():
        rowSum = 0
        name, values = row
        for loop, elements in enumerate(values):
            rowSum = elements*factors[loop] + rowSum
        if sum(factors) is 0:
            sumPerClassifier = 0
        else:
            sumPerClassifier.append(rowSum/sum(factors) * 100)
    return sumPerClassifier

def preProcSumForEachMetric(factors, loopThroughMetrics):
    metricsPerModelColl = []
    loopThroughMetrics = loopThroughMetrics.fillna(0)
    metricsPerModelColl.append(loopThroughMetrics['mean_test_accuracy'])
    metricsPerModelColl.append(loopThroughMetrics['geometric_mean_score_micro'])
    metricsPerModelColl.append(loopThroughMetrics['geometric_mean_score_macro'])
    metricsPerModelColl.append(loopThroughMetrics['geometric_mean_score_weighted'])
    metricsPerModelColl.append(loopThroughMetrics['mean_test_precision_micro'])
    metricsPerModelColl.append(loopThroughMetrics['mean_test_precision_macro'])
    metricsPerModelColl.append(loopThroughMetrics['mean_test_precision_weighted'])
    metricsPerModelColl.append(loopThroughMetrics['mean_test_recall_micro'])
    metricsPerModelColl.append(loopThroughMetrics['mean_test_recall_macro'])
    metricsPerModelColl.append(loopThroughMetrics['mean_test_recall_weighted'])
    metricsPerModelColl.append(loopThroughMetrics['f5_micro'])
    metricsPerModelColl.append(loopThroughMetrics['f5_macro'])
    metricsPerModelColl.append(loopThroughMetrics['f5_weighted'])
    metricsPerModelColl.append(loopThroughMetrics['f1_micro'])
    metricsPerModelColl.append(loopThroughMetrics['f1_macro'])
    metricsPerModelColl.append(loopThroughMetrics['f1_weighted'])
    metricsPerModelColl.append(loopThroughMetrics['f2_micro'])
    metricsPerModelColl.append(loopThroughMetrics['f2_macro'])
    metricsPerModelColl.append(loopThroughMetrics['f2_weighted'])
    metricsPerModelColl.append(loopThroughMetrics['matthews_corrcoef'])
    metricsPerModelColl.append(loopThroughMetrics['mean_test_roc_auc_ovo_weighted'])
    metricsPerModelColl.append(loopThroughMetrics['log_loss'])
    f=lambda a: (abs(a)+a)/2
    for index, metric in enumerate(metricsPerModelColl):
        if (index == 19):
            metricsPerModelColl[index] = ((f(metric))*factors[index]) * 100
        elif (index == 21):
            metricsPerModelColl[index] = ((1 - metric)*factors[index]) * 100
        else:  
            metricsPerModelColl[index] = (metric*factors[index]) * 100
        metricsPerModelColl[index] = metricsPerModelColl[index].to_json()
    return metricsPerModelColl

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
    global foreachMetricResults
    foreachMetricResultsJSON = json.dumps(foreachMetricResults)
    ResultsUpdate.append(foreachMetricResultsJSON)
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
    global previousState
    global previousStateActive
    global keySpec
    global keySpecInternal
    global keyData
    scores = []

    global all_classifiersSelection  
    all_classifiersSelection = []

    global all_classifiers

    global XData
    global yData
    global sclf

    lr = LogisticRegression(random_state=RANDOM_SEED)

    if (keyRetrieved == 0):
        all_classifiers = []
        columnsInit = []
        columnsInit = [XData.columns.get_loc(c) for c in XData.columns if c in XData]

        temp = json.loads(allParametersPerformancePerModel[1])
        temp = temp['params']
        temp = {int(k):v for k,v in temp.items()}
        tempDic = {    
            'params': temp
        }
        dfParamKNN = pd.DataFrame.from_dict(tempDic)
        dfParamKNNFilt = dfParamKNN.iloc[:,0]
        for eachelem in KNNModels:
            arg = dfParamKNNFilt[eachelem]
            all_classifiers.append(make_pipeline(ColumnSelector(cols=columnsInit), KNeighborsClassifier().set_params(**arg)))
    
        temp = json.loads(allParametersPerformancePerModel[10])
        temp = temp['params']
        temp = {int(k):v for k,v in temp.items()}
        tempDic = {    
            'params': temp
        }
        dfParamSVC = pd.DataFrame.from_dict(tempDic)
        dfParamSVCFilt = dfParamSVC.iloc[:,0]
        for eachelem in SVCModels:
            arg = dfParamSVCFilt[eachelem-SVCModelsCount]
            all_classifiers.append(make_pipeline(ColumnSelector(cols=columnsInit), SVC(probability=True,random_state=RANDOM_SEED).set_params(**arg)))
        
        temp = json.loads(allParametersPerformancePerModel[19])
        temp = temp['params']
        temp = {int(k):v for k,v in temp.items()}
        tempDic = {    
            'params': temp
        }
        dfParamGauNB = pd.DataFrame.from_dict(tempDic)
        dfParamGauNBFilt = dfParamGauNB.iloc[:,0]
        for eachelem in GausNBModels:
            arg = dfParamGauNBFilt[eachelem-GausNBModelsCount]
            all_classifiers.append(make_pipeline(ColumnSelector(cols=columnsInit), GaussianNB().set_params(**arg)))

        temp = json.loads(allParametersPerformancePerModel[28])
        temp = temp['params']
        temp = {int(k):v for k,v in temp.items()}
        tempDic = {    
            'params': temp
        }
        dfParamMLP = pd.DataFrame.from_dict(tempDic)
        dfParamMLPFilt = dfParamMLP.iloc[:,0]
        for eachelem in MLPModels:
            arg = dfParamMLPFilt[eachelem-MLPModelsCount]
            all_classifiers.append(make_pipeline(ColumnSelector(cols=columnsInit), MLPClassifier(random_state=RANDOM_SEED).set_params(**arg)))

        temp = json.loads(allParametersPerformancePerModel[37])
        temp = temp['params']
        temp = {int(k):v for k,v in temp.items()}
        tempDic = {    
            'params': temp
        }
        dfParamLR = pd.DataFrame.from_dict(tempDic)
        dfParamLRFilt = dfParamLR.iloc[:,0]
        for eachelem in LRModels:
            arg = dfParamLRFilt[eachelem-LRModelsCount]
            all_classifiers.append(make_pipeline(ColumnSelector(cols=columnsInit), LogisticRegression(random_state=RANDOM_SEED).set_params(**arg)))

        temp = json.loads(allParametersPerformancePerModel[46])
        temp = temp['params']
        temp = {int(k):v for k,v in temp.items()}
        tempDic = {    
            'params': temp
        }
        dfParamLDA = pd.DataFrame.from_dict(tempDic)
        dfParamLDAFilt = dfParamLDA.iloc[:,0]
        for eachelem in LDAModels:
            arg = dfParamLDAFilt[eachelem-LDAModelsCount]
            all_classifiers.append(make_pipeline(ColumnSelector(cols=columnsInit), LinearDiscriminantAnalysis().set_params(**arg)))

        temp = json.loads(allParametersPerformancePerModel[55])
        temp = temp['params']
        temp = {int(k):v for k,v in temp.items()}
        tempDic = {    
            'params': temp
        }
        dfParamQDA = pd.DataFrame.from_dict(tempDic)
        dfParamQDAFilt = dfParamQDA.iloc[:,0]
        for eachelem in QDAModels:
            arg = dfParamQDAFilt[eachelem-QDAModelsCount]
            all_classifiers.append(make_pipeline(ColumnSelector(cols=columnsInit), QuadraticDiscriminantAnalysis().set_params(**arg)))

        temp = json.loads(allParametersPerformancePerModel[64])
        temp = temp['params']
        temp = {int(k):v for k,v in temp.items()}
        tempDic = {    
            'params': temp
        }
        dfParamRF = pd.DataFrame.from_dict(tempDic)
        dfParamRFFilt = dfParamRF.iloc[:,0]
        for eachelem in RFModels:
            arg = dfParamRFFilt[eachelem-RFModelsCount]
            all_classifiers.append(make_pipeline(ColumnSelector(cols=columnsInit), RandomForestClassifier(random_state=RANDOM_SEED).set_params(**arg)))

        temp = json.loads(allParametersPerformancePerModel[73])
        temp = temp['params']
        temp = {int(k):v for k,v in temp.items()}
        tempDic = {    
            'params': temp
        }
        dfParamExtraT = pd.DataFrame.from_dict(tempDic)
        dfParamExtraTFilt = dfParamExtraT.iloc[:,0]


        for eachelem in ExtraTModels:
            arg = dfParamExtraTFilt[eachelem-ExtraTModelsCount]
            all_classifiers.append(make_pipeline(ColumnSelector(cols=columnsInit), ExtraTreesClassifier(random_state=RANDOM_SEED).set_params(**arg)))

        temp = json.loads(allParametersPerformancePerModel[82])
        temp = temp['params']
        temp = {int(k):v for k,v in temp.items()}
        tempDic = {    
            'params': temp
        }
        dfParamAdaB = pd.DataFrame.from_dict(tempDic)
        dfParamAdaBFilt = dfParamAdaB.iloc[:,0]
        for eachelem in AdaBModels:
            arg = dfParamAdaBFilt[eachelem-AdaBModelsCount]
            all_classifiers.append(make_pipeline(ColumnSelector(cols=columnsInit), AdaBoostClassifier(random_state=RANDOM_SEED).set_params(**arg)))

        temp = json.loads(allParametersPerformancePerModel[91])
        temp = temp['params']
        temp = {int(k):v for k,v in temp.items()}
        tempDic = {    
            'params': temp
        }
        dfParamGradB = pd.DataFrame.from_dict(tempDic)
        dfParamGradBFilt = dfParamGradB.iloc[:,0]
        for eachelem in GradBModels:
            arg = dfParamGradBFilt[eachelem-GradBModelsCount]
            all_classifiers.append(make_pipeline(ColumnSelector(cols=columnsInit), GradientBoostingClassifier(random_state=RANDOM_SEED).set_params(**arg)))

        global sclf 
        sclf = 0
        sclf = StackingCVClassifier(classifiers=all_classifiers,
                            use_probas=True,
                            meta_classifier=lr,
                            random_state=RANDOM_SEED,
                            n_jobs = -1)
        keySpec = 0
    elif (keyRetrieved == 1):     
        Models = json.loads(Models)
        ModelsAll = preProceModels()
        for index, modHere in enumerate(ModelsAll):
            flag = 0
            for loop in Models['ClassifiersList']:
                if (int(loop) == int(modHere)):
                    flag = 1
            if (flag is 1):
                all_classifiersSelection.append(all_classifiers[index])

        sclf = StackingCVClassifier(classifiers=all_classifiersSelection,
                            use_probas=True,
                            meta_classifier=lr,
                            random_state=RANDOM_SEED,
                            n_jobs = -1)
        keySpec = 1
    elif (keyRetrieved == 2):
        if (len(all_classifiersSelection) == 0):
            all_classifiers = []
            columnsInit = []
            countItems = 0
            
            temp = json.loads(allParametersPerformancePerModel[1])
            temp = temp['params']
            temp = {int(k):v for k,v in temp.items()}
            tempDic = {    
                'params': temp
            }
            dfParamKNN = pd.DataFrame.from_dict(tempDic)
            dfParamKNNFilt = dfParamKNN.iloc[:,0]
            flag = 0
            for index, eachelem in enumerate(KNNModels):
                arg = dfParamKNNFilt[eachelem]
                all_classifiers.append(make_pipeline(ColumnSelector(cols=featureSelection['featureSelection'][countItems]), KNeighborsClassifier().set_params(**arg)))
                countItems += 1
      
            temp = json.loads(allParametersPerformancePerModel[10])
            temp = temp['params']
            temp = {int(k):v for k,v in temp.items()}
            tempDic = {    
                'params': temp
            }
            dfParamSVC = pd.DataFrame.from_dict(tempDic)
            dfParamSVCFilt = dfParamSVC.iloc[:,0]
            for index, eachelem in enumerate(SVCModels):
                arg = dfParamSVCFilt[eachelem-SVCModelsCount]
                all_classifiers.append(make_pipeline(ColumnSelector(cols=featureSelection['featureSelection'][countItems]), SVC(probability=True,random_state=RANDOM_SEED).set_params(**arg)))
                countItems += 1
   
            temp = json.loads(allParametersPerformancePerModel[19])
            temp = temp['params']
            temp = {int(k):v for k,v in temp.items()}
            tempDic = {    
                'params': temp
            }
            dfParamGauNB = pd.DataFrame.from_dict(tempDic)
            dfParamGauNBFilt = dfParamGauNB.iloc[:,0]
            for index, eachelem in enumerate(GausNBModels):
                arg = dfParamGauNBFilt[eachelem-GausNBModelsCount]
                all_classifiers.append(make_pipeline(ColumnSelector(cols=featureSelection['featureSelection'][countItems]), GaussianNB().set_params(**arg)))
                countItems += 1

            temp = json.loads(allParametersPerformancePerModel[28])
            temp = temp['params']
            temp = {int(k):v for k,v in temp.items()}
            tempDic = {    
                'params': temp
            }
            dfParamMLP = pd.DataFrame.from_dict(tempDic)
            dfParamMLPFilt = dfParamMLP.iloc[:,0]
            for index, eachelem in enumerate(MLPModels):
                arg = dfParamMLPFilt[eachelem-MLPModelsCount]
                all_classifiers.append(make_pipeline(ColumnSelector(cols=featureSelection['featureSelection'][countItems]), MLPClassifier(random_state=RANDOM_SEED).set_params(**arg)))
                countItems += 1

            temp = json.loads(allParametersPerformancePerModel[37])
            temp = temp['params']
            temp = {int(k):v for k,v in temp.items()}
            tempDic = {    
                'params': temp
            }
            dfParamLR = pd.DataFrame.from_dict(tempDic)
            dfParamLRFilt = dfParamLR.iloc[:,0]
            for index, eachelem in enumerate(LRModels):
                arg = dfParamLRFilt[eachelem-LRModelsCount]
                all_classifiers.append(make_pipeline(ColumnSelector(cols=featureSelection['featureSelection'][countItems]), LogisticRegression(random_state=RANDOM_SEED).set_params(**arg)))
                countItems += 1

            temp = json.loads(allParametersPerformancePerModel[46])
            temp = temp['params']
            temp = {int(k):v for k,v in temp.items()}
            tempDic = {    
                'params': temp
            }
            dfParamLDA = pd.DataFrame.from_dict(tempDic)
            dfParamLDAFilt = dfParamLDA.iloc[:,0]
            for index, eachelem in enumerate(LDAModels):
                arg = dfParamLDAFilt[eachelem-LDAModelsCount]
                all_classifiers.append(make_pipeline(ColumnSelector(cols=featureSelection['featureSelection'][countItems]), LinearDiscriminantAnalysis().set_params(**arg)))
                countItems += 1

            temp = json.loads(allParametersPerformancePerModel[55])
            temp = temp['params']
            temp = {int(k):v for k,v in temp.items()}
            tempDic = {    
                'params': temp
            }
            dfParamQDA = pd.DataFrame.from_dict(tempDic)
            dfParamQDAFilt = dfParamQDA.iloc[:,0]
            for index, eachelem in enumerate(QDAModels):
                arg = dfParamQDAFilt[eachelem-QDAModelsCount]
                all_classifiers.append(make_pipeline(ColumnSelector(cols=featureSelection['featureSelection'][countItems]), QuadraticDiscriminantAnalysis().set_params(**arg)))
                countItems += 1

            temp = json.loads(allParametersPerformancePerModel[64])
            temp = temp['params']
            temp = {int(k):v for k,v in temp.items()}
            tempDic = {    
                'params': temp
            }
            dfParamRF = pd.DataFrame.from_dict(tempDic)
            dfParamRFFilt = dfParamRF.iloc[:,0]
            for index, eachelem in enumerate(RFModels):
                arg = dfParamRFFilt[eachelem-RFModelsCount]
                all_classifiers.append(make_pipeline(ColumnSelector(cols=featureSelection['featureSelection'][countItems]), RandomForestClassifier(random_state=RANDOM_SEED).set_params(**arg)))
                countItems += 1

            temp = json.loads(allParametersPerformancePerModel[73])
            temp = temp['params']
            temp = {int(k):v for k,v in temp.items()}
            tempDic = {    
                'params': temp
            }
            dfParamExtraT = pd.DataFrame.from_dict(tempDic)
            dfParamExtraTFilt = dfParamExtraT.iloc[:,0]
            for index, eachelem in enumerate(ExtraTModels):
                arg = dfParamExtraTFilt[eachelem-ExtraTModelsCount]
                all_classifiers.append(make_pipeline(ColumnSelector(cols=featureSelection['featureSelection'][countItems]), ExtraTreesClassifier(random_state=RANDOM_SEED).set_params(**arg)))
                countItems += 1

            temp = json.loads(allParametersPerformancePerModel[82])
            temp = temp['params']
            temp = {int(k):v for k,v in temp.items()}
            tempDic = {    
                'params': temp
            }
            dfParamAdaB = pd.DataFrame.from_dict(tempDic)
            dfParamAdaBFilt = dfParamAdaB.iloc[:,0]
            for index, eachelem in enumerate(AdaBModels):
                arg = dfParamAdaBFilt[eachelem-AdaBModelsCount]
                all_classifiers.append(make_pipeline(ColumnSelector(cols=featureSelection['featureSelection'][countItems]), AdaBoostClassifier(random_state=RANDOM_SEED).set_params(**arg)))
                countItems += 1

            temp = json.loads(allParametersPerformancePerModel[91])
            temp = temp['params']
            temp = {int(k):v for k,v in temp.items()}
            tempDic = {    
                'params': temp
            }
            dfParamGradB = pd.DataFrame.from_dict(tempDic)
            dfParamGradBFilt = dfParamGradB.iloc[:,0]
            for index, eachelem in enumerate(GradBModels):
                arg = dfParamGradBFilt[eachelem-GradBModelsCount]
                all_classifiers.append(make_pipeline(ColumnSelector(cols=featureSelection['featureSelection'][countItems]), GradientBoostingClassifier().set_params(**arg)))
                store = index
                flag = 1          

            sclf = StackingCVClassifier(classifiers=all_classifiers,
                                use_probas=True,
                                meta_classifier=lr,
                                random_state=RANDOM_SEED,
                                n_jobs = -1)
            keySpec = 1
    else:
        keySpec = 2

        # Models = json.loads(Models)
        # ModelsAll = preProceModels()
        # for index, modHere in enumerate(ModelsAll):
        #     flag = 0
        #     for loop in Models['ClassifiersList']:
        #         if (int(loop) == int(modHere)):
        #             flag = 1
        #     if (flag is 1):
        #         all_classifiersSelection.append(all_classifiers[index])

        # sclfStack = StackingCVClassifier(classifiers=all_classifiersSelection,
        #                     use_probas=True,
        #                     meta_classifier=lr,
        #                     random_state=RANDOM_SEED,
        #                     n_jobs = -1)
        
        
        #else:
        #    for index, eachelem in enumerate(algorithmsWithoutDuplicates):
        #        if (eachelem == 'KNN'):
        #            for j, each in enumerate(resultsList[index][1]):
        #                all_classifiersSelection.append(make_pipeline(ColumnSelector(cols=columnsReduce[j]), KNeighborsClassifier().set_params(**each)))
        #            del columnsReduce[0:len(resultsList[index][1])]
        #        else:
        #            for j, each in enumerate(resultsList[index][1]):
        #                all_classifiersSelection.append(make_pipeline(ColumnSelector(cols=columnsReduce[j]), RandomForestClassifier(random_state=RANDOM_SEED).set_params(**each)))
        #            del columnsReduce[0:len(resultsList[index][1])]
        #    sclf = StackingCVClassifier(classifiers=all_classifiersSelection,
        #                        use_probas=True,
        #                        meta_classifier=lr,
        #                        random_state=RANDOM_SEED,
        #                        n_jobs = -1)

    # if (keyRetrieved == 0):
    #     pass
    # else:
    print(keySpec)
    print(keySpecInternal)
    if (keySpec == 0 or keySpec == 1):
        num_cores = multiprocessing.cpu_count()
        inputsSc = ['accuracy','precision_weighted','recall_weighted','f1_weighted']

        flat_results = Parallel(n_jobs=num_cores)(delayed(solve)(sclf,keyData,keySpec,keySpecInternal,previousState,previousStateActive,XData,yData,crossValidation,item,index) for index, item in enumerate(inputsSc))
        scores = [item for sublist in flat_results for item in sublist]

    if (keySpec == 0):
        previousState = []
        previousState.append(scores[2])
        previousState.append(scores[3])
        previousState.append(scores[6])
        previousState.append(scores[7])
        previousState.append(scores[10])
        previousState.append(scores[11])
        previousState.append(scores[14])
        previousState.append(scores[15])
    elif (keySpec == 1):
        if (keySpecInternal == 1):
            previousStateActive = []
            previousStateActive.append(scores[0])
            previousStateActive.append(scores[1])
            previousStateActive.append(scores[4])
            previousStateActive.append(scores[5])
            previousStateActive.append(scores[8])
            previousStateActive.append(scores[9])
            previousStateActive.append(scores[12])
            previousStateActive.append(scores[13])
        else:
            previousStateActive = []
            previousStateActive.append(scores[0])
            previousStateActive.append(scores[1])
            previousStateActive.append(scores[4])
            previousStateActive.append(scores[5])
            previousStateActive.append(scores[8])
            previousStateActive.append(scores[9])
            previousStateActive.append(scores[12])
            previousStateActive.append(scores[13])
            previousState = []
            previousState.append(scores[2])
            previousState.append(scores[3])
            previousState.append(scores[6])
            previousState.append(scores[7])
            previousState.append(scores[10])
            previousState.append(scores[11])
            previousState.append(scores[14])
            previousState.append(scores[15])
    else:
        scores = []
        previousState = []
        scores.append(previousStateActive[0])
        scores.append(previousStateActive[1])
        scores.append(previousStateActive[0])
        scores.append(previousStateActive[1])
        previousState.append(previousStateActive[0])
        previousState.append(previousStateActive[1])
        scores.append(previousStateActive[2])
        scores.append(previousStateActive[3])
        scores.append(previousStateActive[2])
        scores.append(previousStateActive[3])
        previousState.append(previousStateActive[2])
        previousState.append(previousStateActive[3])
        scores.append(previousStateActive[4])
        scores.append(previousStateActive[5])
        scores.append(previousStateActive[4])
        scores.append(previousStateActive[5])
        previousState.append(previousStateActive[4])
        previousState.append(previousStateActive[5])
        scores.append(previousStateActive[6])
        scores.append(previousStateActive[7])
        scores.append(previousStateActive[6])
        scores.append(previousStateActive[7])
        previousState.append(previousStateActive[6])
        previousState.append(previousStateActive[7])

    return 'Okay'

def solve(sclf,keyData,keySpec,keySpecInternal,previousStateLoc,previousStateActiveLoc,XData,yData,crossValidation,scoringIn,loop):
    scoresLoc = []
    if (keySpec == 0):
        temp = model_selection.cross_val_score(sclf, XData, yData, cv=crossValidation, scoring=scoringIn, n_jobs=-1)
        scoresLoc.append(temp.mean())
        scoresLoc.append(temp.std())
        if (keyData == 1):
            if (loop == 0):
                scoresLoc.append(previousStateLoc[0])
                scoresLoc.append(previousStateLoc[1])
            elif (loop == 1):
                scoresLoc.append(previousStateLoc[2])
                scoresLoc.append(previousStateLoc[3])
            elif (loop == 2):
                scoresLoc.append(previousStateLoc[4])
                scoresLoc.append(previousStateLoc[5])
            else:
                scoresLoc.append(previousStateLoc[6])
                scoresLoc.append(previousStateLoc[7])
        else:
            scoresLoc.append(temp.mean())
            scoresLoc.append(temp.std())
    else:
        if (keySpecInternal == 1):
            temp = model_selection.cross_val_score(sclf, XData, yData, cv=crossValidation, scoring=scoringIn, n_jobs=-1)
            scoresLoc.append(temp.mean())
            scoresLoc.append(temp.std())
            if (loop == 0):
                scoresLoc.append(previousStateLoc[0])
                scoresLoc.append(previousStateLoc[1])
            elif (loop == 1):
                scoresLoc.append(previousStateLoc[2])
                scoresLoc.append(previousStateLoc[3])
            elif (loop == 2):
                scoresLoc.append(previousStateLoc[4])
                scoresLoc.append(previousStateLoc[5])
            else:
                scoresLoc.append(previousStateLoc[6])
                scoresLoc.append(previousStateLoc[7])
        else:
            temp = model_selection.cross_val_score(sclf, XData, yData, cv=crossValidation, scoring=scoringIn, n_jobs=-1)
            scoresLoc.append(temp.mean())
            scoresLoc.append(temp.std())
            scoresLoc.append(temp.mean())
            scoresLoc.append(temp.std())

    return scoresLoc

# Sending the final results to be visualized as a line plot
@app.route('/data/SendFinalResultsBacktoVisualize', methods=["GET", "POST"])
def SendToPlotFinalResults():
    response = {    
        'FinalResults': scores
    }
    return jsonify(response)

# Sending the final results to be visualized as a line plot
#@app.route('/data/SendInstancesImportance', methods=["GET", "POST"])
#def SendImportInstances():
#    global DataHeatmap
#    response = {    
#        'instancesImportance': DataHeatmap
#    }
#    return jsonify(response)

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
    global keyData
    keyData = 1
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

    if (filterActionFinal == 'merge'):
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

    # save and restore
    if (filterProvenanceFinal == 'save'):
        XDataStored = XData
        yDataStored = yData
    else:
        XData = XDataStored.copy()
        yData = yDataStored.copy()

    return 'Done'