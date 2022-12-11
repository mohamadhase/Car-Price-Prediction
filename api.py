import pickle
import pandas as pd

from http import HTTPStatus
import pydantic
import uvicorn
from src.data_handler import CarFeaturesPrediction
import logging

from fastapi import FastAPI, Request
#print my current path 
import os
import src.transformers
import utils
import sys

sys.path.append(os.getcwd())
app = FastAPI(
    title="CAR PRICE PREDICTION API",
    description="..",
    version="0.1",
)
logger = logging.getLogger(__name__)
logging.basicConfig(filename='../logs/CarPrediction.log', level=logging.DEBUG)

try: 
    DesicionTreeModel = pickle.load(open('../models/Polynomial.pkl', 'rb')) # could not find the file the path of the file is CAR/MODELS/DecisionTree.pkl

except FileNotFoundError as e:
    #print the relative path of the script
    print(e)
    logger.exception(e)
    exit()

@app.get("/health")
def _health_check(request: Request) -> dict:
    """Health check."""
    logger.info("Health check")
    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {},
    }
    logger.info("Health check successful")
    return response


@app.post("/predict")
# the CarFeatures class attributes are optional becouse i used it in parsing the data 
# can we make them required only in the post request without effecting the parsing process ? 
# a: yes we can, i will show you how in the next snippet
async def _predict(car_features: CarFeaturesPrediction) -> dict:
    """predict the price of the car"""
    logger.info("Predicting the price of the car")


    df = pd.DataFrame([vars(car_features)]) 
    df.drop(columns=['__pydantic_initialised__'], inplace=True)
    price = DesicionTreeModel.predict(df)
    
    print(price)
    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {"price": price[0]},
    }
    logger.info("Predicting the price of the car successful")
    return response




# if __name__ == "__main__":
#     file_name = __file__.split("/")[-1].split(".")[0].split("\\")[-1] # file name without extension

#     uvicorn.run(f"{file_name}:app", host='0.0.0.0', port=8000, reload=True) # why the reload not working ?
    # a: because you are not using the uvicorn command to run the app, you are using the python command to run the app, so the reload will not work
    #  
