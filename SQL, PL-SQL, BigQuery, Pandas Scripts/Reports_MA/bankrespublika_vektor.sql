select [ExtraParams].query('data(r/trm_prv_id)') modenis_trn_id
	  ,[Number]
	  ,[PaySum]
	  ,[AgentPaymentID]
      ,[PaymentID]
      ,[PayDate]
      ,[StatusDate]
	  ,[Status]
	  ,s.[ServiceID]
	FROM gate211.dbo.Payment p with(nolock) 
	join gate211.dbo.Service s 
	on p.ServiceID=s.ServiceID
where s.ServiceID in ('126','127')
	and  StatusDate Between '2021-09-01'and'2021-10-01'
    and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) <> '3'
    and [Status] = 2
