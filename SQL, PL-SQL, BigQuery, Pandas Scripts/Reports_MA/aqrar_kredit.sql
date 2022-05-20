select [ExtraParams].query('data(r/nbc_account)') en_trn_id
	  ,[ExtraParams].query('data(r/nbc_customer)') customer
	  ,[ExtraParams].query('data(r/trm_prv_id)') modenis_trn_id
	  ,[Number]
	  ,[PaySum]
      ,[PaymentID]
      ,[AgentPaymentID]
      ,[PayDate]
      ,[StatusDate]
	  ,[Status]
	from gate211.dbo.Payment where ServiceID = 839 
	and StatusDate Between '2021-06-01'and'2021-07-01'
	--and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) <> '3'
    --and [Status] = 2
	--and CAST([ExtraParams].query('data(r/nbc_account)') as nvarchar) = 'AZ32ACJT41010170321010994413'
      and CAST([ExtraParams].query('data(r/nbc_customer)') as nvarchar(44)) = 'Abdullayeva Gulsabah Pasa qizi'

-- Extra Params
--SELECT TOP 1000 [PaymentID]
--,[ExtraID]
--,[ExtraValue]
--FROM [Main].[dbo].[Payment_Extra]
--where PaymentID in (
--SELECT
--[PaymentID]

--FROM [Main].[dbo].[Payment]
--where CreateTime>'2021-01-01' and ServiceID=2126
--)
--and ExtraValue='000000021780'
