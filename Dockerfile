FROM python:3.8

ADD ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD ./app.py /app/app.py

WORKDIR /app
CMD ["uvicorn", "--host", "0.0.0.0", "app:app"]
