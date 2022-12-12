# Car-Price-Prediction

## Table of Contents

1. [Installation](#installation)
2. [Project Motivation](#motivation)
3. [Data](#data)
3. [File Descriptions](#files)

## Installation <a name="installation"></a>

The code should run with no issues using Python versions 3.*. The following libraries are used:

* pandas
* numpy
* matplotlib
* seaborn
* sklearn
* pickle
* flask
* json
* plotly
* joblib
you can install all the required libraries using the following command:

```bash
python setup.py install
```

or

```bash
pip install -r requirements.txt
```

to run the fastapi server, you need to run the following command:

```bash
uvicorn api:app --reload
```

## Data<a name="data"></a>
the data is collected from <a href="https://shobiddak.com/cars">shobiddak</a> and it contains 5,000 car sales the data is collected from 2018-2020 to use the Parsed data you can find it here <a href="https://github.com/mohamadhase/Car-Price-Prediction/blob/main/data.csv">data.csv</a>
## Project Motivation<a name="motivation"></a>

For this project, I was interestested in using Car Sales Data to better understand:

1. What are the most important features that affect the price of a car?
2. How can we predict the price of a car?

## File Descriptions <a name="files"></a>

theres 5 steps in this project each steps is seperated in its file:

1. filtering data files : this step is to filter the data files that are not in the right format, the code is in <a href="https://github.com/mohamadhase/Car-Price-Prediction/blob/main/parser/handle_wrong_files.py">handle_wrong_files.py</a>

2. data Parsing : this step is to parse the data files and convert them to csv files, the code is in <a href="https://github.com/mohamadhase/Car-Price-Prediction/blob/main/parser/main.py">Parser.py</a>

3. Model Generation : this step is to generate the model with all the neccessary steps  and save it in a pickle file, the code is in <a href="https://github.com/mohamadhase/Car-Price-Prediction/blob/main/notebooks/car_prediction_v2.ipynb">car_prediction.ipynb</a>

4. Model Deployment : this step is to deploy the model using fastapi, the code is in <a href="https://github.com/mohamadhase/Car-Price-Prediction/blob/main/api.py">api.py</a>

5. Model Testing : to test the model you can use this <a href="https://github.com/mohamadhase/Car-Price-Prediction/blob/main/ML.postman_collection.json">postman collection</a> to test the model

