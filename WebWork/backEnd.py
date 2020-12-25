from flask import Flask , render_template , request
import csv
import pandas as pd
import itertools 
import json
import requests
from flask import jsonify

app = Flask(__name__)


@app.route('/')
#function to route to html file *2
def index(): 
    return render_template('main.html') 


@app.route('/predict' , methods=['GET' ,'POST'])
def Recommend_Movies(): 
    if request.method == "POST" :
        userId = request.form.get('user')
        predict_movies_ids = [1]#predict(userId)  
        predict_movies_ids = json.dumps(predict_movies_ids)
        movies_titles = requests.post("https://data-filtering.herokuapp.com/titles", data = predict_movies_ids)
        print(type(movies_titles))

        if 'json' in movies_titles.headers.get('Content-Type'):
            js = movies_titles.json()
        else:
            print('Response content is not in JSON format.')
            js = 'spam'
        print(type(js))
        #for item in js.itertools:
            #print(item)
        print(js["movies_titles"])

        return 'done'
    
   
    elif request.method == "GET" :

        userId = request.arg.get('user')  
        predict_movies_ids = [414]#predict(userId)
        predict_movies_ids = json.dumps(predict_movies_ids)
        movies_titles = requests.post( url = "https://data-filtering.herokuapp.com/titles", data = predict_movies_ids)
        
        if 'json' in movies_titles.headers.get('Content-Type'):
            js = movies_titles.json()
        else:
            print('Response content is not in JSON format.')
            js = 'spam'
        print(type(js))
        #for item in js.itertools:
            #print(item)
        print(js["movies_titles"])

        return 'done'
   
   
if __name__ == '__main__':

    app.run(debug=True)
