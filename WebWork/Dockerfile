FROM python:3.9

WORKDIR  Final Project/WebWork

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000/tcp
EXPOSE 5000/udp

CMD ["python3", "backEnd.py"]
