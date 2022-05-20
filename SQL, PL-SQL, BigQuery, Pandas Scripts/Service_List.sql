/****** Script for SelectTopNRows command from SSMS  ******/
SELECT [ServiceID]
      ,[ServiceName]
      ,s.[ProviderID]
      ,[GateServiceID]
      ,s.[Enabled]
	  , P.ProviderName
	  , P.Enabled,
	  P.Balance
  FROM [gate211].[dbo].[Service] S
  LEFT JOIN dbo.Provider P
  ON s.ServiceID = P.ProviderID
 
