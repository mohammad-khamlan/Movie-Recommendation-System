FROM python:3.6-slim

WORKDIR /app
COPY . ./app

# Install OpenJDK 8
RUN \
apt-get update && \
apt-get install -y openjdk-8-jdk && \
rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r ./app/Recommendation_model/requirements.txt

EXPOSE 5000/tcp
EXPOSE 5000/udp

CMD ["python3", "./app/Recommendation_model/movie_recommendation.py"]
