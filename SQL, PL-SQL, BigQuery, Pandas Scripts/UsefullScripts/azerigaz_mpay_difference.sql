/****** Script for SelectTopNRows command from SSMS  ******/
SELECT  [SUBID]
      ,a.[account]
      ,[TRN_AMOUNT]
	  ,m.state
	  ,m.substate
	  ,m.comment
	  ,m.sum_income
	  ,m.time_point
	  ,a.date
      ,[date1]
	  ,m.id_operation
	  ,Count(m.id_operation) countchecker
	  

  FROM [12DekabrReconcilition].[dbo].[prv_azerigaz] a
  full join [12DekabrReconcilition].[dbo].mpay_azerigaz m
  on a.account = m.account and a.TRN_AMOUNT = m.sum_income and  Cast(day(a.date1) as int) = CAST(Right(LEFT(m.time_point,10),2) as int) 
  and CAST(Right(LEFT(m.time_point,13),2) as int) = CAST(Right(LEFT(a.date,13),2) as int)  
  where a.SUBID is not null 
  group by  [SUBID]
      ,a.[account]
      ,[TRN_AMOUNT]
	  ,m.state
	  ,m.comment
	  ,m.sum_income
	  ,m.time_point
      ,[date1]
	  ,m.id_operation
	  ,a.date
	  ,m.substate
