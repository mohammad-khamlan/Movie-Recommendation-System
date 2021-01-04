from flask import Flask, request , jsonify
from pymongo import MongoClient
import pymongo
import pandas as pd
import json
import argparse 
import os


app = Flask(__name__)
collection = 0

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


def get_title(list_moviesId):
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
    

@app.route('/titles' , methods=['GET' ,'POST'])
def take_parameters():
  if request.method == "POST" :
    movies_ids = request.get_json()['ids']
    movies_titles = get_title(movies_ids)
    movies_titles = json.dumps(movies_titles) 
    return movies_titles

  elif request.method == "GET" :
    movies_ids = list(map(int,request.args.getlist('ids')))
    movies_titles = get_title(movies_ids)
    movies_titles = json.dumps(movies_titles)
    movies_titles = {"movies_titles": movies_titles}
    return jsonify(movies_titles)


if __name__ == '__main__':
  # connec to mongoDB database and collection
  collection = connect_to_mongo()
  port = int(os.environ.get('PORT', 5000))
  app.run(host = '0.0.0.0', debug=True, port = port)


