# first line: 705
def GridSearchForParameters(clf, params, eachAlgor, factors):

    global scoring 
    global NumberofscoringMetrics

    # instantiate spark session
    spark = (   
        SparkSession    
        .builder    
        .getOrCreate()    
        )
    sc = spark.sparkContext 

    scoring = {'accuracy': 'accuracy', 'f1_macro': 'f1_weighted', 'precision': 'precision_weighted', 'recall': 'recall_weighted', 'jaccard': 'jaccard_weighted'}
    global crossValidation
    NumberofscoringMetrics = len(scoring)

    grid = DistGridSearchCV(    
        estimator=clf, param_grid=params,     
        sc=sc, cv=crossValidation, refit='accuracy', scoring=scoring,
        verbose=0, n_jobs=-1)

    grid.fit(XData, yData)
    yPredict = grid.predict(XData)
    cv_results = []
    cv_results.append(grid.cv_results_)
    df_cv_results = pd.DataFrame.from_dict(cv_results)
    number_of_classifiers = len(df_cv_results.iloc[0][0])

    df_cv_results_per_item = []
    df_cv_results_per_row = []

    for i in range(number_of_classifiers):
        df_cv_results_per_item = []
        for column in df_cv_results.iloc[0]:
            df_cv_results_per_item.append(column[i])
        df_cv_results_per_row.append(df_cv_results_per_item)
    df_cv_results_classifiers = pd.DataFrame(data = df_cv_results_per_row, columns= df_cv_results.columns)

    global allParametersPerformancePerModel
    global parametersPerformancePerModel

    metrics = df_cv_results_classifiers.copy()
    metrics = metrics.filter(['mean_test_accuracy','mean_test_f1_macro','mean_test_precision','mean_test_recall','mean_test_jaccard'])
    sumperModel = []
    global rowSum
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
    global target_names
    global PerClassMetric
    global PerClassMetricPandas
    PerClassMetric = []
    yPredictProb.append(grid.predict_proba(XData))
    PerClassMetric.append(classification_report(yData, yPredict, target_names=target_names, digits=2, output_dict=True))
    PerClassMetricPandas = pd.DataFrame(PerClassMetric)  
    del PerClassMetricPandas['accuracy']  
    del PerClassMetricPandas['macro avg']  
    del PerClassMetricPandas['weighted avg']  
    summarizedMetrics = pd.DataFrame(sumperModel)
    summarizedMetrics.rename(columns={0:'sum'})
    parameters = pd.DataFrame(df_cv_results_classifiers['params'])
    parametersPerformancePerModel = pd.concat([summarizedMetrics, parameters], axis=1)
    PerClassMetricPandas = PerClassMetricPandas.to_json()
    parametersPerformancePerModel = parametersPerformancePerModel.to_json()
    allParametersPerformancePerModel.append(parametersPerformancePerModel)
    allParametersPerformancePerModel.append(PerClassMetricPandas)
    return 'Everything is okay'