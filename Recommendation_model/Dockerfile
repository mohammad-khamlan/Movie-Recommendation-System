FROM python:3.6-slim

WORKDIR Final_project/Recommendation_model
COPY . .

RUN apt-get update -qq
RUN apt-get install -y openjdk-8-jdk
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000/tcp
EXPOSE 5000/udp

CMD ["python3", "movie_recommendation.py"]
