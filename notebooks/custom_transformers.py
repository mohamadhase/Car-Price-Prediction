from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np
import re
from sklearn.impute import KNNImputer
import convert_numbers
from sklearn.preprocessing import OneHotEncoder, LabelEncoder


class DateTransformer(BaseEstimator, TransformerMixin):
    """this class is used to extract the year"""

    def __init__(self, date_column):
        """this is the constructor of the class and it takes the name of the column to be transformed"""
        self.date_column = date_column

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X[self.date_column] = pd.to_datetime(
            X[self.date_column])
        X['sell_year'] = X[self.date_column].dt.year
        X.drop(self.date_column, axis=1, inplace=True)
        return X


class PrevOwnerTransformer(BaseEstimator, TransformerMixin):
    """this class is used to convert the previous owner column to int type """

    def __init__(self, prev_owner_column):
        self.prev_owner_column = prev_owner_column

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X[self.prev_owner_column] = X[self.prev_owner_column].apply(
            PrevOwnerTransformer.__normalize_prev_owner)
        X[self.prev_owner_column] = pd.to_numeric(
            X[self.prev_owner_column], errors='coerce')
        X = X.apply(PrevOwnerTransformer.__prev_owners_mean, args=(X,), axis=1)
        X = X[X[self.prev_owner_column].notna()]
        return X

    @staticmethod
    def __normalize_prev_owner(prev_owner: str) -> str or np.nan:
        """ convert the arabic writen discribtion about the prev_owners to a string number

        Args:
            prev_owner (str): the discribtion about the prev_owners

        Returns:
            str : the number of the prev_owners
            np.nan : if the prev_owner is np.nan

        """
        if prev_owner is np.nan:
            return np.nan
        try:
            return str(int(prev_owner))
        except ValueError:
            pass
        if re.search(r'صفر|مش|وارد|مان|احد|يوجد|استيراد|مستورد|شرك|انا', prev_owner):
            return '0'
        if re.search(r'أول|اول|1', prev_owner):
            return '1'
        if re.search(r'ثان|تان|2|اثنان', prev_owner):
            return '2'
        if re.search(r'ثالث|تالث|3|ثلاث|تلات|تالت', prev_owner):
            return '3'
        if re.search(r'رابع|4|اربع|اربعة|اربعه', prev_owner):
            return '4'
        if re.search(r'خامس|5|خمس|خمسة|خمسه', prev_owner):
            return '5'
        if re.search(r'سادس|6|سادسة|سادسه', prev_owner):
            return '6'
        if re.search(r'سابع|7|سابعة|سابعه', prev_owner):
            return '7'
        if re.search(r'ثامن|8|ثامنة|ثامنه', prev_owner):
            return '8'
        if re.search(r'تاسع|9|تاسعة|تاسعه', prev_owner):
            return '9'
        if re.search(r'عاشر|10|عشر|عشرة|عشره', prev_owner):
            return '10'
        if re.search('يد', prev_owner):
            try:
                return str(int(re.search(r'\d+', prev_owner).group()))
            except AttributeError:
                return np.nan
        if re.search(r'[^a-zA-Z0-9\u0600-\u06FF]', prev_owner):
            return np.nan
        return prev_owner

    def __prev_owners_mean(row: pd.Series, car_data) -> pd.Series:
        """this function is used to fill the prev_owners column with the mean of the prev_owners of the same year

        Args:
            row (pd.Series): the row of the dataframe 
        Returns:
            pd.Series: the row of the dataframe with the filled prev_owners column
        """
        if pd.notnull(row['prev_owners']):
            return row
        year = row['year']
        data = car_data[car_data['year'] == year]
        row['prev_owners'] = data['prev_owners'].mean()
        return row


class PassengerCpacityTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, passenger_capacity_column):
        self.passenger_capacity_column = passenger_capacity_column

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X['passenger_capacity'] = X['passenger_capacity'].apply(
            self.__arabic_to_english)
        imputer = KNNImputer(n_neighbors=5)
        X['passenger_capacity'] = imputer.fit_transform(
            X[['passenger_capacity']])
        X['passenger_capacity'] = X['passenger_capacity'].astype(int)
        return X

    def __arabic_to_english(self, equation: str) -> str or np.nan:
        if pd.isnull(equation):
            return equation
        equation = equation.strip()
        equation = re.sub(r'[^a-zA-Z0-9\u0600-\u06FF]', '', equation)
        equation = convert_numbers.arabic_to_english(equation)

        equation = sum([int(i) for i in equation])
        return equation


class NominalTransformer(BaseEstimator, TransformerMixin):
    """ this class takes a list of columns and apply one hot encoding on them """
    hot_encoder_data = {

    }

    def __init__(self, one_hot_encoder_columns):
        self.one_hot_encoder_columns = one_hot_encoder_columns

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        for column in self.one_hot_encoder_columns:  # not sure if this is work or not
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
        X.drop(self.one_hot_encoder_columns, axis=1, inplace=True)
        return X


class OrdenalTransformer(BaseEstimator, TransformerMixin):
    """this class takes a list of columns and apply label encoding on them"""

    def __init__(self, columns, order_dict):
        self.columns = columns
        self.order_dict = order_dict

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        for column in self.columns:
            X = self.__encoding_feature(X, column)
        return X

    def __encoding_feature(self, df: pd.DataFrame, feature: str) -> pd.DataFrame:
        """this function is used to encode the nominal categorical features"""
        order = self.ordinal_order[feature]
        df[feature] = df[feature].map(order)
        return df


class ColorTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, color_column):
        self.color_column = color_column

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X.drop(self.color_column, axis=1, inplace=True)
        return X


class AdditionalInfoTransformer(BaseEstimator, TransformerMixin):
    additinal_info = ['مسجل CD',
                      'جهاز إنذار',
                      'جنطات مغنيسيوم',
                      'فرش جلد',
                      'وسادة حماية هوائية',
                      'إغلاق مركزي',
                      'فتحة سقف',
                      'مُكيّف']

    def __init__(self, additional_info_column):
        self.additional_info_column = additional_info_column

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = self.__add_additional_info(X, self.additional_info_column)
        X.drop(self.additional_info_column, axis=1, inplace=True)
        return X

    def __encoding_additional_info(self, df: pd.DataFrame, feature: str) -> pd.DataFrame:
        """this function is used to encode the additional_info feature"""
        df[feature] = df[feature].str.split(",")
        for i in self.additinal_info:
            df[i] = df[feature].apply(lambda x: 1 if i in x else 0)
        return df

