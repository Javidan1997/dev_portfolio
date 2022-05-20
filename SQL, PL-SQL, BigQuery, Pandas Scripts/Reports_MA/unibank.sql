select  s.servicename
 ,CAST([PaymentInfo].query('data(r/sessionid)') as nvarchar) as sessionid
 ,CAST([ExtraParams].query('data(r/accunibank)') as nvarchar) asaccunibank
 ,Number as PinCode
 ,PaySum, CONVERT(VARCHAR(19), StatusDate, 120) DateTime
  INTO [dbo].UnibankAll
	from gate211.dbo.Payment p with(nolock)
		join gate211.dbo.Service s 
		on p.ServiceID=s.ServiceID 
	where s.[ProviderID]=14
	and StatusDate between '2021-07-01' and '2021-08-01'
	and Status=2
