# EMDK

Run query 

Group by and All Transactions

```
DECLARE @DateFrom DateTime
DECLARE @DateTo DateTime
SET @DateFrom='2021-04-01'
SET @DateTo='2021-05-01'

--SELECT id,serviceName,SUM(PaySum) as Amount,SUM(ProviderSum) as ProviderAmount,SUM(Comission) as ComissionAmount,0.00 as CardComissionAmount, Count(*) as Count,Agent,ProviderName FROM
--(
SELECT Number,AgentPaymentID, 
CAST([PaymentInfo].query('data(r/id)') as nvarchar) as id,
CAST([PaymentInfo].query('data(r/serviceName)') as nvarchar(MAX)) as serviceName,
PaySum,
[ProviderSum] - CAST(CAST(PaymentInfo.query('data(r/overpaid)') as nvarchar) as decimal(7,2)) as ProviderSum
,([CommissionSum] + CAST(CAST(PaymentInfo.query('data(r/overpaid)') as nvarchar) as decimal(7,2))) as Comission,
CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) as Agent
,pp.ProviderName
FROM

[dbo].[Payment] p with (nolock) join Service s on p.ServiceID=s.ServiceID join Provider pp on s.ProviderID=pp.ProviderID
WHERE (StatusDate BETWEEN @DateFrom and @DateTo
and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) not in ( '3','10','14')
)
and Status=2
and p.ServiceID in (254,255)
--)t GROUP BY id,serviceName,Agent,ProviderName
--HAVING Agent>3
UNION ALL
--select -- XH digər xidmətlər
--id,
--serviceName as ServiceName,SUM(PaySum) Amount,SUM(ProviderSum) ProviderAmount,SUM(CommissionSum) CommissionAmount,0.00 as CardCommissionAmount,
--count(*) Count, Agent,t.ProviderName FROM
--(
SELECT Number,AgentPaymentID,
CAST([PaymentInfo].query('data(r/id)') as nvarchar) as id,
CAST([PaymentInfo].query('data(r/serviceName)') as nvarchar(MAX)) as serviceName,

PaySum,ProviderSum,CommissionSum, CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) as Agent
,pp.ProviderName
FROM [dbo].[Payment] p with (nolock)
join Service s on p.ServiceID=s.ServiceID join Provider pp on s.ProviderID=pp.ProviderID
WHERE (StatusDate BETWEEN @DateFrom and @DateTo and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) not in ( '3','10','14')
)
and Status=2

and p.ServiceID in (257,258,259,260,261,262,263,264)
--) t GROUP BY id , ServiceName, Agent,t.ProviderName
--HAVING Agent>3
```



```
DECLARE @DateFrom DateTime
DECLARE @DateTo DateTime
SET @DateFrom='2021-07-01'
SET @DateTo='2021-08-01'

SELECT ID,ServiceName,SUM(PaySum) as Amount,SUM(ProviderSum) as ProviderAmount,SUM(Comission) as ComissionAmount,0.00 as CardComissionAmount, Count(*) as Count,Agent,ProviderName FROM
(
SELECT Number,
AgentPaymentID, 
CAST([PaymentInfo].query('data(r/id)') as nvarchar) as ID,
CAST([PaymentInfo].query('data(r/serviceName)') as nvarchar(MAX)) as ServiceName,
PaySum,
[ProviderSum] - CAST(CAST(PaymentInfo.query('data(r/overpaid)') as nvarchar) as decimal(7,2)) as ProviderSum
,([CommissionSum] + CAST(CAST(PaymentInfo.query('data(r/overpaid)') as nvarchar) as decimal(7,2))) as Comission,
CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) as Agent
,pp.ProviderName
FROM

[dbo].[Payment] p with (nolock) join Service s on p.ServiceID=s.ServiceID join Provider pp on s.ProviderID=pp.ProviderID
WHERE (StatusDate BETWEEN @DateFrom and @DateTo
and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) not in ( '3','10','14')
)
and Status=2
and p.ServiceID in (254,255)
)t GROUP BY id,serviceName,Agent,ProviderName
HAVING Agent>3
UNION ALL
select -- XH digər xidmətlər
ID,
ServiceName as ServiceName
,SUM(PaySum) Amount,
SUM(ProviderSum) ProviderAmount,
SUM(CommissionSum) CommissionAmount,0.00 as CardCommissionAmount,
count(*) Count, 
Agent,
t.ProviderName FROM
(
SELECT Number,AgentPaymentID,
CAST([PaymentInfo].query('data(r/id)') as nvarchar) as ID,
CAST([PaymentInfo].query('data(r/serviceName)') as nvarchar(MAX)) as ServiceName,

PaySum,ProviderSum,CommissionSum, CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) as Agent
,pp.ProviderName
FROM [dbo].[Payment] p with (nolock)
join Service s on p.ServiceID=s.ServiceID join Provider pp on s.ProviderID=pp.ProviderID
WHERE (StatusDate BETWEEN @DateFrom and @DateTo and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) not in ( '3','10','14')
)
and Status=2

and p.ServiceID in (257,258,259,260,261,262,263,264)
) t GROUP BY ID , ServiceName, Agent,t.ProviderName
HAVING Agent>3
```

## Then 
Go to RejectedPayments -> Revoked CurrentMonth EMDK Transactions

Take P_ID s and find them in this query

```
Declare @DateFrom date
Declare @DateTo date
set @DateFrom = '2021-03-01'
set @DateTo = '2021-04-01'

SELECT id,serviceName,SUM(PaySum) as Amount,SUM(ProviderSum) as ProviderAmount,SUM(Comission) as ComissionAmount,0.00 as CardComissionAmount, Count(*) as Count,Agent,ProviderName FROM
(SELECT 
CAST([PaymentInfo].query('data(r/id)') as nvarchar) as id,
CAST([PaymentInfo].query('data(r/serviceName)') as nvarchar(MAX)) as serviceName,
PaySum,
[ProviderSum] - CAST(CAST(PaymentInfo.query('data(r/overpaid)') as nvarchar) as decimal(7,2)) as ProviderSum
 ,([CommissionSum] + CAST(CAST(PaymentInfo.query('data(r/overpaid)') as nvarchar) as decimal(7,2))) as Comission,
CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) as Agent
,pp.ProviderName
FROM

[dbo].[Payment] p with (nolock) join Service s on p.ServiceID=s.ServiceID join Provider pp on s.ProviderID=pp.ProviderID
WHERE  (StatusDate BETWEEN @DateFrom and @DateTo
and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) not in ( '3','10','14')
) 
and --Status=2
AgentPaymentID in (497030105,
495213980,
495108020,
491864560,
490638551,
490638412,
490377557,
489697166,
489696933,
489305459,
486224040,
486223942,
486223697,
485029133,
483949269,
472871080,
470406316,
448255237,
322842906
)
and p.ServiceID  in (254,255)
)t GROUP BY id,serviceName,Agent,ProviderName
--HAVING Agent>3

```

## Subtract
Minus the final amount from AllPrvSum - >

```
Declare @DateFrom date
Declare @DateTo date
set @DateFrom = '2021-03-01'
set @DateTo = '2021-04-01'

SELECT 
p.AgentPaymentID,
p.PaymentID,
CAST([PaymentInfo].query('data(r/id)') as nvarchar) as id,
CAST([PaymentInfo].query('data(r/serviceName)') as nvarchar(MAX)) as serviceName,
PaySum,
[ProviderSum] - CAST(CAST(PaymentInfo.query('data(r/overpaid)') as nvarchar) as decimal(7,2)) as ProviderSum
 ,([CommissionSum] + CAST(CAST(PaymentInfo.query('data(r/overpaid)') as nvarchar) as decimal(7,2))) as Comission,
CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) as Agent
,pp.ProviderName
FROM
[dbo].[Payment] p with (nolock) join Service s on p.ServiceID=s.ServiceID join Provider pp on s.ProviderID=pp.ProviderID
WHERE  (StatusDate BETWEEN @DateFrom and @DateTo
and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) not in ( '3','10','14')
) and AgentId = 1 and 

--Status=2
AgentPaymentID in (497030105,
495213980,
495108020,
491864560,
490638551,
490638412,
490377557,
489697166,
489696933,
489305459,
486224040,
486223942,
486223697,
485029133,
483949269,
472871080,
470406316,
448255237,
322842906
)
```


## Also
Subtract this

```
EXECUTE [dbo].[GetNewPayment]
@Login = N'aqammadzadae'
,@PasswordMD5 = N'c2caea1c32db0492a967feb3743fb168'
--,@DealerID
--,@ActDealerID
--,@TransactionID
--,@OuterTransactionID
--,@PaymentID=310540015
--,@PointID
--,@UserID
--,@ProviderID
--,@PayType
--,@Code
,@RevokeStatus=5 -- 4, 5 
--,@RetryStatus
--,@Number='503428514'
--,@PayTimeFrom
--,@PayTimeTo
--,@CreateTimeFrom='2021-01-09'
,@Status=2
,@ServiceID=1108 --1069 1070 1090 1091 1094 1095 1099 1100 1107 1108
--note
--,@CreateTimeFrom='2020-10-01'
--,@CreateTimeTo='2020-11-01'
--,@RevokeTimeFrom = '2020-11-01'

,@CreateTimeTo='2021-04-01'
,@RevokeTimeFrom = '2021-04-01'
,@RevokeTimeTo = '2021-05-01'

--,@RefundedTimeFrom
--,@RefundedTimeTo
--,@RetryDateFrom
--,@RetryDateTo
--,@WithRevoke
--,@WithRetry
--,@IsRetried
--,@IsRefunded
--,@IsFirstInRetryChain
--,@IsLastInRetryChain
--,@IsConfirmed
--,@PointType
--,@PointAddressCode
--,@IncludeExtras=1
-- ,@NomenclatureID=3
--,@IsFishing
--,@Top=10
--,@Debug
GO
```
