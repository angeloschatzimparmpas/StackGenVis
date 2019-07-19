# first line: 133
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
