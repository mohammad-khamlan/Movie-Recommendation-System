FROM python:3.6-slim
WORKDIR Final Project/Recommendation_model
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4999/tcp
EXPOSE 4999/udp

CMD ["python3", "movie_recommendation.py"]
