SELECT [PaymentID]
      ,[PointID]
      ,[TransactionID]
      ,[TryNumber]
      ,[UserID]
      ,[ReceiptNumber]
      ,[PayTime]
      ,[CreateTime]
      ,[StatusTime]
      ,[ServiceID]
      ,[ProviderID]
      ,[Number]
      ,[Status]
      ,[ProcessStatus]
      ,[PayValue]
      ,PortalComment
      
  FROM [Main].[dbo].[Payment]
  where StatusTime between '2021-10-12' and '2021-11-24' and ServiceID in (2366,2367) and Status = 3 and PortalComment is not null
