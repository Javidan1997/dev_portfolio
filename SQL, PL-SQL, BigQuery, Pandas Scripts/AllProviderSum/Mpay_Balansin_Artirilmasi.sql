/****** Script for SelectTopNRows command from SSMS  ******/
SELECT SUM(p.PaySum),SUM(p.CommissionSum), p.AgentTerminalID
  FROM [gate211].[dbo].[Payment] p
  where ServiceID = 762 and StatusDate between '2021-11-01' and '2021-12-01'  and AgentTerminalID = 4702
  group by  p.AgentTerminalID
