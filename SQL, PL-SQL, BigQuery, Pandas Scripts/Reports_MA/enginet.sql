select [ExtraParams].query('data(r/enginet_transactionid)') en_trn_id,[ExtraParams].query('data(r/trm_prv_id)') modenis_trn_id ,
Number,PaySum,AgentPaymentID,PaymentID

      ,[PaymentID]
      ,[AgentPaymentID]
      ,[ProviderPaymentIDString]
      ,[PayDate]
      ,[StatusDate]
	  ,Status,*

from gate211.dbo.Payment where ServiceID in (

299,
300,
693
)
and
 StatusDate Between '2021-04-01'and'2021-05-01'
   and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) <> '3'
   and [Status] = 2
