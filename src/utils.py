from functools import wraps
from exceptions import WrongColumnName
import pandas as pd
import numpy as np
import re
import convert_numbers
from sklearn.pipeline import Pipeline
# mean square error
from sklearn.metrics import mean_squared_error
def validate_columns(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        """ decorator to check if the column name is correct """
        try:
            if args[0].column not in args[1].columns:
                raise WrongColumnName(args[0])
            return f(*args, **kwargs)
        except AttributeError :
            pass
        # if its a list of columns
        for col in args[0].columns: 
            if col not in args[1].columns:
                print(col,args[1].columns)
                raise WrongColumnName(col)
        return f(*args, **kwargs)
    

    return decorated



def normalize_prev_owner(prev_owner: str) -> str or np.nan:
    # sourcery skip: compare-via-equals
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

def fill_by_mean_mode_of_year(row: pd.Series, car_data,column:str,type:str = 'mode') -> pd.Series:
    """this function is used to fill the null values of column with the mean of the silimlar data of the same year

    Args:
        row (pd.Series): the row of the dataframe 
    Returns:
        pd.Series: the row of the dataframe with the filled  column
    """
    if type not in ['mean','mode']:
        raise ValueError("type must be mean or mode")

    if column not in car_data.columns:
        raise WrongColumnName(column)
    # what is the value of float('nan')?
    # a: nan
    if row[column] not in [np.nan,np.NaN,None] :
        # check if numaric or not
        try:
            int(row[column])
            return row
        except ValueError:
            pass
        
    
   
    year = row['year']
    data = car_data[car_data['year'] == year]
    # drop the null values
    data = data[data[column].notna()]
    
    try :
        
        value = data[column].mode()[0] if type == 'mode'\
                                else data[column].mean()
        row[column] = value
        return row
    except KeyError:
        return row


def arabic_to_english(equation: str) -> str or np.nan:
    if pd.isnull(equation):
        return equation
    if type(equation) != str:
        return equation
    
    equation = equation.strip()
    equation = re.sub(r'[^a-zA-Z0-9\u0600-\u06FF]', '', equation)
    equation = convert_numbers.arabic_to_english(equation)
    equation = sum(int(i) for i in equation)
    return equation


def encoding_feature( df: pd.DataFrame, feature: str,order_dict:dict) -> pd.DataFrame:
    """this function is used to encode the nominal categorical features"""
    order = order_dict[feature]
    df[feature] = df[feature].map(order)
    return df


def encoding_additional_info(df: pd.DataFrame, feature: str,possible_values:list) -> pd.DataFrame:
        """this function is used to encode the additional_info feature"""
        df[feature] = df[feature].str.split(",")
        
        for i in possible_values:
            df[i] = df[feature].apply(lambda x: 1 if i in x else 0)
            
        return df
    

def train_models(models: dict,X_train:pd.DataFrame,y_train:pd.Series) -> dict:
    """ this function is used to train the models and return the trained models """
    for name,model in models.items():
        models[name]['model'] = Pipeline(steps=model['steps'])
        models[name]['model'].fit(X_train.copy(),y_train.copy())
    return models

def eval_models(models:dict,X_test:pd.DataFrame,y_test:pd.Series,type:str,metric = 'r2') -> dict:
    """ this function is used to evaluate the models and return the results """
    if type not in ['train','test']:
        raise ValueError("type must be train or test")
    if metric not in ['r2','mae','rmse','accuracy']:
        raise ValueError("metric must be r2 or mae or mse or accuracy")
    for name,model in models.items():
        print(f"evaluating {name} model")
        # eval based on the given metric eg: r2 , rmse , mae using score method
        from sklearn.metrics import r2_score,mean_squared_error,mean_absolute_error,accuracy_score
        if metric == 'r2':
            models[name][f'score_{type}'] = model['model'].score(X_test.copy(),y_test.copy())   
        elif metric == 'rmse':
            models[name][f'score_{type}'] = np.sqrt(mean_squared_error(y_test.copy(),model['model'].predict(X_test.copy())))
        elif metric == 'mae':
            models[name][f'score_{type}'] = mean_absolute_error(y_test.copy(),model['model'].predict(X_test.copy()))
        elif metric == 'accuracy':
            models[name][f'score_{type}'] = accuracy_score(y_test.copy(),model['model'].predict(X_test.copy()))

  
    return models


def log_transform(x):
    """ 
    Calculate log adding 1 to avoid calculation errors if x is very close to 0.
    """
    return np.log(x+1)