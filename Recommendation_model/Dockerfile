FROM alpine:3.7

RUN apk update \
&& apk upgrade \
&& apk add --no-cache bash \
&& apk add --no-cache --virtual=build-dependencies unzip \
&& apk add --no-cache curl \
&& apk add --no-cache openjdk8-jre

RUN apk add --no-cache python3 py3-pip3

WORKDIR /app
ADD . /app

RUN pip3 install --no-cache-dir -r requirements.txt

ENV JAVA_HOME="/usr/lib/jvm/java-1.8-openjdk" 
EXPOSE 5000/tcp
EXPOSE 5000/udp

CMD ["python3", "movie_recommendation.py"]
