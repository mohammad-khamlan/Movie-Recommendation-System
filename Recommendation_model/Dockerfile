FROM python:3
WORKDIR /Recommendation_model
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000/tcp
EXPOSE 5000/udp

CMD ["python3", "./movie_recommendation.py"]
