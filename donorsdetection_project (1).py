# -*- coding: utf-8 -*-
"""DonorsDetection_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_jLQOrd6LLcnTKMES88ob6z2sYEWBYUg
"""

#Importing the necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from collections import Counter
from sklearn.model_selection import cross_val_score
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import f1_score
from sklearn.metrics import auc
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve
from numpy import where
from sklearn.metrics import roc_auc_score
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from scipy.stats import chi2_contingency
from scipy import stats as st
from sklearn import metrics
from IPython.display import display
from sklearn.preprocessing import PowerTransformer, QuantileTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from pprint import pprint
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import MinMaxScaler

"""IMPORTING THE DATASET"""

#reading csv
df_donor_data = pd.read_csv("Final Donors List.csv")

#shape of the dataset
df_donor_data.shape

#info of the dataset
df_donor_data.info()

df_donor_data.head(5)

#finding the unique values in the target variable
df_donor_data["RFM_Segment"].unique()

#count plot of the target variable
sns.set(rc = {'figure.figsize':(15,8)})
sns.countplot(x='RFM_Segment', data=df_donor_data, palette= ['royalblue'])
plt.show()

"""HANDLING MISSING VALUES"""

#missing values in the dataset
#the missing values in the datset are filled with a question mark

#replacing? with nan
df_donor_data = df_donor_data.replace('?', np.nan)

#counting the  missing values
df_donor_data.apply(lambda x: sum(x.isnull()),axis=0)

#Dropping features with high number of missing values and irrelevant to the analysis

df_donor_data = df_donor_data.drop(columns=['ID', 'FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME','INFORMAL', 'ADDRESS_2','ZIP', 'COUNTRY','BIRTHDATE', 'ADDRESS UPDATED','WORK_PHONE', 'WORK PHONE UPDATED','HOME_PHONE', 'HOME PHONE UPDATED', 'CELL_PHONE', 'CELL PHONE UPDATED', 'EMAIL', 'EMAIL UPDATED', 'Date of Birth' ])

#deleting other columns which are not relevant
df_donor_data = df_donor_data.drop(columns=['ADDRESS_1', 'DO_NOT_SOLICIT', 'NO_FOUNDATION_MAIL', 'Bequest',
                                                               'Attribute 1_x', 'Status'])

"""DATA EXPLORATION"""

sns.set(rc = {'figure.figsize':(20,8)})
sns.countplot(x='Net Worth Estimation', data=df_donor_data, palette= ['royalblue'])
plt.show()

sns.set(rc = {'figure.figsize':(20,8)})
sns.countplot(x='Gift Officer Name_x', data=df_donor_data, palette= ['royalblue'])
plt.show()

sns.set(rc = {'figure.figsize':(60,20)})
sns.countplot(x='Chapter', data=df_donor_data, palette= ['royalblue'], order=df_donor_data['Chapter'].value_counts().index )
plt.xticks(rotation = 90, ) # Rotates X-Axis Ticks by 90-degrees
plt.show()

df_donor_data['Chapter'].nunique()

sns.set(rc = {'figure.figsize':(20,8)})
sns.countplot(x='Target Tier', data=df_donor_data, palette= ['royalblue'])
plt.show()

"""CREATING CALUCULATED FIELDS"""

df_donor_data['PLEDGE DATE'] = pd.to_datetime(df_donor_data['PLEDGE DATE'])

df_donor_data.info()

df_donor_data['Pledge_year'] = pd.DatetimeIndex(df_donor_data['PLEDGE DATE']).year

from datetime import date
today = date.today()
df_donor_data["Pledge_years"]  = today.year - df_donor_data['Pledge_year']

df_donor_data = df_donor_data.drop(columns=['PLEDGE DATE', 'BccAmount', 'BccReceived', 'BccBalance', 'BCC Chapter Status','Gift Officer Name_x'
                                                               , 'Pledge_year'])

df_donor_data = df_donor_data.reindex(columns=['Unnamed: 0','CITY','STATE_PROVINCE','INITIATION DATE', 'UNIV', 'Chapter','GRADUATION DATE','Age Calculated field', 'Net Worth Estimation',
       'Inclination: Giving', 'Income', 'Charitable Donations', 'Total Donation Sum', 'Number of Years Donated','Average Donation Value',
                                                                'Percentile_Donation_Amount', 'DLV',
                                                               'Percentile_Donation_Freq','BCC Donor', 'BCC Chapter ', 'Gift Capacity Range (M&L)', 'Target Tier',
       'Pledge_years', 'RFM_Segment'])

sns.set(rc = {'figure.figsize':(20,8)})
sns.countplot(x='STATE_PROVINCE', data=df_donor_data, palette= ['royalblue'], order=df_donor_data['STATE_PROVINCE'].value_counts().index )
plt.xticks(rotation = 90, ) # Rotates X-Axis Ticks by 90-degrees)
plt.show()

df_donor_data['STATE_PROVINCE'].unique()

df_donor_data['STATE_PROVINCE'] = df_donor_data['STATE_PROVINCE'].str.upper()

df_donor_data['STATE_PROVINCE'].unique()

sns.set(rc = {'figure.figsize':(20,8)})
sns.countplot(x='STATE_PROVINCE', data=df_donor_data, palette= ['royalblue'], order=df_donor_data['STATE_PROVINCE'].value_counts().index )
plt.xticks(rotation = 90, ) # Rotates X-Axis Ticks by 90-degrees))
plt.show()

df_donor_data['CITY'] = df_donor_data['CITY'].str.upper()
print("number of uniques values in CITY variable", df_donor_data['CITY'].nunique())

"""CONVERTING THE CATEGORICAL VARIABLES"""

df_donor_data['UNIV'], _ = pd.factorize(df_donor_data['UNIV'])

df_donor_data['Chapter'], _ = pd.factorize(df_donor_data['Chapter'])
df_donor_data['STATE_PROVINCE'], _ = pd.factorize(df_donor_data['STATE_PROVINCE'])
df_donor_data['CITY'], _ = pd.factorize(df_donor_data['CITY'])

df_donor_data['INITIATION DATE'] = pd.to_datetime(df_donor_data['INITIATION DATE'])

df_donor_data['initiation_year'] = pd.DatetimeIndex(df_donor_data['INITIATION DATE']).year

from datetime import date
today = date.today()
df_donor_data["initiation_years"]  = today.year - df_donor_data['initiation_year']

df_donor_data = df_donor_data.drop(columns=['INITIATION DATE','initiation_year'])

"""NORMALIZING THE NUMERICAL VARIABLES"""

from sklearn.preprocessing import PowerTransformer, QuantileTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from pprint import pprint
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import MinMaxScaler

num_cols = df_donor_data.columns[df_donor_data.dtypes.apply(lambda c: np.issubdtype(c, np.number))]

# used MinMaxScaler to Normalize the data
scaler = MinMaxScaler()
df_donor_data[num_cols] = scaler.fit_transform(df_donor_data[num_cols])

list(df_donor_data.columns)

df_donor_data_corr = df_donor_data #dataframe for factorised data of categorical values
df_donor_data_onh = df_donor_data #dataframe for one hot encoded data of categorical values

#factorising the categorical variables
df_donor_data_corr['Age Calculated field'], _ = pd.factorize(df_donor_data_corr['Age Calculated field'])
df_donor_data_corr['Inclination: Giving'], _ = pd.factorize(df_donor_data_corr['Inclination: Giving'])
df_donor_data_corr['Net Worth Estimation'], _ = pd.factorize(df_donor_data_corr['Net Worth Estimation'])
df_donor_data_corr['Income'], _ = pd.factorize(df_donor_data_corr['Income'])
df_donor_data_corr['Charitable Donations'], _ = pd.factorize(df_donor_data_corr['Charitable Donations'])
df_donor_data_corr['BCC Donor'], _ = pd.factorize(df_donor_data_corr['BCC Donor'])
df_donor_data_corr['BCC Chapter '], _ = pd.factorize(df_donor_data_corr['BCC Chapter '])
df_donor_data_corr['Gift Capacity Range (M&L)'], _ = pd.factorize(df_donor_data_corr['Gift Capacity Range (M&L)'])
df_donor_data_corr['Target Tier'], _ = pd.factorize(df_donor_data_corr['Target Tier'])

df_donor_data_corr.head()

df_donor_data_corr = df_donor_data_corr.drop(columns=['Unnamed: 0'])

#visualize the correlation of factorised variables
plt.figure(figsize=(20, 8))
heatmap = sns.heatmap(df_donor_data_corr.corr(), vmin=-1, vmax=1, annot=True, cmap='BrBG')
heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':10}, pad=12);

#dropping the variables which are highly correlated with a value of "1"
df_donor_data_corr = df_donor_data_corr.drop(columns=['UNIV','DLV','Pledge_years'])

df_donor_data_corr.info()

df_donor_data_corr['RFM_Segment'].unique()

df_donor_data_corr['RFM_Segment'] = df_donor_data_corr['RFM_Segment'].map({"Can't Loose Them": 7, 'Champions': 6, "Loyal": 5, "Promising": 4, "Potential": 3, "Needs Attention": 2, "Require Activation": 1, "One hit wonders": 0})

df_donor_data_corr.info()

df_donor_data_corr.head()

df_donor_data_corr['RFM_Segment'].unique()

df_donor_data_corr.fillna(0)

np.any(np.isnan(df_donor_data_corr))

print(df_donor_data_corr.isnull().sum())

sns.boxplot(df_donor_data_corr['initiation_years'])

#assuming missing values in initiation years as '0' they have not pledged but donated
df_donor_data_corr['initiation_years'] = df_donor_data_corr['initiation_years'].fillna(0)

print(df_donor_data_corr.isnull().sum())

"""TRAIN TEST SPLIT OF DATA"""

#Startified train test Split-out dataset
from sklearn.model_selection import train_test_split

features = []
for feature in df_donor_data_corr.columns:
    if feature != 'RFM_Segment':
        features.append(feature)
X = df_donor_data_corr[features]
Y = df_donor_data_corr['RFM_Segment']

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, stratify=Y, test_size=0.25)

Y_train.unique()

Y_test.unique()

np.any(np.isnan(X_train))

np.all(np.isfinite(X_train))

X_train.apply(lambda x: sum(x.isnull()),axis=0)

"""RANDOM FOREST MODEL"""

#Fitting the Random Forest
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

forest = RandomForestClassifier(n_estimators=10, random_state=42)
forest.fit(X_train, Y_train)

#the accuracy on the training data
print('Accuracy on the training data',forest.score(X_train,Y_train))

#confusion_matrix for the training
disp = plot_confusion_matrix(forest, X_train, Y_train ,display_labels=None, cmap=plt.cm.Blues)

# Testing the Random Forest Model

#the accuracy on the test data
print('Accuracy on the test data', forest.score(X_test, Y_test))

#Precision, Recall & F1-Score
Y_pred = forest.predict(X_test)
print('Precision: %.3f' % precision_score(Y_test, Y_pred, average='weighted'))
print('Recall: %.3f' % recall_score(Y_test, Y_pred, average='weighted'))
print('F1 Score: %.3f' % f1_score(Y_test, Y_pred, average='weighted'))

#confusion_matrix for the testing
disp = plot_confusion_matrix(forest, X_test, Y_test ,display_labels=None, cmap=plt.cm.Blues)

# Define parameters
max_depth=[2, 4, 8, 12, 16, 20]
n_estimators = [64, 128, 256, 512]
param_grid = dict(max_depth=max_depth, n_estimators=n_estimators)

# Build the gridsearch
dfrst = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
grid = GridSearchCV(estimator=dfrst, param_grid=param_grid, cv = 5)
grid_results = grid.fit(X_train, Y_train)

# Summarize the results in a readable format
print("Best: {0}, using {1}".format(grid_results.cv_results_['mean_test_score'], grid_results.best_params_))
results_df = pd.DataFrame(grid_results.cv_results_)
results_df

# Extract the best decision forest
best_clf = grid_results.best_estimator_
Y_pred = best_clf.predict(X_test)

print('Precision: %.3f' % precision_score(Y_test, Y_pred, average='weighted'))
print('Recall: %.3f' % recall_score(Y_test, Y_pred, average='weighted'))
print('F1 Score: %.3f' % f1_score(Y_test, Y_pred, average='weighted'))

# Create a confusion matrix
cnf_matrix = confusion_matrix(Y_test, Y_pred)

# Create heatmap from the confusion matrix
class_names=[False, True] # name  of classes
fig, ax = plt.subplots(figsize=(7, 6))
sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="Blues", fmt='g')
ax.xaxis.set_label_position("top")
plt.tight_layout()
plt.title('Confusion matrix')
plt.ylabel('Actual label'); plt.xlabel('Predicted label')

print(metrics.classification_report(Y_test, Y_pred, digits=8))

from sklearn.preprocessing import label_binarize
best_clf = grid_results.best_estimator_
Y_score = best_clf.predict_proba(X_test)

#Binarize the output
y_test_bin = label_binarize(Y_test, classes=[0, 1, 2, 3, 4, 5, 6,7])
n_classes = y_test_bin.shape[1]

fpr = dict()
tpr = dict()
roc_auc = dict()

for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], Y_score[:, i])
    plt.plot(fpr[i], tpr[i], lw=2)
    print('AUC for Class {}: {}'.format(i+1, auc(fpr[i], tpr[i])))

plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic Curves')
plt.show()

"""NAIVE BAYES MODEL"""

#Fitting the Naive Bayes Model - Baseline

gnb = GaussianNB().fit(X_train, Y_train)

#accuracy on the training data
gnb_train_acc = gnb.score(X_train,Y_train)
print('Accuracy for the Naive Bayes Model on the training data %.4f' % (gnb_train_acc*100))

#confusion_matrix for the training
disp = plot_confusion_matrix(gnb, X_train, Y_train ,display_labels = None, cmap=plt.cm.Blues)

#Testing the Naive Bayes Model- Baseline

#the accuracy on the test data
gnb_test_acc = gnb.score(X_test,Y_test)
print('Accuracy for the Naive Bayes Model on the test data %.4f' % (gnb_test_acc*100) )

#Precision, Recall & F1-Score
Y_naiveb = gnb.predict(X_test)
print('Precision: %.4f' % precision_score(Y_test, Y_naiveb, average='weighted'))
print('Recall: %.4f' % recall_score(Y_test, Y_naiveb, average='weighted'))
print('F1 Score: %.4f' % f1_score(Y_test, Y_naiveb, average='weighted'))

#confusion_matrix for the testing
disp = plot_confusion_matrix(gnb, X_test, Y_test ,display_labels=None, cmap=plt.cm.Blues)

#Hyperparameter Tuning the Naive Bayes Model

#Create the parameter grid
param_grid = {'var_smoothing': np.logspace(0,-9, num=25)}

gnb = GaussianNB()

# search of parameters, using 3 fold cross validation,
# search across 25 different combinations
gnb_random = GridSearchCV(gnb, param_grid, cv = 3, scoring = 'recall_weighted', refit = True, verbose = 3)

# Fit the random search model
gnb_random.fit(X_train, Y_train)

#print best parameters
print(gnb_random.best_params_)

#accuracy for best estimator
bestgnb = gnb_random.best_estimator_
best_gnb_acc = bestgnb.score(X_train,Y_train)
print('Accuracy of the Naive Bayes model data with hyperparameter tuning:  %.4f' % (best_gnb_acc*100))

#Precision, Recall & F1-Score
y_naivebhp = bestgnb.predict(X_test)
print('Precision: %.4f' % precision_score(Y_test, y_naivebhp, average='weighted'))
print('Recall: %.4f' % recall_score(Y_test, y_naivebhp, average='weighted'))
print('F1 Score: %.4f' % f1_score(Y_test, y_naivebhp, average='weighted'))

#confusion_matrix for the testing
disp = plot_confusion_matrix(bestgnb, X_test, Y_test ,display_labels=None, cmap=plt.cm.Blues)

print(metrics.classification_report(Y_test, y_naivebhp, digits=8))



"""K - MEANS CLUSTERING - UNSUPERVISED LEARNING"""

df_donor_data_kmeans = df_donor_data_corr.drop(columns=['RFM_Segment'])

# first we would like to know that how many cluster or to say donors can be clustered
# with less SSE(Sum of Squared Error) we will use "Elbow method" to find out

# KMeans instance
from sklearn.cluster import KMeans
km = KMeans()
k_rng = range(1,21)  # k value
sse = [] # sse value for each k
for i in k_rng:
    km = KMeans(n_clusters = i)
    km.fit(df_donor_data_kmeans)
    # calculating sse
    sse.append(km.inertia_)

plt.plot(k_rng, sse, color = 'green')
plt.xlabel('K value')
plt.ylabel('SSE')
plt.title('Best K value')
plt.show()

df_donor_data_kmeans5 = df_donor_data_kmeans
df_donor_data_kmeans6 = df_donor_data_kmeans
df_donor_data_kmeans7 = df_donor_data_kmeans
df_donor_data_kmeans8 = df_donor_data_kmeans

#with 5 clusters
kmeans5 = KMeans(n_clusters=5, init='k-means++', random_state=0).fit(df_donor_data_kmeans5)
df_donor_data_kmeans5['cluster5'] = kmeans5.predict(df_donor_data_kmeans5)

from collections import Counter
Counter(kmeans5.labels_)

from sklearn.manifold import TSNE
donor_embedding5 = TSNE(n_components=2, verbose=2).fit_transform(df_donor_data_kmeans5)
projection5 = pd.DataFrame(columns=['x', 'y'], data=donor_embedding5)

projection5['cluster5'] = df_donor_data_kmeans5['cluster5']

projection5.head()

import plotly.express as px

fig5 = px.scatter(projection5, x='x', y='y', color='cluster5', hover_data=['x', 'y'])
fig5.show()

#with 6 clusters
kmeans6 = KMeans(n_clusters=6, init='k-means++', random_state=0).fit(df_donor_data_kmeans6)
df_donor_data_kmeans6['cluster6'] = kmeans6.predict(df_donor_data_kmeans6)

#TSNE -converting high dimensions into 2 dimensions
donor_embedding6 = TSNE(n_components=2, verbose=2).fit_transform(df_donor_data_kmeans6)
projection6 = pd.DataFrame(columns=['x', 'y'], data=donor_embedding6)

#adding cluster value to the reduced dimension dataframe
projection6['cluster6'] = df_donor_data_kmeans6['cluster6']

#plotting the cluster
fig6 = px.scatter(projection6, x='x', y='y', color='cluster6', hover_data=['x', 'y'])
fig6.show()

#with 7 clusters
kmeans7 = KMeans(n_clusters=7, init='k-means++', random_state=0).fit(df_donor_data_kmeans7)
df_donor_data_kmeans7['cluster7'] = kmeans7.predict(df_donor_data_kmeans7)

#TSNE -converting high dimensions into 2 dimensions
donor_embedding7 = TSNE(n_components=2, verbose=2).fit_transform(df_donor_data_kmeans7)
projection7 = pd.DataFrame(columns=['x', 'y'], data=donor_embedding7)

#adding cluster value to the reduced dimension dataframe
projection7['cluster7'] = df_donor_data_kmeans7['cluster7']

#plotting the cluster
fig7 = px.scatter(projection7, x='x', y='y', color='cluster7', hover_data=['x', 'y'])
fig7.show()

#with 8 clusters
kmeans8 = KMeans(n_clusters=8, init='k-means++', random_state=0).fit(df_donor_data_kmeans8)
df_donor_data_kmeans8['cluster8'] = kmeans8.predict(df_donor_data_kmeans8)

#TSNE -converting high dimensions into 2 dimensions
donor_embedding8 = TSNE(n_components=2, verbose=2).fit_transform(df_donor_data_kmeans8)
projection8 = pd.DataFrame(columns=['x', 'y'], data=donor_embedding8)

#adding cluster value to the reduced dimension dataframe
projection8['cluster8'] = df_donor_data_kmeans8['cluster8']

#plotting the cluster
fig8 = px.scatter(projection8, x='x', y='y', color='cluster8', hover_data=['x', 'y'])
fig8.show()

df_donor_data_kmeans10 = df_donor_data_kmeans
#with 10 clusters
kmeans10 = KMeans(n_clusters=10, init='k-means++', random_state=0).fit(df_donor_data_kmeans10)
df_donor_data_kmeans10['cluster10'] = kmeans10.predict(df_donor_data_kmeans10)

#TSNE -converting high dimensions into 2 dimensions
donor_embedding10 = TSNE(n_components=2, verbose=2).fit_transform(df_donor_data_kmeans10)
projection10 = pd.DataFrame(columns=['x', 'y'], data=donor_embedding10)

#adding cluster value to the reduced dimension dataframe
projection10['cluster10'] = df_donor_data_kmeans10['cluster10']

#plotting the cluster
fig10 = px.scatter(projection10, x='x', y='y', color='cluster10', hover_data=['x', 'y'])
fig10.show()

df_donor_data_kmeans12 = df_donor_data_kmeans
#with 12 clusters
kmeans12 = KMeans(n_clusters=12, init='k-means++', random_state=0).fit(df_donor_data_kmeans12)
df_donor_data_kmeans12['cluster12'] = kmeans12.predict(df_donor_data_kmeans12)

#TSNE -converting high dimensions into 2 dimensions
donor_embedding12 = TSNE(n_components=2, verbose=2).fit_transform(df_donor_data_kmeans12)
projection12 = pd.DataFrame(columns=['x', 'y'], data=donor_embedding12)

#adding cluster value to the reduced dimension dataframe
projection12['cluster12'] = df_donor_data_kmeans12['cluster12']

#plotting the cluster
fig12 = px.scatter(projection12, x='x', y='y', color='cluster12', hover_data=['x', 'y'])
fig12.show()

df_donor_data_kmeans4 = df_donor_data_kmeans
#with 4 clusters
kmeans4 = KMeans(n_clusters=4, init='k-means++', random_state=0).fit(df_donor_data_kmeans4)
df_donor_data_kmeans4['cluster4'] = kmeans4.predict(df_donor_data_kmeans4)

#TSNE -converting high dimensions into 2 dimensions
donor_embedding4 = TSNE(n_components=2, verbose=2).fit_transform(df_donor_data_kmeans4)
projection4 = pd.DataFrame(columns=['x', 'y'], data=donor_embedding4)

#adding cluster value to the reduced dimension dataframe
projection4['cluster4'] = df_donor_data_kmeans4['cluster4']

#plotting the cluster
fig4 = px.scatter(projection4, x='x', y='y', color='cluster4', hover_data=['x', 'y'])
fig4.show()

"""K-NEAREST NEIGHBOR (KNN) MODEL"""

#Fitting the KNN moel - Baseline

knn = KNeighborsClassifier().fit(X_train, Y_train)

#accuracy on the training data
knn_train_acc = knn.score(X_train,Y_train)
print('Accuracy for the KNeighborsClassifier on the training data %.4f'  % (knn_train_acc*100))

#confusion_matrix for the training
disp = plot_confusion_matrix(knn, X_train, Y_train ,display_labels=None, cmap=plt.cm.Blues)

# Testing the KNN Model- Baseline

#the accuracy on the test data
knn_test_acc = knn.score(X_test,Y_test)
print('Accuracy for the KNeighborsClassifier on the testing data %.4f'  % (knn_test_acc*100))

#Precision, Recall & F1-Score
Y_KNN = knn.predict(X_test)
print('Precision: %.4f' % precision_score(Y_test, Y_KNN, average='weighted'))
print('Recall: %.4f' % recall_score(Y_test, Y_KNN, average='weighted'))
print('F1 Score: %.4f' % f1_score(Y_test, Y_KNN, average='weighted'))

#confusion_matrix for the testing
disp = plot_confusion_matrix(knn, X_test, Y_test ,display_labels=None, cmap=plt.cm.Blues)

#Hyperparameter Tuning the KNN Model
#Create the parameter grid
param_grid = {'n_neighbors' : [5,10,15,20]}

knn = KNeighborsClassifier()

# search of parameters, using 3 fold cross validation,
# search across 4 different combinations
knn_random = GridSearchCV(knn, param_grid, cv = 3, scoring = 'recall_weighted', refit = True, verbose = 3)

# Fit the random search model
knn_random.fit(X_train, Y_train)

#print best parameters
print('The best parameters: ', knn_random.best_params_)

#accuracy for best estimator
bestknn = knn_random.best_estimator_
best_knn_acc = bestknn.score(X_train,Y_train)
print('Accuracy of the KNN model with hyperparameter tuning:  %.4f' % (best_knn_acc*100))

#Precision, Recall & F1-Score
Y_knnhp = bestknn.predict(X_test)
print('Precision: %.4f' % precision_score(Y_test, Y_knnhp, average='weighted'))
print('Recall: %.4f' % recall_score(Y_test, Y_knnhp, average='weighted'))
print('F1 Score: %.4f' % f1_score(Y_test, Y_knnhp, average='weighted'))

#confusion_matrix for the testing
disp = plot_confusion_matrix(bestknn, X_test, Y_test ,display_labels=None, cmap=plt.cm.Blues)

print(metrics.classification_report(Y_test, Y_knnhp, digits=8))

"""LOGISTIC REGRESSION"""

#Fitting the Regression moel - Baseline

logistic = LogisticRegression(solver='liblinear', max_iter = 1000).fit(X_train, Y_train)

logistic_train_acc = logistic.score(X_train,Y_train)
print('Accuracy for the Logistic Regression model on the training data %.4f' % (logistic_train_acc*100))

#confusion_matrix for the training
disp = plot_confusion_matrix(logistic, X_train, Y_train ,display_labels=None, cmap=plt.cm.Blues)

#coefficients
#pd.DataFrame(zip(X_train.columns, np.transpose(logistic.coef_.tolist()[0])), columns=['features', 'coef'])

# Testing the logistic Regression Model - Baseline

#the accuracy on the test data
logistic_test_acc = logistic.score(X_test,Y_test)
print('Accuracy for the Logistic Regression model on the test data %.4f' % (logistic_test_acc*100))

#Precision, Recall & F1-Score
Y_logi = logistic.predict(X_test)
print('Precision: %.4f' % precision_score(Y_test, Y_logi, average='weighted'))
print('Recall: %.4f' % recall_score(Y_test, Y_logi, average='weighted'))
print('F1 Score: %.4f' % f1_score(Y_test, Y_logi, average='weighted'))

#confusion_matrix for the testing
disp = plot_confusion_matrix(logistic, X_test, Y_test ,display_labels=None, cmap=plt.cm.Blues)

#Hyperparameter Tuning the logistic regression Model
#Create the parameter grid
param_grid = {'solver':['newton-cg', 'lbfgs'],
              'C': [0.1,0.2,0.4,0.8,1.0]}

LR = LogisticRegression(multi_class='multinomial', max_iter = 1000)

# search of parameters, using 3 fold cross validation,
# search across 12 different combinations
LR_random = GridSearchCV(LR, param_grid, cv = 3, scoring = "recall_weighted", refit = True, verbose = 3)

# Fit the random search model
LR_random.fit(X_train, Y_train)

#print best parameters
print('The best parameters: ', LR_random.best_params_)

#accuracy for best estimator
bestlogistic = LR_random.best_estimator_
best_logistic_acc = bestlogistic.score(X_train,Y_train)
print('Accuracy of the Logistic Regression model with hyperparameter tuning:  %.4f' % (best_logistic_acc*100))
#Precision, Recall & F1-Score
Y_logihp = bestlogistic.predict(X_test)
print('Precision: %.4f' % precision_score(Y_test, Y_logihp, average='weighted'))
print('Recall: %.4f' % recall_score(Y_test, Y_logihp, average='weighted'))
print('F1 Score: %.4f' % f1_score(Y_test, Y_logihp, average='weighted'))

#confusion_matrix for the testing
disp = plot_confusion_matrix(bestlogistic, X_test, Y_test ,display_labels=None, cmap=plt.cm.Blues)

print(metrics.classification_report(Y_test, Y_logihp, digits=8))

