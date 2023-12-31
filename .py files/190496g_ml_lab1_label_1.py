# -*- coding: utf-8 -*-
"""190496G_ML_Lab1_Label_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1edKACRGZhKzZXTlCkjbokeSSYhb2KrW8
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

train[train['label_3'].notna()].shape

train['label_4'].value_counts()

from sklearn.preprocessing import StandardScaler

tr_df = train
vl_df = valid
tst_df = test

scaler = StandardScaler()

X_train = pd.DataFrame(scaler.fit_transform(tr_df.drop(LABELS, axis = 1)), columns = FEATURES)
Y_train = tr_df['label_1']
X_valid = pd.DataFrame(scaler.transform(vl_df.drop(LABELS, axis = 1)), columns = FEATURES)
Y_valid = vl_df['label_1']

X_test = pd.DataFrame(scaler.transform(tst_df.drop(LABELS, axis = 1)), columns = FEATURES)

X_train

Y_train

X_train.describe()

"""### Now lets check the accuracy of prediction before feature engineering for label 1. Then let's predict the test dataset label value before feature engineering.

**Label 1 - Speaker Id**
"""

from sklearn import svm, metrics

model = svm.SVC(kernel = 'linear')
model.fit(X_train, Y_train)
y_pred = model.predict(X_valid)

print(metrics.confusion_matrix(Y_valid ,y_pred))
print(metrics.accuracy_score(Y_valid ,y_pred))
print(metrics.precision_score(Y_valid ,y_pred, average = 'weighted'))
print(metrics.recall_score(Y_valid ,y_pred, average = 'weighted'))

print(metrics.classification_report(Y_valid, y_pred))

"""The value for label 1 (Speaker ID) for the test dataset is predicted as follows."""

test_pred_before = model.predict(X_test)
df = pd.DataFrame(test_pred_before, columns=['label_1'])
print(df)
df.to_csv('predicted_label_1_before_feature_engineering.csv', index=False)

"""### Feature Engineering

PCA
"""

from sklearn.decomposition import PCA

pca = PCA(n_components= 0.95, svd_solver= 'full')
pca.fit(X_train)
X_train_after_pca = pd.DataFrame(pca.transform(X_train))
X_valid_after_pca = pd.DataFrame(pca.transform(X_valid))
X_test_after_pca = pd.DataFrame(pca.transform(X_test))
print(X_train_after_pca.shape)

model_after_pca = svm.SVC(kernel = 'linear')
model_after_pca.fit(X_train_after_pca, Y_train)
y_pred_after_pca = model_after_pca.predict(X_valid_after_pca)
print(metrics.confusion_matrix(Y_valid,y_pred_after_pca))
print(metrics.accuracy_score(Y_valid,y_pred_after_pca))
print(metrics.precision_score(Y_valid,y_pred_after_pca, average = 'weighted'))
print(metrics.recall_score(Y_valid,y_pred_after_pca, average = 'weighted'))

"""Test data is predicted here"""

test_pred_after_pca = model_after_pca.predict(X_test_after_pca)
df_after = pd.DataFrame(test_pred_after_pca, columns=['label_1'])
print(df_after)
df_after.to_csv('predicted_label_1_after_feature_engineering.csv', index=False)

"""Getting the csv files after feature engineering"""

NEW_COLUMNS = ['New_feature_'+ str(i) for i in range(1,68)]
X_test_df_after = pd.DataFrame(X_test_after_pca)
print(X_test_df_after)
X_test_df_after.to_csv('new_features_label_1.csv', index=False)