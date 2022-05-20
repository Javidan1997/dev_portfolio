SELECT 
case 
when  Cast(s.id as int)  in (18193,18239,18200,18184,18184,18233,18185,18185)
then Cast(s.id as int)
else 77777
end ID      
      ,"Service Name" as ServiceName
	  ,SUM(s.amount)+SUM(s.chargecommission) +SUM(s.purchasecommission) as Amount
	  ,SUM(s.amount) as ProviderAmount
      ,SUM(s.purchasecommission) as CommissionAmount
	  ,SUM(s.chargecommission) as CardComission
	  ,Count(s.p_id) as Count
      ,cast(agent as int) as Agent
      ,description as ProviderName
     
      
  FROM reckon.sdk_provider_trnsaction s
  where s.p_date between '2022-02-01' and '2022-03-01'
  group by Cast(s.id as int),s.description,s."Service Name",s.agent

  union all 

SELECT  888888 as ID,'Kartdan balansın artırılması'  as ServiceName, cast(s.total as float) as Amount, cast(s.amount as float) as ProviderAmount,
cast(s.prvgatecomm as float) as CommissionAmount, cast(s.cardoprcomm as float) as CardCommissionAmount, s.count  as Count,
cast(s.agent as int) as Agent ,'Yığım (Mpay)'  as ProviderName  

from reckon.sdk_report_by_services s
where Cast(s.id as int) = 1018
group by 1,2,3,4,5,6,8,9
   union all

SELECT  888888  as ID,'Mpay terminallarından balansın artırılması'  as ServiceName,cast(a.Amount as float)  as Amount, cast(a.Amount as float) as ProviderAmount,
0.00 as CommissionAmount, 0.00 as CardCommissionAmount, a.Count  as Count,
19 as Agent ,'Yığım (Mpay)'  as ProviderName  
from
(SELECT SUM(p.PaySum) as Amount, COUNT(p.PaymentID) as Count
  FROM reckon.gate_payment p
  where ServiceID = 762 and StatusDate between '2022-02-01' and '2022-03-01'  and AgentTerminalID = 4702 and Status = 2
  group by  p.AgentTerminalID) a
 group by 1,2,3,4,5,6,7,8,9

union all

SELECT 888888 as ID,'Modenis terminallarından balansın artırılması'  as ServiceName, 

cast((SELECT  s.total
from reckon.sdk_report_by_services s
where Cast(s.id as int) = 1017) - (select SUM(p.PaySum)
  FROM reckon.gate_payment p
  where ServiceID = 762 and StatusDate between '2022-02-01' and '2022-03-01'  and AgentTerminalID = 4702 and Status = 2
  group by  p.AgentTerminalID) as float) as Amount, 

cast((SELECT  s.total
from reckon.sdk_report_by_services s
where Cast(s.id as int) = 1017) - (select SUM(p.PaySum)
  FROM reckon.gate_payment p
  where ServiceID = 762 and StatusDate between '2022-02-01' and '2022-03-01'  and AgentTerminalID = 4702 and Status = 2
  group by  p.AgentTerminalID) as float)   as ProviderAmount,

0.00 as CommissionAmount,
0.00 as CardCommissionAmount, 

(SELECT  s.COUNT
from reckon.sdk_report_by_services s
where Cast(s.id as int) = 1017) - (select COUNT(p.PaymentID)
  FROM reckon.gate_payment p
  where ServiceID = 762 and StatusDate between '2022-02-01' and '2022-03-01'  and AgentTerminalID = 4702 and Status = 2
  group by  p.AgentTerminalID)    as Count,

5 as Agent ,
'Yığım (Modenis)'  as ProviderName
