SELECT 	[AgentPaymentID]  
		,s.[ServiceName]
		,MONTH(StatusDate) Month
		,[Number]
		,[AgentTerminalID]
		,[PaySum]
		,ExtraParams
		,CAST([ExtraParams].query('data(r/sessionid)') as nvarchar) as sessionid
		,CAST([ExtraParams].query('data(r/rabita_session)') as nvarchar) as rabita_session
  FROM [dbo].[Payment] p 
  JOIN Service s ON s.ServiceID=p.ServiceID
	WHERE s.ProviderID in (63) and Status=2 
	and StatusDate between '2021-11-01' and '2021-12-01' 
	and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) <> '3'
