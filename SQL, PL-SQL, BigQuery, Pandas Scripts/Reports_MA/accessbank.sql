SELECT 
CAST(ExtraParams.query('data(r/access_idnumber)') as nvarchar(MAX)) as access_idnumber,
CAST(ExtraParams.query('data(r/Access_counter)') as nvarchar(MAX)) as Access_counter,
CAST(ExtraParams.query('data(r/prc_agent_id)') as nvarchar(MAX)) as Agent,
    CAST([ExtraParams].query('data(r/trm_prv_id)') as nvarchar) trm_prv_id,

AgentPaymentID,
PaymentID,
s.ServiceName,
os.OsmpProviderID,
PaySum,
Status
Number--,
--* 

FROM gate211.dbo.Payment p 
join gate211.dbo.Service s on p.ServiceID = s.ServiceID
join gate211.dbo.Osmp_Service os on os.ServiceID = s.ServiceID

WHERE StatusDate between '2021-03-01' and '2021-04-01' and p.Status = 2 and 

s.ServiceID in (418 ,419,420,421 ,422,423,599) -- and  ReceiveDate >'2018-12-01' and Number = '6900283441'
