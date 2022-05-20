from pymssql import connect
import pyodbc 
import pandas as pd
import xlsxwriter

server = '10.203.180.32\AZDB'
user = 'sqlreport'
password = 'sqlreport2021'
database = 'gate'

Login = 'aqammadzadae'
PasswordMD5 = 'c2caea1c32db0492a967feb3743fb168'

DealerID = '5' # 16
CreateTimeFrom = '2021-05-01'
CreateTimeTo = '2021-05-01'
RetryDateFrom = '2021-05-01'
RetryDateTo = '2021-05-01'
RevokeStatus = '4' # 5
RevokeTimeFrom = '2021-05-01'
RevokeTimeTo = '2021-06-01'
Status='3'

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=10.203.180.32\AZDB;'
                      'Database=Main;'
                      'UID=sqlreport;'
                      'PWD=sqlreport2021;')

cursor = conn.cursor()
sql = """\
EXEC [dbo].[GetNewPayment] @Login=?, @PasswordMD5=?, @DealerID=?,  @RevokeTimeFrom=?, @RevokeTimeTo=?, @Status=?
"""
params = ('aqammadzadae', 'c2caea1c32db0492a967feb3743fb168', '5', '2021-05-01','2021-05-05', '3')
cursor.execute(sql, params)
pd.set_option('max_columns', None)

data = cursor.fetchall()
cursor.close()
df = pd.read_sql(sql=sql, con=conn, params=params)
print(df)

# df = data.copy()
# # date_columns = df.select_dtypes(include=['datetime64[ns, UTC]']).columns
# # for date_column in date_columns:
# #     df[date_column] = df[date_column].dt.date
writer = pd.ExcelWriter('output4.xlsx')
df.to_excel(writer, index=False)
writer.save()
print('DataFrame is written successfully to Excel File from Ms Server UPG.')





