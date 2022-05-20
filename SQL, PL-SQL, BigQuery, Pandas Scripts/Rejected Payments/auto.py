import pyodbc 
import pandas as pd

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=MODDEVUPG;'
                      'Database=gate211;'
                      'Trusted_Connection=yes;')

# cursor = conn.cursor()
# cursor.execute('SELECT TOP 10 * FROM gate211.dbo.Payment').fetchall()

sql_query = pd.read_sql_query("""
        SELECT   [PaymentID]	,[AgentPaymentID]
		,[Status]		,[Number]
		,[PaySum]		,[ProviderSum]			,[AgentTerminalID]     
	  ,s.[ServiceID],  p.[GateServiceID]  	  ,s.[ProviderID]
		,[PayDate]		,[StatusDate]			,[ReceiveDate]       
		,[IsTest]		,[OsmpProviderID]		,[ProviderPaymentIDString]
		,CAST(ExtraParams.query('data(r/card_number)') as nvarchar(max)) 'Card'
		,CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) AgentID
		,CAST(ExtraParams.query('data(r/trm_prv_id)') as nvarchar)+RIGHT('0000000000'+CAST(AgentTerminalID as nvarchar),10) TRN_ID
	FROM [gate211].[dbo].[Payment] p
	left join gate211.dbo.Service s 
	on	s.ServiceID=p.ServiceID
	where AgentID=1 
--and status=3 
--and [OsmpProviderID] = 17498
--and PayDate between '2021-03-29' and '2021-03-30'
--and [PaymentID] = '5917153181'
and [AgentPaymentID] in (526348471)
--and s.[ServiceID] in (549, 550, 600)
--and ProviderID = 120
and p.[StatusDate] between '2021-04-06' and '2021-06-06'
--and Number = 7003560830
--and p.[PaySum] = 67
--order by AgentPaymentID""",conn)
print(sql_query)
df = sql_query.copy()
date_columns = df.select_dtypes(include=['datetime64[ns, UTC]']).columns
for date_column in date_columns:
    df[date_column] = df[date_column].dt.date
# import xlsxwriter
writer = pd.ExcelWriter('output.xlsx')
df.to_excel(writer)
writer.save()
print('DataFrame is written successfully to Excel File from Ms Server UPG.')
# print(type(sql_query))

# for row in cursor:
#     print(row)
# print("Hello world")
