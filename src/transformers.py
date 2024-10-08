from utils import fill_by_mean_mode_of_year, validate_columns, normalize_prev_owner, arabic_to_english, encoding_feature, encoding_additional_info
import pickle
import json
import sys
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np
import re
from sklearn.impute import KNNImputer
import convert_numbers
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from functools import wraps
# make the importing of the utils relative to the current file place
# so we can import the utils from the current directory
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# when i try import this file from this path CAR/ i got an error that the utlis module is not found
# a: you need to add the current directory to the path
sys.path.append(os.getcwd())


class DateTransformer(BaseEstimator, TransformerMixin):
    """this class is used to extract the year"""

    def __init__(self, column: str):
        self.column = column

    def fit(self, X: pd.DataFrame, y=None):
        return self

    @validate_columns
    def transform(self, X: pd.DataFrame, y=None):
        X[self.column] = pd.to_datetime(X[self.column])

        X[f"{self.column}.year"] = X[self.column].dt.year
        # convert the year to int and ignore the nan values by using the errors='coerce'
        X[f"{self.column}.year"] = X[f"{self.column}.year"].astype(
            int, errors='ignore')
        X.drop(self.column, axis=1, inplace=True)
        return X


class PrevOwnerTransformer(BaseEstimator, TransformerMixin):
    """this class is used to convert the previous owner column to int type """

    def __init__(self, column):
        self.column = column

    def fit(self, X: pd.DataFrame, y=None):
        return self

    @validate_columns
    def transform(self, X: pd.DataFrame, y=None):
        X[self.column] = X[self.column].apply(normalize_prev_owner)
        X[self.column] = pd.to_numeric(X[self.column], errors='coerce')
        # fix the nan values after converting the column to numeric
        X = X.apply(fill_by_mean_mode_of_year, args=(X, 'prev_owners'), axis=1)
        X = X[X[self.column].notna()]  # drop the remaining nan values
        return X


class PassengerCpacityTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, column):
        self.column = column

    def fit(self, X: pd.DataFrame, y=None):
        return self

    @validate_columns
    def transform(self, X: pd.DataFrame, y=None):
        X[self.column] = X[self.column].apply(arabic_to_english)
        X[self.column] = X[self.column].astype(int, errors='ignore')
        imputer = KNNImputer(n_neighbors=5)
        X[self.column] = imputer.fit_transform(X[[self.column]])
        X[self.column] = X[self.column].astype(int)

        return X


class NominalTransformer(BaseEstimator, TransformerMixin):
    """ this class takes a list of columns and apply one hot encoding on them """
    hot_encoder_data = {

    }

    def __init__(self, columns: list):
        self.columns = columns

    def fit(self, X: pd.DataFrame, y=None):

        return self

    @validate_columns
    def transform(self, X: pd.DataFrame, y=None):
        try:
            # load the hot encoder data from the pickle file
            for column in self.columns:
                with open(f'../models/{column}_label_encoder.pkl', 'rb') as handle:
                    self.hot_encoder_data[column] = pickle.load(handle)
        except Exception as e:
            print(e)
        for column in self.columns:  
            if column in NominalTransformer.hot_encoder_data:
                classes = NominalTransformer.hot_encoder_data[column].classes_
                # add every class as a column with value 0 if it is not equal the column value and 1 if it is
                X = X.join(pd.DataFrame(np.where(X[column].values[:, None] == classes, 1, 0),
                                        columns=classes, index=X.index))
            else:
                label_encoder = LabelEncoder()
                feature_labels = label_encoder.fit_transform(X[column])
                X[column+"_label"] = feature_labels
                one_hot_encoder = OneHotEncoder()
                feature_labels = one_hot_encoder.fit_transform(
                    X[[column + '_label']]).toarray()
                feature_feature_labels = (label_encoder.classes_)
                feature_features = pd.DataFrame(
                    feature_labels, columns=feature_feature_labels)
                feature_features.reset_index(drop=True, inplace=True)
                X.reset_index(drop=True, inplace=True)
                X = pd.concat([X, feature_features], axis=1)

                # save each class and its
                NominalTransformer.hot_encoder_data[column] = label_encoder
        X.drop(self.columns, axis=1, inplace=True)
        try:
            X.drop([column + '_label' for column in self.columns],
                   axis=1, inplace=True)
        except KeyError:
            pass
        # for each column save the label encoder model in file called coulmn_label_encoder.pkl
        for column in self.columns:
            with open(f'../models/{column}_label_encoder.pkl', 'wb') as f:
                pickle.dump(NominalTransformer.hot_encoder_data[column], f)
        return X


class OrdenalTransformer(BaseEstimator, TransformerMixin):
    """this class takes a list of columns and apply label encoding on them"""

    def __init__(self, columns, order_dict):
        self.columns = columns
        self.order_dict = order_dict

    def fit(self, X: pd.DataFrame, y=None):
        return self

    @validate_columns
    def transform(self, X: pd.DataFrame, y=None):
        for column in self.columns:
            X = encoding_feature(X, column, self.order_dict)
        return X


class CarNameTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, column):
        self.column = column

    def fit(self, X: pd.DataFrame, y=None):
        return self

    @validate_columns
    def transform(self, X: pd.DataFrame, y=None):
        X['company_name'] = X[self.column].apply(lambda x: x.split()[0])
        X.drop(self.column, axis=1, inplace=True)
        return X


class AdditionalInfoTransformer(BaseEstimator, TransformerMixin):
    POSSIBLE_ADDITONALS = ['مسجل CD',
                           'جهاز إنذار',
                           'جنطات مغنيسيوم',
                           'فرش جلد',
                           'وسادة حماية هوائية',
                           'إغلاق مركزي',
                           'فتحة سقف',
                           'مُكيّف']

    def __init__(self, column):
        self.column = column

    def fit(self, X: pd.DataFrame, y=None):
        return self

    @validate_columns
    def transform(self, X: pd.DataFrame, y=None):
        X = encoding_additional_info(X, self.column, self.POSSIBLE_ADDITONALS)
        X.drop(self.column, axis=1, inplace=True)
        return X


class log_transformer(BaseEstimator, TransformerMixin):
    # this class apply the log transformation for all the numerical columns
    def __init__(self):
        pass

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame, y=None):
        print(X)
        for column in X.columns:
            if X[column].dtype in ['int64', 'float64', 'int32', 'float32']:
                X[column] = np.log(X[column])
            print(X[X.isna()])
        return X
