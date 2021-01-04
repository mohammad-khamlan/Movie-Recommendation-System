FROM robertlgtucker/pyspark-java8

WORKDIR /app
ADD . /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000/tcp
EXPOSE 5000/udp

CMD ["python3", "movie_recommendation.py"]
