select  [ExtraParams].query('data(r/trm_prv_id)') TR_ID
       ,[ExtraParams].query('data(r/agt_id)') Agent_ID
       ,[Number]
       ,[PaySum]
       ,[AgentPaymentID]
       ,[PaymentID]
       ,[PayDate]
       ,[StatusDate]
       ,[Status]
	FROM gate211.dbo.Payment p with(nolock) 
	join gate211.dbo.Service s 
	on p.ServiceID=s.ServiceID
		where s.ProviderID = ***
		and  StatusDate Between '2021-08-01'and'2021-09-01'
		and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) <> '3' --exclude test transactions
		and [Status] = 2 --include only successfull transactions
