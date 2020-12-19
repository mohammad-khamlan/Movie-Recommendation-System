from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import pymongo
import pandas as pd
import json


app = Flask(__name__)

# read csv file wich contain data 
data = pd.read_csv("data.csv")

def connect_to_mongo():
  """
    connect to our db which in mongodb atlas and get the db and the collection
    :param: none
    :return: none
  """
  # connect to mongodb atlas
  client = pymongo.MongoClient("mongodb://movie_recommendation:abdallah123456789@cluster0-shard-00-00.nbikg.mongodb.net:27017,cluster0-shard-00-01.nbikg.mongodb.net:27017,cluster0-shard-00-02.nbikg.mongodb.net:27017/movie_recommendation?ssl=true&replicaSet=atlas-v650m9-shard-0&authSource=admin&retryWrites=true&w=majority")
  db = client.movie_recommendation   # reaching the main  DB                                 
  collection = db.MoviesData  # reaching the collection
  return collection


def getTitle(list_moviesId, collection):
  """
  retrieve movies titles 
  :Args:
  list_moviesId (list): list contains movies id's for user
  collection (pymongo collection): collection to use data from mongoDB
  :return: movies titles
  """
  # creating list for titles for each Id
  movies_titles = []  
  temp_list = [] # temproray list
    
  for Id in range(len(list_moviesId)):
      query = collection.find_one({'movieId':list_moviesId[Id]})
      if query!=None:          
        temp_list.append(collection.find_one({'movieId':list_moviesId[Id]},{'title':1,'_id':0})) 
        movies_titles.append(temp_list[Id].get('title'))  
      else:
        print('The movieID <' , list_moviesId[Id] , '> wasn\'t found')
  return movies_titles
    


if __name__ == '__main__':
  # connec to mongoDB database and collection
  collection = connect_to_mongo()
  # retrieve movies titles for given movies id's
  movies_titles = getTitle(movies_ids, collection)
  app.run(debug=True)


