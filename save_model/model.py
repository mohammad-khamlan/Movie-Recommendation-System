from flask import Flask, request, jsonify
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
import numpy as np
import pandas as pd
import sklearn
import itertools


app = Flask(__name__)

data = pd.read_csv("movie_recommendation.csv")
spark = SparkSession.builder.appName('Recommendation_system').getOrCreate()

def ratings_to_0(user): 
    """
    function that take 20% of movies from a sample of users and make the ratings of these movies 0
    :args:
        list of users :test data set
    :returns: list of movies ids 
    """
    test_movies = []
    #store the users data in a dataframe 
    user_data = data[["userId","movieId","rating"]]
    user_data = user_data[user_data["userId"] == user]
    #take movies from different ratings and append it to test_movies list
    rate5 = user_data[user_data["rating"] == 5]
    test_movies.append(rate5["movieId"].head(15))

    rate4 = user_data[(user_data["rating"] == 4) | (user_data["rating"] == 4.5)]
    test_movies.append(rate4["movieId"].head(15))

    rate3 = user_data[(user_data["rating"] == 3) | (user_data["rating"] == 3.5)]
    test_movies.append(rate3["movieId"].head(15))

    rate2 = user_data[(user_data["rating"] == 2) | (user_data["rating"] == 2.5)]
    test_movies.append(rate2["movieId"].head(15))

    rate1 = user_data[(user_data["rating"] == 1) | (user_data["rating"] == 1.5)]
    test_movies.append(rate1["movieId"].head(15))
    #prepaire the final list from list of lists into one list
    test_movies = list(itertools.chain.from_iterable(test_movies))
    return test_movies


def normalize_data(df_rating):
    """
    reads the dataset from the same directory contains this file, clean and normalized it
    :Args:
    user_test_data (list): list contains random user as test data
    :return: dataframe ready to use in ML algorithm to train a model
    """
    #storing the users ids and movie ids and teh movies ratings into dataframe
    users_data = df_rating[["userId", "movieId", "rating"]]
    #grouping data by the userid and sum ratings for each users and store it into dataframe
    users_group1 = users_data.groupby(['userId'],as_index = False, sort=False)["rating"].sum()
    #merge the dataframe that has the sum with the uses_data dataframe
    users_data = pd.merge(users_data, users_group1, on = "userId", how = "left", sort = False)
    #grouping data by user id and count the ratings 
    users_group2 = users_data.groupby(['userId'],as_index = False, sort=False)["rating_x"].count()
    #merging the users_data with the grouupby dataframe
    users_data = pd.merge(users_data, users_group2, on = "userId", how = "left", sort = False)
    #normalize the each rate and store it in a new column
    users_data["normalize_rating"] = (users_data["rating_x_x"] - users_data["rating_y"]) / users_data["rating_x_y"]
    #rename some columns in the data
    data_normalize = users_data.rename(columns = {"rating_x_x":"rating", "rating_y":"sum", "rating_x_y":"count"})
    #drop some unuseful columns
    data_normalize = data_normalize.drop(columns = ["rating", "sum", "count"])
    return data_normalize 



def read_data(test_data):
    """
    reads the dataset from the same directory contains this file, clean and normalized it
    :Args:
        test_data (list): list contains random user as test data
    :return: dataframe ready to use in ML algorithm to train a model
    """

    # Reading data and store it in pyspark dataframe
    df = spark.read.csv("movie_recommendation.csv" , inferSchema = True , header = True)

    # Select features needs to train a model
    df_rating = df.select(df['userId'],df['movieId'],df['rating'])
    
    # conver pyspark dataframe to pandas dataframe to normalize rating
    df_rating = df_rating.select("*").toPandas()

    # normalizing data by normalize_data function
    df_rating = normalize_data(df_rating)
    df_rating = df_rating.rename(columns = {"normalize_rating":"rating"})
    
    # calling split_data function to split data as test data
    df_rating = split_data(df_rating, test_data)
    df_rating = spark.createDataFrame(df_rating) 

    return df_rating



def split_data(df_rating, test_data):
    """
    splitting data to train and test dataset
    :Args:
        df_rating (pandas dataframe): dataframe contains all users data
        test_data (list): list contains random user as test data
    :return: training dataframe without test data, it contains zero ratings for user in test data
    """
    # make rating of movies for user in test data zero
    for userid in test_data:
        test_movies = ratings_to_0(userid)
        for user in range(len(df_rating["userId"])):
            if(df_rating["userId"][user] == userid):
                if(df_rating["movieId"][user] in test_movies):
                    df_rating["rating"][user] = 0
    return df_rating
    


def train_model(df_rating):
    """
    train a model on training dataset
    :Args:
        df_rating (pandas dataframe): dataframe contains training dataset
    :return: model trained by training dataset
    """
    # convert pandas dataframe to pyspark dataframe
    #df_rating = spark.createDataFrame(df_rating) 

    # Train ALS model on the dataset with user column (userId), item column (movieId) and rating column (rating)
    als_model = ALS(maxIter=10, regParam=0.5, userCol = "userId", itemCol = "movieId",ratingCol = "rating", coldStartStrategy = "drop")
    model = als_model.fit(df_rating)
    
    # return the model
    return model
    

def save_model(model):
    """
    save model as a file to use it later
    :Args:
        model (ALS model): model already trained
    :return: none
    """
    # save model as a file
    model.save("als_model2")


def save_test_file(data):
    """
    save test data as a CSV file to use it later
    :Args:
        data (DataFrame): dataframe contains test data
    :return: none
    """
    testdata = data[data["rating"] == 0]
    testdata = testdata.select("*").toPandas()
    testdata.to_csv(r'recommendation_test_data.csv', index = False)



if __name__ == '__main__':
    #random user ids used as test data set 
    test_data = [414, 599, 474, 448, 274, 610, 68, 380, 606, 249, 288, 387, 182, 177, 318]
    data = read_data(test_data)
    model = train_model(data)
    save_test_file(data)
    save_model(model)
    app.run(debug=True)


