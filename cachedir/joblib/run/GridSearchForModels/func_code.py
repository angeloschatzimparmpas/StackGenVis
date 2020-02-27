# first line: 556
@memory.cache
def GridSearchForModels(XData, yData, clf, params, eachAlgor, AlgorithmsIDsEnd):
    print(clf)
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

    metrics = metrics.filter(['mean_test_accuracy','mean_test_neg_mean_absolute_error','mean_test_neg_root_mean_squared_error','mean_test_precision_micro','mean_test_precision_macro','mean_test_precision_weighted','mean_test_recall_micro','mean_test_recall_macro','mean_test_recall_weighted','mean_test_roc_auc_ovo_weighted']) 

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

    loop = 10

    # influence calculation for all the instances
    inputs = range(len(XData))
    num_cores = multiprocessing.cpu_count()
    
    impDataInst = Parallel(n_jobs=num_cores)(delayed(processInput)(i,XData,yData,crossValidation,clf) for i in inputs)

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
    metrics = metrics.clip(lower=0)
    metrics = metrics.to_json()
    results.append(metrics) # Position: 6 and so on
    results.append(perModelProbPandas) # Position: 7 and so on
    results.append(json.dumps(impDataInst)) # Position: 8 and so on

    return results
