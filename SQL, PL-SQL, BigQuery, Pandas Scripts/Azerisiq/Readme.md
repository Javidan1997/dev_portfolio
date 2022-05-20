# Azerisiq 
Azerisiq has 2 types: 

*Ehali

*Qeyri Ehali

## Qeyri Ehali
Initially, we need to create 2 tables to compare which transactions are missing from the other or vice versa
First table is Modenis's table contaning payments the company "see"s
Second table is Azerisiq's table containing payments the Azerisiq "see"s



## Ehali
Initially, we need to create 2 tables to compare which transactions are missing from the other or vice versa
First table is Modenis's table contaning payments the company "see"s
Second table is Azerisiq's table containing payments the Azerisiq "see"s

First table is taken from the Gate DB Payment table with the following query. 
Second table is given us via email as excel files, containing files from 1-11, 11-18, 19-26, 27-31

Compare:
First table with Union of all excel files(from 1-31th day of the month)

First table query:
------------------------------------------------------------------------------------------------------------------------------------------
```
select * into yanvar2021.dbo.Azerisiqehali from (

SELECT 
CASE 
WHEN ServiceID in (719, 720) THEN ProviderPaymentIDString
ELSE AgentPaymentID END as trn_id, 
      [ProviderPaymentIDString]
      ,[PaymentID]
      ,[AgentPaymentID]
      ,[ServiceID]
      ,[GateServiceID]
      ,[PayDate]
      ,[StatusDate]
      ,[Number]
      ,[PaymentInfo]
      ,[AgentTerminalID]
      ,[PaySum]
      ,[Status]
      ,[GateErrorMessage]
      ,[ExtraParams]
   
,CAST(ExtraParams.query('data(r/isiq_counter)') as nvarchar) isiq_counter
,CAST(ExtraParams.query('data(r/isiq_subid)') as nvarchar) isiq_subid
,[OsmpProviderID]
--into Sentyabr2019.[dbo].AzerisiqEhaliM
FROM [gate211].[dbo].[Payment]
where (StatusDate between '2021-01-01' and '2021-02-01' ) and ServiceID in (276,  719)
   and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) <> '3'
union all

SELECT 

	  LEFT(CAST([ExtraParams].query('data(r/trm_prv_id)') as  nvarchar(max)),10)+RIGHT('0000000000'+cast(AgentTerminalID as varchar(10)),10)  trm_prv_id 
      ,[AgentPaymentID]
      ,[PaymentID]
      ,[AgentPaymentID]
      ,[ServiceID]
      ,[GateServiceID]
      ,[PayDate]
      ,[StatusDate]
      ,[Number]
      ,[PaymentInfo]
      ,[AgentTerminalID]
      ,[PaySum]
      ,[Status]
      ,[GateErrorMessage]
      ,[ExtraParams]
,CAST(ExtraParams.query('data(r/isiq_counter)') as nvarchar) isiq_counter
,CAST(ExtraParams.query('data(r/isiq_subid)') as nvarchar) isiq_subid
,[OsmpProviderID]
FROM [gate211].[dbo].[Payment]
where (StatusDate between '2021-01-01' and '2021-02-01' )and ServiceID in (  990,991,998,999)
and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) <> '3' and
len(CAST(ExtraParams.query('data(r/ai_subscriber_type)') as nvarchar))<7 ) a
```

qehali create ---------------------------
```
SELECT * INTO [8august2021_recon].dbo.AzerisiqQehali FROM (SELECT CASE WHEN 
	ServiceID in (719, 720) 
	THEN ProviderPaymentIDString
	ELSE AgentPaymentID END as trn_id 
    ,[ProviderPaymentIDString]
    ,[AgentPaymentID]
	,[ProviderSum]
    ,[Status] 
FROM [gate211].[dbo].[Payment]
where 
	(StatusDate between '2021-08-01' and '2021-09-01' ) 
	and ServiceID in ( 277,  720)
    and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) <> '3'
union all
SELECT LEFT(CAST([ExtraParams].query('data(r/trm_prv_id)') as  nvarchar(max)),10)+RIGHT('0000000000'+cast(AgentTerminalID as varchar(10)),10)  trm_prv_id 
      ,[AgentPaymentID]
      ,[AgentPaymentID]
	  ,[ProviderSum]
      ,[Status]
FROM [gate211].[dbo].[Payment]
where (StatusDate between '2021-08-01' and '2021-09-01' )
	and ServiceID in (  990,991,998,999)
	and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) <> '3' 
	and len(CAST(ExtraParams.query('data(r/ai_subscriber_type)') as nvarchar))>7
	) AS AzerishiqQehali

```
qehali create ---------------------------

```
select * into dbo.AzerisiqQehali from (SELECT 
CASE 
WHEN ServiceID in (719, 720) THEN ProviderPaymentIDString
ELSE AgentPaymentID END as trn_id, 
      [ProviderPaymentIDString]
      ,[PaymentID]
      ,[AgentPaymentID]
      ,[ServiceID]
      ,[GateServiceID]
      ,[PayDate]
      ,[StatusDate]
      ,[Number]
      ,[PaymentInfo]
      ,[AgentTerminalID]
      ,[PaySum]
      ,[ProviderSum]
      ,[Status]
      ,[GateErrorMessage]
      ,[ExtraParams]
   
,CAST(ExtraParams.query('data(r/isiq_counter)') as nvarchar) isiq_counter
,CAST(ExtraParams.query('data(r/isiq_subid)') as nvarchar) isiq_subid
,[OsmpProviderID]
--into Sentyabr2019.[dbo].AzerisiqEhaliM
FROM [gate211].[dbo].[Payment]
where (StatusDate between '2021-03-01' and '2021-04-01' ) and ServiceID in ( 277,  720)
   and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) <> '3'
union all

SELECT 

	  LEFT(CAST([ExtraParams].query('data(r/trm_prv_id)') as  nvarchar(max)),10)+RIGHT('0000000000'+cast(AgentTerminalID as varchar(10)),10)  trm_prv_id 
      ,[AgentPaymentID]
      ,[PaymentID]
      ,[AgentPaymentID]
      ,[ServiceID]
      ,[GateServiceID]
      ,[PayDate]
      ,[StatusDate]
      ,[Number]
      ,[PaymentInfo]
      ,[AgentTerminalID]
      ,[PaySum]
      ,[ProviderSum]
      ,[Status]
      ,[GateErrorMessage]
      ,[ExtraParams]
,CAST(ExtraParams.query('data(r/isiq_counter)') as nvarchar) isiq_counter
,CAST(ExtraParams.query('data(r/isiq_subid)') as nvarchar) isiq_subid
,[OsmpProviderID]
FROM [gate211].[dbo].[Payment]
where (StatusDate between '2021-03-01' and '2021-04-01' )and ServiceID in (  990,991,998,999)
and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) <> '3' and
len(CAST(ExtraParams.query('data(r/ai_subscriber_type)') as nvarchar))>7 ) a
```

------------------------------------------------------------------------------------------------------------------------------------------

Second table query: Union of files from 1-31: Remove sum values
------------------------------------------------------------------------------------------------------------------------------------------
```/****** Script for SelectTopNRows command from SSMS  ******/
select *into dbo.AzerisiqAll from (SELECT [POST_ID]
      ,[WS_USER_NAME]
      ,[TRANSACTION_DATE]
      ,[TARGET_SUBSCRIBER_ID]
      ,[PAYMENT_AMOUNT]
      ,[TRANSACTION_ID]
  FROM [dbo].[1_10]
  union all
  SELECT [POST_ID]
      ,[WS_USER_NAME]
      ,[TRANSACTION_DATE]
      ,[TARGET_SUBSCRIBER_ID]
      ,[PAYMENT_AMOUNT]
      ,[TRANSACTION_ID]
  FROM [dbo].[11_18]
     union all
  SELECT [POST_ID]
      ,[WS_USER_NAME]
      ,[TRANSACTION_DATE]
      ,[TARGET_SUBSCRIBER_ID]
      ,[PAYMENT_AMOUNT]
      ,[TRANSACTION_ID]
  FROM [dbo].[15_20]
    union all
  SELECT [POST_ID]
      ,[WS_USER_NAME]
      ,[TRANSACTION_DATE]
      ,[TARGET_SUBSCRIBER_ID]
      ,[PAYMENT_AMOUNT]
      ,[TRANSACTION_ID]
  FROM [dbo].[20_25]
    union all
  SELECT [POST_ID]
      ,[WS_USER_NAME]
      ,[TRANSACTION_DATE]
      ,[TARGET_SUBSCRIBER_ID]
      ,[PAYMENT_AMOUNT]
      ,[TRANSACTION_ID]
  FROM [dbo].[26_31]) t
```
------------------------------------------------------------------------------------------------------------------------------------------

Find Differences between each table: AHALI
------------------------------------------------------------------------------------------------------------------------------------------
```
SELECT  count(*), a.TRANSACTION_ID,a.PAYMENT_AMOUNT,m.PaySum,m.trn_id,m.Status from [5may2021_recon].[dbo].[AzerisiqEhali] m
full join [5may2021_recon].[dbo].[AzerisiqAll] a
on a.TRANSACTION_ID = m.trn_id
and a.PAYMENT_AMOUNT = m.PaySum  
WHERE  
 --or 
  (a.TRANSACTION_ID is null and m.Status=2) or
 m.trn_id is  null 
 or (a.TRANSACTION_ID is not null and m.Status=3 and not exists (select * from [dbo].[AzerisiqEhali] c where c.trn_id =m.trn_id and c.status=2))
  
group by a.TRANSACTION_ID,m.PaySum,m.trn_id,a.PAYMENT_AMOUNT,m.Status
order by 1
select sum(payment_amount) AMNT_Az from [dbo].[azerisiqall]
select sum(paysum) AMNT_Modenis from [dbo].[AzerisiqEhali] where status=2


select count(payment_amount) CNT_Az from azerisiqall
select count(paysum) AMNT_Modenis from [dbo].[Azerisiqehali]

select trn_id, count(*), sum(paysum)/count(*) from [dbo].[Azerisiqehali] where status = 2
 group by trn_id
 having count(*) > 1


```
------------------------------------------------------------------------------------------------------------------------------------------


Find Differences between each table: QEYRI-AHALI
------------------------------------------------------------------------------------------------------------------------------------------

```
SELECT  count(*), a.TRANSACTION_ID,a.PAYMENT_AMOUNT,m.PaySum,m.trn_id,m.Status from [dbo].[AzerisiqQEhalim] m
full join [dbo].[AzerisiqQa2] a
--on cast(transaction_id as DECIMAL(28,0)) = m.trn_id
on transaction_id = m.trn_id

and a.PAYMENT_AMOUNT = m.ProviderSum
WHERE  
 --or 
  (a.TRANSACTION_ID is null and m.Status=2) or
 m.trn_id is  null 
 or (a.TRANSACTION_ID is not null and m.Status=3 and not exists (select * from [dbo].[AzerisiqQEhalim] c where c.trn_id =m.trn_id and c.status=2))
  
group by a.TRANSACTION_ID,m.PaySum,m.trn_id,a.PAYMENT_AMOUNT,m.Status
order by 2

select sum(payment_amount) AMNT_Az from [dbo].[azerisiqQa2]
select sum(providersum) AMNT_Modenis from [dbo].[AzerisiqQEhalim] where status=2


select count(payment_amount) CNT_Az from [azerisiqQa2]
select count(providersum) AMNT_Modenis from [dbo].[AzerisiqQEhalim] where status=2

select trn_id, count(*), sum(providersum)/count(*) from [dbo].[AzerisiqQEhalim] where status = 2
 group by trn_id
 having count(*) > 1

```
Now as tables are ready and we have differences list, now we need to analyze and investigate on differences to explore why the difference even exits.
Save the output of the query in an Excel sheet.
1. We need an Excel file containing
Ferq, Novbeti Ayda olacaq, Kecen ayda ugurlu qebul edilib ve Yekun sheets.
Example: S:\MA\Provayder Hesabatlari\202101\azerisiq

2. Ferq - is the general output of the difference query as showed 
