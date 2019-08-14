# first line: 484
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
