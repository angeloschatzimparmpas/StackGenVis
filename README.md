# StackGenVis: Alignment of Data, Algorithms, and Models for Stacking Ensemble Learning Using Performance Metrics

This Git repository contains the code that accompanies the research paper "StackGenVis: Alignment of Data, Algorithms, and Models for Stacking Ensemble Learning Using Performance Metrics". The details of the experiments and the research outcome are described in [the paper](https://doi.org/10.1109/TVCG.2020.3030352).

**Note:** StackGenVis is optimized to work better for standard resolutions (such as 1440p/QHD (Quad High Definition) and 1080p). For lower resolutions, our recommendation is to use the collapsible functionality of the top dark gray panels. Finally, any other resolution might need manual adjustment of your browser's zoom level to work properly.

**Note:** The tag `paper-version` matches the implementation at the time of the paper's publication. The current version might look significantly different depending on how much time has passed since then.

**Note:** As any other software, the code is not bug free. There might be limitations in the views and functionalities of the tool that could be addressed in a future code update.

# Data Sets #
All publicly available data sets used in the paper are in the `data` folder, formatted as comma separated values (csv). 
Most of them are available online from the [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/index.php): Iris and Heart Disease. We also used a collection of data related to sentiment/stance detection in texts. This data set is not included due to permission issues, since it was parsed from well-known social media platforms by our group.

# Requirements #
For the backend:
- [Python 3](https://www.python.org/downloads/)
- [Flask](https://palletsprojects.com/p/flask/)
- [MongoDB](https://www.mongodb.com/try/download/community) (Version: 4.x)
- Other packages: `pymongo`, `Flask-PyMongo`, `flask_cors`, `mlxtend`, `imblearn`, `joblib`, `numpy`, `scikit-learn`, `scikit-learn-extra`, `sk-dist`, `eli5`, `umap-learn`, and `pandas`.

You can install all the backend requirements for Python with the following command:
```
pip install -r requirements.txt
```

For the frontend:
- [Node.js](https://nodejs.org/en/) (including Webpack; to install it, `npm install webpack-dev-server@3.10.3`)

There is no need to install anything further for the frontend (e.g., D3 and Plotly.js), since all modules are in the repository.

For the reproducibility of the first use case, the red wine quality data set should be inserted to MongoDB by using the commands below:
```
# recommendation: use insertMongo script to add a data set in Mongo database
# for Python3
python3 insertMongo.py
```

# Usage #
Below is an example of how you can get StackGenVis running using Python and Node.js for the backend and frontend, respectively. The frontend is written in JavaScript/HTML with the help of Vue.js framework, so it could be hosted in any other web server of your preference. The only hard requirement (currently) is that both frontend and backend must be running on the same machine. 
```
# first terminal: hosting the visualization side (client)
# with Node.js
cd frontend
npm run dev
```

```
# second terminal: hosting the computational side (server)
FLASK_APP=run.py flask run
```

Then, open your browser and point it to `localhost:8080`. We recommend using an up-to-date version of Google Chrome.

# Hyper-Parameters per Algorithm #
**Base classifiers:**
- **K-Nearest Neighbor:** {'n_neighbors': list(range(1, 25)), 'metric': ['chebyshev', 'manhattan', 'euclidean', 'minkowski'], 'algorithm': ['brute', 'kd_tree', 'ball_tree'], 'weights': ['uniform', 'distance']}
- **Support Vector Machine:** {'C': list(np.arange(0.1,4.43,0.11)), 'kernel': ['rbf','linear', 'poly', 'sigmoid']}
- **Gaussian Naive Bayes:** {'var_smoothing': list(np.arange(0.00000000001,0.0000001,0.0000000002))}
- **Multilayer Perceptron:** {'alpha': list(np.arange(0.00001,0.001,0.0002)), 'tol': list(np.arange(0.00001,0.001,0.0004)), 'max_iter': list(np.arange(100,200,100)), 'activation': ['relu', 'identity', 'logistic', 'tanh'], 'solver' : ['adam', 'sgd']}
- **Logistic Regression:** {'C': list(np.arange(0.5,2,0.075)), 'max_iter': list(np.arange(50,250,50)), 'solver': ['lbfgs', 'newton-cg', 'sag', 'saga'], 'penalty': ['l2', 'none']}
- **Linear Discriminant Analysis:** {'shrinkage': list(np.arange(0,1,0.01)), 'solver': ['lsqr', 'eigen']}
- **Quadratic Discriminant Analysis:** {'reg_param': list(np.arange(0,1,0.02)), 'tol': list(np.arange(0.00001,0.001,0.0002))}
- **Random Forests:** {'n_estimators': list(range(60, 140)), 'criterion': ['gini', 'entropy']}
- **Extra Trees:** {'n_estimators': list(range(60, 140)), 'criterion': ['gini', 'entropy']}
- **Adaptive Boosting:** {'n_estimators': list(range(40, 80)), 'learning_rate': list(np.arange(0.1,2.3,1.1)), 'algorithm': ['SAMME.R', 'SAMME']} 
- **Gradient Boosting:** {'n_estimators': list(range(85, 115)), 'learning_rate': list(np.arange(0.01,0.23,0.11)), 'criterion': ['friedman_mse', 'mse', 'mae']}

**Meta-learner**: 
- **Logistic Regression** with the default Sklearn hyper-parameters. By that time, the core hyper-parameter tuples were: C=1.0, max_iter=100, solver='lbfgs', and penalty='l2'.

# Corresponding Author #
For any questions with regard to the implementation or the paper, feel free to contact [Angelos Chatzimparmpas](mailto:angelos.chatzimparmpas@lnu.se).
