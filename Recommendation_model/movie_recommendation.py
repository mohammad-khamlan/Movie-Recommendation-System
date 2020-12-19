from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import sklearn
from pyspark.ml.recommendation import ALSModel
from pyspark.sql import SparkSession
import itertools

app = Flask(__name__)

spark = SparkSession.builder.appName('Recommendation_system').getOrCreate()
test_data = pd.read_csv("recommendation_test_data.csv")

def predict_movies(als_model, test_data, user_id):
    """
    predict movies id's for given user
    :Args:
    als_model (ALS model): model to predict movies
    test_data (pandas dataframe): datarame contains test data 
    user_id (int): id for given user to predict movies
    :return: list of recommended movies id's
    """
    #test_data = test_data[test_data["userId"] == uid]

    # convert pandas dataframe to pyspark dataframe
    test_data = spark.createDataFrame(test_data) 
    # predict movies fo all users using als model
    prediction = als_model.transform(test_data)
    # convert pyspark dataframe to pandas dataframe
    prediction = prediction.select("*").toPandas()
    # sort values in dataframe by prediction
    prediction = prediction.sort_values(by='prediction', ascending=False)
    # select highest predict rating and return it's movie id
    prediction = prediction[prediction["userId"] == user_id]["movieId"].head()
    return prediction



if __name__ == '__main__':
    # load ALS model to use
    als_model = ALSModel.load('als_model2')
    # predict movies for given user
    recommended_movies = predict_movies(als_model, test_data, 318)
    app.run(debug=True)

