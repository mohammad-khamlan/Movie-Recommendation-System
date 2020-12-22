from flask import Flask , render_template , request
import csv
import pandas as pd
from pyspark.ml.recommendation import ALSModel
from pyspark.sql import SparkSession
import itertools 
import json 
import requests

app = Flask(__name__)


@app.route('/')
#function to route to html file *2
def index(): 
    return render_template('main.html') 


@app.route('/predict' , methods=['GET' ,'POST'])
def Recommend_Movies(): 
    if request.method == "POST" :
        userId = request.form.get('user')  
        predict_movies_ids = [1] #predict(userId)
        predict_movies_ids = json.dumps(predict_movies_ids)
        movies_titles = requests.post(url = "https://data-filtering.herokuapp.com/titles", data = predict_movies_ids)
        movies_titles = json.loads(movies_titles.text)
        print(movies_titles)
        return render_template('main.html')
      
    elif request.method == "GET" :
        userId = request.arg.get('user')  
        predict_movies_ids = [1]#predict(userId)
        predict_movies_ids = json.dumps(predict_movies_ids)
        movies_titles = requests.post( url = "https://data-filtering.herokuapp.com/titles", data = predict_movies_ids)
        #print(movies_titles)
        #redirect(url_for('main', movies_titles = movies_titles))
        return 'done'

if __name__ == '__main__':
    app.run(debug=True)
