# -*- coding: utf-8 -*-
"""190496G_ML_Lab1_Label_3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GGCm7Cgq8KETn_x8qF3G9YtEGYnRLBTr
"""

import pandas as pd
import numpy as np

LABELS = ['label_1', 'label_2', 'label_3', 'label_4']
FEATURES = ['feature_'+ str(i) for i in range(1,257)]

train = pd.read_csv("drive/MyDrive/Colab Notebooks/Lab 1/train.csv")
valid = pd.read_csv("drive/MyDrive/Colab Notebooks/Lab 1/valid.csv")
test = pd.read_csv("drive/MyDrive/Colab Notebooks/Lab 1/test.csv")

print(LABELS)
print(FEATURES)

print(train.shape)
train.describe()

print(valid.shape)
valid.describe()

print(test.shape)
test.describe()

"""Preprocessing the data"""

train.info()

"""Label 2 has some empty values. These will be neglected when scaling using the standard scaler"""

train[train['label_2'].notna()].shape

from sklearn.preprocessing import StandardScaler

tr_df = train
vl_df = valid
tst_df = test

scaler = StandardScaler()

X_train = pd.DataFrame(scaler.fit_transform(tr_df.drop(LABELS, axis = 1)), columns = FEATURES)
Y_train = tr_df['label_3']
X_valid = pd.DataFrame(scaler.transform(vl_df.drop(LABELS, axis = 1)), columns = FEATURES)
Y_valid = vl_df['label_3']

X_test = pd.DataFrame(scaler.transform(tst_df.drop(LABELS, axis = 1)), columns = FEATURES)

X_train

Y_train

X_valid

Y_valid

X_train.describe()

"""### Now lets check the accuracy of prediction before feature engineering for label 3. Then let's predict the test dataset label value before feature engineering.

**Label 3 - Speaker Gender**

The value for label 3 (Speaker Gender) for the test dataset is predicted as follows.
"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

# Create a KNN model with k=5
k = 5
model = KNeighborsClassifier(n_neighbors=k)
model.fit(X_train, Y_train)
y_pred = model.predict(X_valid)

conf_matrix = metrics.confusion_matrix(Y_valid, y_pred)
accuracy = metrics.accuracy_score(Y_valid, y_pred)
precision = metrics.precision_score(Y_valid, y_pred, average='weighted')
recall = metrics.recall_score(Y_valid, y_pred, average='weighted')

print("Confusion Matrix:\n", conf_matrix)
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)

test_pred_before = model.predict(X_test)
df = pd.DataFrame(test_pred_before, columns=['label_3'])
print(df)
df.to_csv('predicted_label_3_before_feature_engineering.csv', index=False)

"""### Feature Engineering

PCA
"""

from sklearn.decomposition import PCA

pca = PCA(n_components= 0.67, svd_solver= 'full')
pca.fit(X_train)
X_train_after_pca = pd.DataFrame(pca.transform(X_train))
X_valid_after_pca = pd.DataFrame(pca.transform(X_valid))
X_test_after_pca = pd.DataFrame(pca.transform(X_test))
print(X_train_after_pca.shape)

k = 5
model_after_pca = KNeighborsClassifier(n_neighbors=k)
model_after_pca.fit(X_train_after_pca, Y_train)
y_pred_after_pca = model_after_pca.predict(X_valid_after_pca)
print(metrics.confusion_matrix(Y_valid,y_pred_after_pca))
print(metrics.accuracy_score(Y_valid,y_pred_after_pca))
print(metrics.precision_score(Y_valid,y_pred_after_pca, average = 'weighted'))
print(metrics.recall_score(Y_valid,y_pred_after_pca, average = 'weighted'))

"""Test data is predicted here"""

test_pred_after_pca = model_after_pca.predict(X_test_after_pca)
df_after = pd.DataFrame(test_pred_after_pca, columns=['label_3'])
print(df_after)
df_after.to_csv('predicted_label_3_after_feature_engineering.csv', index=False)

"""Getting the csv files after feature engineering"""

X_test_df_after = pd.DataFrame(X_test_after_pca)
print(X_test_df_after)
X_test_df_after.to_csv('new_features_label_3.csv', index=False)