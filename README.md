# Movie Recommendation System
It's a web page working using **Machine Learning** algorithms and **Bigdata** principles to predict movies for a given user, by just entering user id
and return a recommended movies for user to watch. We used **ALS** model based to build a model and train it. And we build another **movie based** approach for model.

## Service Link
[MOVAI](https://data-filtering.herokuapp.com)

## How Does System Work
Customer should enter user id for user who want to predict for it, then the  

## ALS Model Based
**Alternating Least Square(ALS)** is a matrix factorization algorithm and it runs itself in parallel fashion. We used ALS from pyspark library and train a model 
to predict a movies for given user id in the website.

## Movie Based 
At the first we normalized the data ,then we used user-user based to create a matrix contain users and the simelarity between them. After that we send the userid to function return the top 10 similar users to the user which we are predicting to him.

Then we create another matrix between users-movies(rows-columns) , this matris wil contain the normalized rating for each movie by each user and we filled the zeros by the mean for columns. At the fainal we bring all movies with it's rating for the user which we are predicting to him and removed the watched movies to let the difference between all the movies and the movies that have been watched be the final result .


