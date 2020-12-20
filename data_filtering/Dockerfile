FROM python:3

WORKDIR  data_filtering
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000/tcp
EXPOSE 5000/udp

CMD ["python", "./inserting_data_final.py"]
