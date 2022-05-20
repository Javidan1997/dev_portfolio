import datetime as dt
from airflow import DAG
import requests
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
import pandas as pd
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
import json


# Default Args

key = 'b26d15597951e131f9d1b50a9dc05f25'

default_args = {
    "owner": "javidan_abdullayev",
    "start_date": dt.datetime(2022, 4, 30, 0, 00, 00),
    "concurrency": 1,
    "retries": 0,
}
GOOGLE_CONN_ID = 'google_cloud_default'
BUCKET_NAME = 'weather-dag'
GS_PATH = '/home/airflow/gcs/data/'
PROJECT_ID = 'holy-water-348217'
STAGING_DATASET = 'WeatherDag'
PATH_TO_UPLOAD_FILE = "/home/javidanja/airflow/gcs/data/weather.csv"
DESTINATION_FILE_LOCATION = f"data/weather{dt.datetime.today().strftime('%Y-%m-%d %H:%M')}.csv"
PATH_TO_UPLOAD_FILE_2 = "/home/javidanja/airflow/gcs/data/weather_top.csv"
DESTINATION_FILE_LOCATION_2 = f"data/weather_top{dt.datetime.today().strftime('%Y-%m-%d %H:%M')}.csv"

# Func for getting API response


def get_weather_api(lat, lon, city):

    key = 'b26d15597951e131f9d1b50a9dc05f25'
    URL = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}"
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        df = pd.json_normalize(data['main'])
        df['city'] = city
        df = df[['city', 'temp', 'feels_like',
                'temp_min', 'temp_max', 'pressure', 'humidity']]
        return df

# Func for joining api results


def process_weather():
    city = ['Tokyo',
            'Jakarta',
            'Delhi',
            'Manila',
            'São Paulo',
            'Seoul',
            'Mumbai',
            'Shanghai',
            'Mexico City',
            'Guangzhou',
            'Cairo',
            'Beijing',
            'New York',
            'Kolkāta',
            'Moscow',
            'Bangkok',
            'Dhaka',
            'Buenos Aires',
            'Ōsaka',
            'Lagos',
            'Istanbul',
            'Karachi',
            'Kinshasa',
            'Shenzhen',
            'Bangalore',
            'Ho Chi Minh City',
            'Tehran',
            'Los Angeles',
            'Rio de Janeiro',
            'Chengdu',
            'Baoding',
            'Chennai',
            'Lahore',
            'London',
            'Paris',
            'Tianjin',
            'Linyi',
            'Shijiazhuang',
            'Zhengzhou',
            'Nanyang',
            'Hyderābād',
            'Wuhan',
            'Handan',
            'Nagoya',
            'Weifang',
            'Lima',
            'Zhoukou',
            'Luanda',
            'Ganzhou']
    lat = ['35.6839',
           '-6.2146',
           '28.6667',
           '14.6',
           '-23.5504',
           '37.56',
           '19.0758',
           '31.1667',
           '19.4333',
           '23.1288',
           '30.0444',
           '39.904',
           '40.6943',
           '22.5727',
           '55.7558',
           '13.75',
           '23.7289',
           '-34.5997',
           '34.752',
           '6.45',
           '41.01',
           '24.86',
           '-4.3317',
           '22.535',
           '12.9791',
           '10.8167',
           '35.7',
           '34.1139',
           '-22.9083',
           '30.66',
           '38.8671',
           '13.0825',
           '31.5497',
           '51.5072',
           '48.8566',
           '39.1467',
           '35.0606',
           '38.0422',
           '34.7492',
           '32.9987',
           '17.3617',
           '30.5872',
           '36.6116',
           '35.1167',
           '36.7167',
           '-12.06',
           '33.625',
           '-8.8383',
           '25.8292'
           ]
    lon = ['139.7744',
           '106.8451',
           '77.2167',
           '120.9833',
           '-46.6339',
           '126.99',
           '72.8775',
           '121.4667',
           '-99.1333',
           '113.259',
           '31.2358',
           '116.4075',
           '-73.9249',
           '88.3639',
           '37.6178',
           '100.5167',
           '90.3944',
           '-58.3819',
           '135.4582',
           '3.4',
           '28.9603',
           '67.01',
           '15.3139',
           '114.054',
           '77.5913',
           '106.6333',
           '51.4167',
           '-118.4068',
           '-43.1964',
           '104.0633',
           '115.4845',
           '80.275',
           '74.3436',
           '-0.1275',
           '2.3522',
           '117.2056',
           '118.3425',
           '114.5086',
           '113.6605',
           '112.5292',
           '78.4747',
           '114.2881',
           '114.4894',
           '136.9333',
           '119.1',
           '-77.0375',
           '114.6418',
           '13.2344',
           '114.9336']

    newDf = pd.DataFrame(columns=['city', 'temp', 'feels_like',
                                  'temp_min', 'temp_max', 'pressure', 'humidity'])
    for i in range(0, 49):

        weather = get_weather_api(lat[i], lon[i], city[i])
        newDf = newDf.append(weather, ignore_index=True)
    newDf.to_json(
        f"/home/javidanja/airflow/gcs/data/weather.json")
    # ti.xcom_push(key='weather', value=out)

# Func for converting JSON to CSV and save to local storage


def save_posts():
    post = open(
        f"/home/javidanja/airflow/gcs/data/weather.json")
    data = json.load(post)
    city = pd.json_normalize(data["city"])
    temp = pd.json_normalize(data["temp"])
    feels_like = pd.json_normalize(data["feels_like"])
    temp_min = pd.json_normalize(data["temp_min"])
    temp_max = pd.json_normalize(data["temp_max"])
    pressure = pd.json_normalize(data["pressure"])
    humidity = pd.json_normalize(data["humidity"])
    df = pd.DataFrame(columns=['city', 'temp', 'feels_like',
                               'temp_min', 'temp_max', 'pressure', 'humidity'])
    for i in range(0, 49):

        df = df.append(pd.DataFrame({'city': city.iloc[0][i], 'temp': temp.iloc[0][i], 'feels_like': feels_like.iloc[0][i], 'temp_min': temp_min.iloc[0]
                                     [i], 'temp_max': temp_max.iloc[0][i], 'pressure': pressure.iloc[0][i], 'humidity': humidity.iloc[0][i], }, index=[i]), ignore_index=True)
    df['temp'] = df['temp'] - 273.15
    df['feels_like'] = df['feels_like'] - 273.15
    df['temp_min'] = df['temp_min'] - 273.15
    df['temp_max'] = df['temp_max'] - 273.15
    df.to_csv(
        f"/home/javidanja/airflow/gcs/data/weather.csv", index=False)

# Func for getting hottest 10 cities


def get_top_values():
    post = open(
        f"/home/javidanja/airflow/gcs/data/weather.json")
    data = json.load(post)
    city = pd.json_normalize(data["city"])
    temp = pd.json_normalize(data["temp"])
    feels_like = pd.json_normalize(data["feels_like"])
    temp_min = pd.json_normalize(data["temp_min"])
    temp_max = pd.json_normalize(data["temp_max"])
    pressure = pd.json_normalize(data["pressure"])
    humidity = pd.json_normalize(data["humidity"])
    df = pd.DataFrame(columns=['city', 'temp', 'feels_like',
                               'temp_min', 'temp_max', 'pressure', 'humidity'])
    for i in range(0, 49):

        df = df.append(pd.DataFrame({'city': city.iloc[0][i], 'temp': temp.iloc[0][i], 'feels_like': feels_like.iloc[0][i], 'temp_min': temp_min.iloc[0]
                                     [i], 'temp_max': temp_max.iloc[0][i], 'pressure': pressure.iloc[0][i], 'humidity': humidity.iloc[0][i], }, index=[i]), ignore_index=True)
    df['temp'] = df['temp'] - 273.15
    df['feels_like'] = df['feels_like'] - 273.15
    df['temp_min'] = df['temp_min'] - 273.15
    df['temp_max'] = df['temp_max'] - 273.15
    df_sort = df.nlargest(10, 'temp')
    df_sort.to_csv(
        f"/home/javidanja/airflow/gcs/data/weather_top.csv", index=False)


with DAG(
    "weather_dag",
    catchup=False,
    default_args=default_args,
    schedule_interval="@daily",
) as dag:
    start_pipeline = DummyOperator(
        task_id='start_pipeline',
        dag=dag
    )
    get_data = PythonOperator(
        task_id='get_data',
        python_callable=process_weather,
        dag=dag
    )

    save_to_local = PythonOperator(
        task_id='save_to_local',
        python_callable=save_posts,
        dag=dag
    )
    get_top_value = PythonOperator(
        task_id='get_top_value',
        python_callable=get_top_values,
        dag=dag
    )

    upload_file = LocalFilesystemToGCSOperator(
        task_id="upload_file",
        src=PATH_TO_UPLOAD_FILE,
        dst=DESTINATION_FILE_LOCATION,
        bucket=BUCKET_NAME,
    )
    upload_top_value = LocalFilesystemToGCSOperator(
        task_id="upload_top_value",
        src=PATH_TO_UPLOAD_FILE_2,
        dst=DESTINATION_FILE_LOCATION_2,
        bucket=BUCKET_NAME,
    )

    load_dataset = GCSToBigQueryOperator(
        task_id='load_dataset',
        bucket=BUCKET_NAME,
        source_objects=[
            f"data/weather{dt.datetime.today().strftime('%Y-%m-%d %H:%M')}.csv"],
        destination_project_dataset_table=f"{PROJECT_ID}:{STAGING_DATASET}.weather_{dt.datetime.today().strftime('%Y-%m-%d-%H-%M')}",
        write_disposition='WRITE_TRUNCATE',
        source_format='csv',
        allow_quoted_newlines='true',
        skip_leading_rows=1,
        schema_fields=[
            {'name': 'city', 'type': 'STRING', 'mode': 'REQUIRED'},
            {'name': 'temp', 'type': 'STRING', 'mode': 'REQUIRED'},
            {'name': 'feels_like', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'temp_min', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'temp_max', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'pressure', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'humidity', 'type': 'STRING', 'mode': 'NULLABLE'}
        ],
        dag=dag

    )
    load_dataset_top_value = GCSToBigQueryOperator(
        task_id='load_dataset_top_value',
        bucket=BUCKET_NAME,
        source_objects=[
            f"data/weather_top{dt.datetime.today().strftime('%Y-%m-%d %H:%M')}.csv"],
        destination_project_dataset_table=f"{PROJECT_ID}:{STAGING_DATASET}.weather_hot_{dt.datetime.today().strftime('%Y-%m-%d-%H-%M')}",
        write_disposition='WRITE_TRUNCATE',
        source_format='csv',
        allow_quoted_newlines='true',
        skip_leading_rows=1,
        schema_fields=[
            {'name': 'city', 'type': 'STRING', 'mode': 'REQUIRED'},
            {'name': 'temp', 'type': 'STRING', 'mode': 'REQUIRED'},
            {'name': 'feels_like', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'temp_min', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'temp_max', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'pressure', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'humidity', 'type': 'STRING', 'mode': 'NULLABLE'}
        ],
        dag=dag

    )

start_pipeline >> get_data >> save_to_local >> get_top_value >> upload_file >> upload_top_value >> load_dataset >> load_dataset_top_value
