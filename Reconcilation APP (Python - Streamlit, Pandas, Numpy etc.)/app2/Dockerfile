FROM python:3.8

WORKDIR /app2

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY app2.py ./app2.py
COPY eManat.png ./eManat.png
COPY emanatpng.png ./emanatpng.png
COPY .streamlit/config.toml /app2/.streamlit/config.toml

COPY .streamlit/secrets.toml /app2/.streamlit/secrets.toml



