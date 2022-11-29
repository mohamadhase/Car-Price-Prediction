from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np
import re
from sklearn.impute import KNNImputer
import convert_numbers
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from functools import wraps

from utils import fill_by_mean_mode_of_year , validate_columns, normalize_prev_owner, arabic_to_english, encoding_feature, encoding_additional_info


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
        X = X.apply(fill_by_mean_mode_of_year, args=(X,'prev_owners') ,axis=1) # fix the nan values after converting the column to numeric
        X = X[X[self.column].notna()] # drop the remaining nan values 
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
        return X


class NominalTransformer(BaseEstimator, TransformerMixin):
    """ this class takes a list of columns and apply one hot encoding on them """
    hot_encoder_data = {

    }

    def __init__(self, columns:list):
        self.columns = columns

    def fit(self, X: pd.DataFrame, y=None):
        return self

    @validate_columns
    def transform(self, X: pd.DataFrame, y=None):
        for column in self.columns:  # not sure if this is work or not
            if column in self.hot_encoder_data:
                classes = self.hot_encoder_data[column]['label_encoder'].classes_
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
                self.hot_encoder_data[column] = {
                    'label_encoder': label_encoder,
                    'one_hot_encoder': one_hot_encoder
                }
        X.drop(self.columns, axis=1, inplace=True)
        try :
             X.drop([column + '_label' for column in self.columns], axis=1, inplace=True)
        except KeyError :
            pass
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


class ColorTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, column):
        self.column = column

    def fit(self, X: pd.DataFrame, y=None):
        return self

    @validate_columns
    def transform(self, X: pd.DataFrame, y=None):
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
