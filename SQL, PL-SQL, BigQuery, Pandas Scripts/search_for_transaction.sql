/****** Script for Search for TR command  ******/
SELECT   [PaymentID]	,[AgentPaymentID]
		,[Status]		,[Number]
		,[PaySum]		,[ProviderSum]
		,[ServiceID]    ,[GateServiceID]
		,[PayDate]		,[StatusDate]			,[ReceiveDate]       
		,[AgentDate]	,[GateNextTryDate]		,[AgentReceipteDate]
		,[WaitToDate]	,[AgentReceipteNumber]	,[AgentTerminalID]     
		,[IsTest]		,[OsmpProviderID]		,[ProviderPaymentIDString]
		,CAST(ExtraParams.query('data(r/card_number)') as nvarchar(max)) 'Card'
	FROM [gate211].[dbo].[Payment] where AgentID=1
--and status=3 and [OsmpProviderID] = 17498
--and Paysum=201  
--and PayDate between '2021-03-29' and '2021-03-30'
and [ServiceID] in (549, 550, 600)
and [StatusDate] between '2021-04-06' and '2021-04-07'
and [PaySum] = 25


