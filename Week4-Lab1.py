# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 17:21:27 2024

@author: KAZ76504
"""

### Hands-on Lab: Complete the Machine Learning Prediction lab

# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns
# Preprocessing allows us to standarsize our data
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
# Allows us to split our data into training and testing data
from sklearn.model_selection import train_test_split
# Allows us to test parameters of classification algorithms and find the best one
from sklearn.model_selection import GridSearchCV
# Logistic Regression classification algorithm
from sklearn.linear_model import LogisticRegression
# Support Vector Machine classification algorithm
from sklearn.svm import SVC
# Decision Tree classification algorithm
from sklearn.tree import DecisionTreeClassifier
# K Nearest Neighbors classification algorithm
from sklearn.neighbors import KNeighborsClassifier

# This function is to plot the confusion matrix.
def plot_confusion_matrix(y,y_predict):
    "this function plots the confusion matrix"
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y, y_predict)
    ax= plt.subplot()
    sns.heatmap(cm, annot=True, ax = ax); #annot=True to annotate cells
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix'); 
    ax.xaxis.set_ticklabels(['did not land', 'land']); ax.yaxis.set_ticklabels(['did not land', 'landed']) 
    plt.show() 


#folder = '//Users//alikazemijahromi//Library//CloudStorage//OneDrive-Personal//Machine Learning//Coursera//IMB Data Science Specialization//Course 10//Week 4//'
folder = 'C:\\Users\\KAZ76504\\OneDrive - Personal\\OneDrive\\Machine Learning\\Coursera\\IMB Data Science Specialization\\Course 10\\Week 4\\'
filename = 'dataset_part_2.csv'
path = folder + filename
data = pd.read_csv(path)

filename = 'dataset_part_3.csv'
path = folder + filename
X = pd.read_csv(path)



### TASK 1: Create a NumPy array from the column Class in data, by applying the
#method to_numpy() then assign it to the variable Y,make sure the output is a 
#Pandas series (only one bracket df['name of column']).
Y = data['Class'].to_numpy()


### TASK 2: Standardize the data in X then reassign it to the variable X using 
#the transform provided below.
X = StandardScaler().fit_transform(X)


### TASK 3: Use the function train_test_split to split the data X and Y into 
#training and test data. Set the parameter test_size to 0.2 and random_state to 
#2. The training data and test data should be assigned to the following labels.
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)


### TASK 4: Create a logistic regression object then create a GridSearchCV 
#object logreg_cv with cv = 10. Fit the object to find the best parameters from 
#the dictionary parameters.
parameters = {'C':[0.01,0.1,1], 'penalty':['l2'], 'solver':['lbfgs']}
lr = LogisticRegression()
Grid_lr = GridSearchCV(estimator=lr, param_grid=parameters, cv=10)
Grid_lr.fit(X_train, Y_train)
best_C = Grid_lr.best_params_
print(Grid_lr.best_score_)

### TASK 5: Calculate the accuracy on the test data using the method score
print(Grid_lr.score(X_test, Y_test)) # This gives the result based on the best estimator in the grid search
Yhat_test = Grid_lr.predict(X_test)  # This gives the result based on the best estimator in the grid search
plot_confusion_matrix(Y_test, Yhat_test)


### TASK 6: Create a support vector machine object then create a GridSearchCV 
#object svm_cv with cv - 10. Fit the object to find the best parameters from 
#the dictionary parameters.
parameters = {'kernel':('linear', 'rbf','poly','rbf', 'sigmoid'), 'C': np.logspace(-3, 3, 5), 'gamma':np.logspace(-3, 3, 5)}
svm = SVC()
Grid_svm = GridSearchCV(estimator=svm, param_grid=parameters, cv=10)
Grid_svm.fit(X_train, Y_train)
best_params = Grid_svm.best_params_
print(Grid_svm.best_score_)


### TASK 7: Calculate the accuracy on the test data using the method score
print(Grid_svm.score(X_test, Y_test)) # This gives the result based on the best estimator in the grid search
Yhat_test = Grid_svm.predict(X_test)  # This gives the result based on the best estimator in the grid search
plot_confusion_matrix(Y_test, Yhat_test)


### TASK 8: Create a decision tree classifier object then create a GridSearchCV 
#object tree_cv with cv = 10. Fit the object to find the best parameters from 
#the dictionary parameters.
parameters = {'criterion': ['gini', 'entropy'],
     'splitter': ['best', 'random'],
     'max_depth': [2*n for n in range(1,10)],
     'max_features': ['auto', 'sqrt'],
     'min_samples_leaf': [1, 2, 4],
     'min_samples_split': [2, 5, 10]}
tree = DecisionTreeClassifier(max_features='sqrt')
Grid_tree = GridSearchCV(estimator=tree, param_grid=parameters, cv=10)
Grid_tree.fit(X_train, Y_train)
best_params = Grid_tree.best_params_
print(Grid_tree.best_score_)


### TASK 9: Calculate the accuracy of tree_cv on the test data using the method score
print(Grid_tree.score(X_test, Y_test)) # This gives the result based on the best estimator in the grid search
Yhat_test = Grid_tree.predict(X_test)  # This gives the result based on the best estimator in the grid search
plot_confusion_matrix(Y_test, Yhat_test)


### TASK 10: Create a k-nearest neighbors object then create a GridSearchCV 
#object knn_cv with cv = 10. Fit the object to find the best parameters from 
#the dictionary parameters.
parameters = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
              'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
              'p': [1,2]}

KNN = KNeighborsClassifier()
Grid_KNN = GridSearchCV(estimator=KNN, param_grid=parameters, cv=10)
Grid_KNN.fit(X_train, Y_train)
best_params = Grid_KNN.best_params_
print(Grid_KNN.best_score_)


### TASK 11: Calculate the accuracy of knn_cv on the test data using the method score
print(Grid_KNN.score(X_test, Y_test)) # This gives the result based on the best estimator in the grid search
Yhat_test = Grid_KNN.predict(X_test)  # This gives the result based on the best estimator in the grid search
plot_confusion_matrix(Y_test, Yhat_test)












