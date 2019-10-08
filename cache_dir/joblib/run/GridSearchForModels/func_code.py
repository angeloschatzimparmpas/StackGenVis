# first line: 714
def GridSearchForModels(clf, params, eachAlgor, factors):

    # scoring parameters
    global scoring 

    # number of scoring parameters
    global NumberofscoringMetrics

    # crossvalidation number
    global crossValidation

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
    yPredict = grid.predict(XData)

    # process the results
    cv_results = []
    cv_results.append(grid.cv_results_)
    df_cv_results = pd.DataFrame.from_dict(cv_results)

    # number of models stored
    number_of_models = len(df_cv_results.iloc[0][0])

    # initialize results per row
    df_cv_results_per_row = []

    # loop through number of models
    for i in range(number_of_models):
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
    for row in metrics.iterrows():
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
    
    yPredictProb.append(grid.predict_proba(XData))
    
    # retrieve target names (class names)
    global target_names
    PerClassMetric = []
    PerClassMetric.append(classification_report(yData, yPredict, target_names=target_names, digits=2, output_dict=True))
    PerClassMetricPandas = pd.DataFrame(PerClassMetric)  
    print(PerClassMetricPandas)
    del PerClassMetricPandas['accuracy']  
    del PerClassMetricPandas['macro avg']  
    del PerClassMetricPandas['weighted avg']  
    PerClassMetricPandas = PerClassMetricPandas.to_json()

    # concat parameters and performance
    parameters = pd.DataFrame(df_cv_results_classifiers['params'])
    parametersPerformancePerModel = pd.concat([summarizedMetrics, parameters], axis=1)
    parametersPerformancePerModel = parametersPerformancePerModel.to_json()
    
    # make global the parameters performance to send it back
    global allParametersPerformancePerModel
    allParametersPerformancePerModel.append(parametersPerformancePerModel)
    allParametersPerformancePerModel.append(PerClassMetricPandas)

    return 'Everything is okay'
