FROM python:3.6-slim-alpine

RUN apk update \
&& apk upgrade \
&& apk add --no-cache bash \
&& apk add --no-cache --virtual=build-dependencies unzip \
&& apk add --no-cache curl \
&& apk add --no-cache openjdk8-jre

WORKDIR /app
ADD . /app

RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev 

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV JAVA_HOME="/usr/lib/jvm/java-1.8-openjdk" 
EXPOSE 5000/tcp
EXPOSE 5000/udp

CMD ["python3", "movie_recommendation.py"]
