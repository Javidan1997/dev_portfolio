select 
 CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) AgentId,
 CAST(ExtraParams.query('data(r/trm_prv_id)') as nvarchar)+RIGHT('0000000000'+CAST(AgentTerminalID as nvarchar),10) Tr_Id,
 Number,
 AgentPaymentID,
 PaySum,
 PaymentID,
 s.ServiceID,
 PayDate,
 StatusDate,
 OsmpProviderID,
 s.ServiceName
 from gate211.dbo.Payment p
left join gate211.dbo.Service s on
s.ServiceID=p.ServiceID
left join gate211.dbo.Provider pp
on pp.ProviderID=s.ProviderID
where 

 (StatusDate between '2021-07-01' and '2021-08-01' ) and pp.ProviderID =101 and status=2 
   and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) <> '3'
