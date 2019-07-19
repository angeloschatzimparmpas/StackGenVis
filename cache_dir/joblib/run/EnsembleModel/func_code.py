# first line: 249
def EnsembleModel (ClassifierIDsList, keyRetrieved): 

    if (keyRetrieved == 0):
        all_classifiers = []
        all_classifiers.append(KNeighborsClassifier(n_neighbors=1))
        all_classifiers.append(KNeighborsClassifier(n_neighbors=2))
        all_classifiers.append(KNeighborsClassifier(n_neighbors=10))
        all_classifiers.append(RandomForestClassifier(random_state=RANDOM_SEED, n_estimators = 1))
        all_classifiers.append(RandomForestClassifier(random_state=RANDOM_SEED, n_estimators = 50))
        lr = LogisticRegression()

        sclf = StackingCVClassifier(classifiers=all_classifiers,
                            use_probas=True,
                            meta_classifier=lr,
                            random_state=RANDOM_SEED,
                            n_jobs = -1)
        for clf, label in zip([sclf], 
                        ['StackingClassifierAllClassifiers']):

            scores = model_selection.cross_val_score(clf, XData, yData, 
                                                    cv=5, scoring='accuracy')
            print("Accuracy: %0.2f (+/- %0.2f) [%s]" 
                % (scores.mean(), scores.std(), label))
    else:        
        all_classifiers = []                 
        ClassifierIDsList = ClassifierIDsList.split('"')
        for loop in ClassifierIDsList:
            if ('ClassifierID' in loop):
                if (loop == 'ClassifierID: 1'):
                    all_classifiers.append(KNeighborsClassifier(n_neighbors=1))
                elif (loop == 'ClassifierID: 2'):
                    all_classifiers.append(KNeighborsClassifier(n_neighbors=2))
                elif (loop == 'ClassifierID: 3'):
                    all_classifiers.append(KNeighborsClassifier(n_neighbors=10))
                elif (loop == 'ClassifierID: 4'):
                    all_classifiers.append(RandomForestClassifier(random_state=RANDOM_SEED, n_estimators = 1))
                else:
                    all_classifiers.append(RandomForestClassifier(random_state=RANDOM_SEED, n_estimators = 50))

        lr = LogisticRegression()

        sclf = StackingCVClassifier(classifiers=all_classifiers,
                            use_probas=True,
                            meta_classifier=lr,
                            random_state=RANDOM_SEED,
                            n_jobs = -1)
        for clf, label in zip([sclf], 
                        ['StackingClassifierSelectedClassifiers']):

            scores = model_selection.cross_val_score(clf, XData, yData, 
                                                    cv=5, scoring='accuracy')
            print("Accuracy: %0.2f (+/- %0.2f) [%s]" 
                % (scores.mean(), scores.std(), label))
