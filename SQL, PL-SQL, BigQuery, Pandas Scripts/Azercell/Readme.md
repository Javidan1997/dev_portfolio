# Azercell



First table query:
------------------------------------------------------------------------------------------------------------------------------------------
```
select r.AgentPaymentID,
    a.payment.value('(stan/text())[1]', 'varchar(20)') as 'stan' ,
    a.payment.value('(response_code/text())[1]', 'varchar(20)') as 'responsecode', 
    a.payment.value('(transaction_DateTime/text())[1]', 'varchar(20)') as 'time' ,
    a.payment.value('(transaction_DateTime/text())[1]', 'varchar(10)') as 'date' ,
    a.payment.value('(amount/text())[1]', 'decimal(18,2)') as 'amount' ,
'994'+Number as Number,PaySum,PaymentID,
 case
 When CAST(PaymentInfo.query('data(root/CheckXml/prepaid)') as varchar)='1' then 'prepaid'
 When CAST(PaymentInfo.query('data(root/CheckXml/partial)') as varchar)='1' then 'postpaid'
 else 'Undefined'
 end as ServiceType,
 Status
 into [dbo].[AzercellM4]
from 
    [gate211].dbo.Payment r
    cross apply r.PaymentInfo.nodes('/root/payment') a(payment)
 where 
 -- Status=2
  ServiceID =543 and
(StatusDate between '2019-09-01' and '2019-10-01' )
 order by StatusDate
```
------------------------------------------------------------------------------------------------------------------------------------------

Second table query:
------------------------------------------------------------------------------------------------------------------------------------------
```
/****** Script for SelectTopNRows command from SSMS  ******/
select *into dbo.AzercallAll2
from Azercell1
union all select *from Azercell2 
union all select *from Azercell3
```
------------------------------------------------------------------------------------------------------------------------------------------

Find Differences between each table:
------------------------------------------------------------------------------------------------------------------------------------------
```
(Select * from 
	(Select Number,sum(cast(amount as decimal(18,2))) sum_M from [dbo].[AzercellM] 
		where Status=2 group by Number ) 
m Full Join 
	(Select [Current Telephone Number],sum(cast([Pay Amount] as decimal(18,2))) SUM_A from [dbo].[AzercellAll]
		group by [Current Telephone Number]) a 
		on m.Number = a.[Current Telephone Number] 
		Where CAST(a.SUM_A as decimal(18,2))<>CAST(m.sum_M as decimal(18,2)) 
		or a.[Current Telephone Number] is null 
		or m.Number is null )
```
------------------------------------------------------------------------------------------------------------------------------------------

Types of Differences:

1) Keçən aydan qalan ödənişlər (Ümummi Diff-dən həmin TR-ləri çıx)
2) Null və ya 994 olan ödənişlər: 

```select where number = 994 or null order by date``` - Compare two tables according to date and amount

3) Azercell-də olub Gate-də olmayanlar: 
 a) Yarımçıq ləğvin qalığı
 b) Portalda uğurlu - OK
 c) Ekspert rəyinə müraciət
 
4) Gələn ayda olan ödənişlər - ask Günay.

General Azercell Difference Report

```
Select * from 	
	(Select Number,sum(cast(amount as decimal(18,2))) sum_M from [dbo].[AzercellM] 
	where Status=2 group by Number ) 
	m Full Join 
	(Select [Current Telephone Number],sum(cast([Pay Amount] as decimal(18,2))) SUM_A from [dbo].[AzercellAll]
	group by [Current Telephone Number]) a 
		on m.Number = a.[Current Telephone Number] 
		Where CAST(a.SUM_A as decimal(18,2))<>CAST(m.sum_M as decimal(18,2)) 
		or a.[Current Telephone Number] is null 
		or m.Number is null 

select count(*) Azercell_CNT from AzercellAll 
select count(*) Modenis_CNT from AzercellM where status=2

select sum([Pay Amount]) Azercell_CNT from AzercellAll
select sum(Amount) Modenis_AMNT from AzercellM where status=2

select *from AzercellAll where [Current Telephone Number] = '994509756999'
select *from AzercellM where [Number] = '994509756999'
select *from AzercellAll where [Current Telephone Number] = '994' or [Current Telephone Number] = '994' order by [Payment Date]
```
 
