FROM python:3.6-slim

WORKDIR  data_filtering
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000/tcp
EXPOSE 5000/udp

CMD ["python", "./inserting_data_final.py"]
