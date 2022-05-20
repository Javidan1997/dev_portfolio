SELECT *
  FROM [Main].[dbo].[Payment]

where [PaymentID] in (

SELECT

      [AgentPaymentID]
     
  FROM [gate].[dbo].[Payment]
 
 where status=1

)
and Status=3
