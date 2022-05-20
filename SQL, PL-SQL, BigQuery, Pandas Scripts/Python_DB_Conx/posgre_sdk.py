import psycopg2 as pg
import pandas as pd
from sqlalchemy import create_engine

engine = pg.connect("dbname='sdk' user='prodpostuser' host='mpay-prod.cbceq9vmt4fo.eu-central-1.rds.amazonaws.com' port='5432' password='eanhpk9bGbZ9vdFS55kKpT'")
df = pd.read_sql('select * from sdk.public.tx_business_base limit 10', con=engine)
print(df)

date_columns = df.select_dtypes(include=['datetime64[ns, UTC]']).columns
for date_column in date_columns:
    df[date_column] = df[date_column].dt.date
# import xlsxwriter
writer = pd.ExcelWriter('output.xlsx')
df.to_excel(writer)
writer.save()
print('DataFrame is written successfully to Excel File from PostGRESql SDK.')

# Create an engine instance
