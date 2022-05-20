
 select  CAST([ExtraParams].query('data(r/trm_prv_id)') as nvarchar) trm_prv_id 
 ,CAST([ExtraParams].query('data(r/abb_accountnumber)') as nvarchar) abb_accountnumber 
 ,CAST([ExtraParams].query('data(r/abb_rrn)') as nvarchar) RrnID 
       ,[PaymentID]
      ,[AgentID]
      ,[AgentPaymentID]
      ,[ProviderPaymentID]
      ,[ProviderPaymentIDString]
      ,[ServiceID]
      ,[StatusDate]
      ,[Number]
      ,[AgentTerminalID]
      ,[PaySum]
      ,[CommissionSum]
      ,[ProviderComission]
      ,[IsTest]
      ,[TestMode]
 from gate211.dbo.Payment where
 ServiceID in ( 
 722,723,765 ,766 ,767 ,768,
 769,770 ,771 ,772,773 ,774,
 652,653 ,654,655 ,656,657,1069,1070,1191
 )
 and StatusDate between '2021-10-01'and'2021-11-01' and Status = 2
 and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) <> '3'
