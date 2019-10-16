# first line: 703
@memory.cache
def EnsembleModel(keyRetrieved): 

    scoresLocal = []
    all_classifiersSelection = []  

    if (keyRetrieved == 0):
        columnsInit = []
        all_classifiers = []  
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

        scoresLocal = model_selection.cross_val_score(clf, XData, yData, cv=crossValidation, scoring='accuracy')
    return scoresLocal
