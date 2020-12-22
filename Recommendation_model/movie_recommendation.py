from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import sklearn
from pyspark.ml.recommendation import ALSModel
from pyspark.sql import SparkSession
import itertools
import json
import os

app = Flask(__name__)

spark = SparkSession.builder.appName('Recommendation_system').getOrCreate()

# load ALS model to use
als_model = ALSModel.load('als_model2')

def predict_movies(user_id):
    """
    predict movies id's for given user
    :Args:
    als_model (ALS model): model to predict movies
    test_data (pandas dataframe): datarame contains test data 
    user_id (int): id for given user to predict movies
    :return: list of recommended movies id's
    """
    #test_data = test_data[test_data["userId"] == uid]
    test_data = pd.read_csv("recommendation_test_data.csv")
    # convert pandas dataframe to pyspark dataframe
    test_data = spark.createDataFrame(test_data) 
    # predict movies fo all users using als model
    prediction = als_model.transform(test_data)
    # convert pyspark dataframe to pandas dataframe
    prediction = prediction.select("*").toPandas()
    # sort values in dataframe by prediction
    prediction = prediction.sort_values(by='prediction', ascending=False)
    # select highest predict rating and return it's movie id
    prediction = prediction[prediction["userId"] == user_id]["movieId"].head().tolist()
    return prediction

@app.route('/predict' , methods=['GET' ,'POST'])
def get_user_id():
    if request.method == "POST" :
        user_id = request.get_json()['id']
        prediction = predict_movies(user_id)
        prediction = json.dumps(prediction)
        return prediction

    elif request.method == "GET" :
        user_id = int(request.args.get('id'))
        prediction = predict_movies(user_id)
        prediction = json.dumps(prediction)
        return prediction

if __name__ == '__main__':
    app.run(debug=True)

