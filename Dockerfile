FROM python:3.9.5
WORKDIR /docker-flask-test
ADD . /docker-flask-test
RUN pip install -r requirements.txt
CMD ["python","app.py"]