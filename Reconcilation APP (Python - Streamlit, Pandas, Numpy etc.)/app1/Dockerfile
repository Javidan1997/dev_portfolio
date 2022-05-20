FROM python:3.8

WORKDIR /app1

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt


COPY app1.py ./app1.py
COPY eManat.png ./eManat.png
COPY emanatpng.png ./emanatpng.png
COPY .streamlit/config.toml /app1/.streamlit/config.toml

COPY .streamlit/secrets.toml /app1/.streamlit/secrets.toml



