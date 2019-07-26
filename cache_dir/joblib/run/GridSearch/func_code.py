# first line: 85
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
    target_names = ['class 0', 'class 1', 'class 2']
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
        print(eachClassifierParamsDictList)   
        grid.fit(XData, yData)
        yPredict = grid.predict(XData)
        print(classification_report(yData, yPredict, target_names=target_names))
        if (FI == 1):
            FeatureImp.append(grid.best_estimator_.feature_importances_)

    return df_cv_results_classifiers, parameters, FeatureImp
