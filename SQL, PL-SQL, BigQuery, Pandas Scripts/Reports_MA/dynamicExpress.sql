select [ExtraParams].query('data(r/trm_prv_id)') modenis_trn_id
	  ,[ExtraParams].query('data(r/agt_id)') Agent_İD
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
where s.ProviderID = 205
	and  StatusDate Between '2021-07-01'and'2021-08-01'
    and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) <> '3'
    and [Status] = 2
