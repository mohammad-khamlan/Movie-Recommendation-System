from flask import Flask , render_template , request
import csv
import pandas as pd
import itertools 
import json
import requests
from flask import jsonify
import os

app = Flask(__name__)


@app.route('/')
#function to route to html file *2
def index():
    print("started")
    return render_template('main.html') 


@app.route('/predict' , methods=['GET' ,'POST'])
def Recommend_Movies(): 
    if request.method == "POST" :
        userId = request.form.get('user')

        userId = int(userId)
        predict_movies_ids = requests.post(url = "http://127.0.0.1:6000/predict", json={'id': userId})

        predict_movies_ids = predict_movies_ids.json()["numbers"]
        movies_titles = requests.post(url = "https://data-filtering.herokuapp.com/titles", json={'ids': predict_movies_ids})
        movies_titles = movies_titles.json()["movies_titles"]
        return render_template('result.html', value = movies_titles) 
    
    
    elif request.method == "GET" :
        userId = request.arg.get('user')  

        userId = int(userId)
        predict_movies_ids = requests.post(url = "http://127.0.0.1:6000/predict", json={'id': userId})

        predict_movies_ids = predict_movies_ids.json()["numbers"]
        movies_titles = requests.post(url = "https://data-filtering.herokuapp.com/titles", json={'ids': predict_movies_ids})
        movies_titles = movies_titles.json()["movies_titles"]

        return 'done'
    
   

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 1234))
    app.run(debug=True, port = port)
