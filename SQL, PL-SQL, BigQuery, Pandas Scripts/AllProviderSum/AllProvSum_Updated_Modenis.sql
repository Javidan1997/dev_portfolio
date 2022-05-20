select LEFT(pb.ID,10) as ID,pb.ServiceName, SUM(pb.PaySum) Amount,
case when SUM(pb.PaySum)!= SUM(pb.ProviderSum)+SUM(pb.CommissionSum)
then SUM(pb.PaySum)-SUM(pb.CommissionSum)
else SUM(pb.ProviderSum) end  ProviderAmount,
SUM(pb.CommissionSum) CommissionAmount, SUM(pb.CardCommissionAmount) CardCommissionAmount, count(*)

 Count_,
pb.Agent ,pb.ProviderName  
from (select 
  case when s.ProviderID=51 
  then Cast(p.OsmpProviderID as nvarchar(30))+
    CASE
     WHEN LEFT(p.Number, 2) in ('01','02','03','04','05','06','07','08','09','10','11','13','15','18','22','31','32','33','34','35','36','37','38','39','40',
    '41','42','43','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','65','66','67','68','69','70','71','72',
    '73','74','75','76','77','78','79','81','82','83','84','85','86') THEN N'01'
     WHEN LEFT(p.Number, 2) = '27' THEN N'02'
     WHEN LEFT(p.Number, 2) = '80' THEN N'05'
     WHEN LEFT(p.Number, 2) in ('28','29','44','64') THEN N'06'
     ELSE ' 00' END
  when p.ServiceID  in(291)
  then CASE WHEN p.PaySum<200 THEN 
    CAST(p.OsmpProviderID as nvarchar)+'200'
    ELSE CAST(p.OsmpProviderID as nvarchar) END
  when p.ServiceID in(312,1242)
  then CASE WHEN p.PaySum<500 THEN 
    CAST(p.OsmpProviderID as nvarchar)+'500'
    ELSE CAST(p.OsmpProviderID as nvarchar) END
  when p.ServiceID  in (254,255,257,258,259,260,261,262,263,264)
  then CAST(p.[PaymentInfo].query('data(r/id)') as nvarchar) 
  else CAST(p.OsmpProviderID as nvarchar) end  as ID 
,pp.ProviderName
, case when  s.ProviderID=51 
  then s.ServiceName+CASE 
    WHEN LEFT(p.Number, 2) in ('01','02','03','04','05','06','07','08','09','10','11','13','15','18','22','31','32','33','34','35','36','37','38','39','40',
    '41','42','43','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','65','66','67','68','69','70','71','72',
    '73','74','75','76','77','78','79','81','82','83','84','85','86') THEN N' Azersu ASC'
    WHEN LEFT(p.Number, 2) = '27' THEN N' Seki TSC'
    WHEN LEFT(p.Number, 2) = '80' THEN N' Gence TSC'
    WHEN LEFT(p.Number, 2) in ('28','29','44','64') THEN N' Birlesmis sukanal MMC'
    ELSE 'Unknown' END
  when p.ServiceID  in(291)
  then CASE WHEN p.PaySum<200 THEN s.ServiceName+' 200 az' ELSE s.ServiceName END 
  when p.ServiceID in(312,1242)
  then CASE WHEN p.PaySum<500 THEN 
    CAST(p.OsmpProviderID as nvarchar)+'500'
    ELSE CAST(p.OsmpProviderID as nvarchar) END
  when p.ServiceID  in (254,255,257,258,259,260,261,262,263,264)
  then CAST(p.[PaymentInfo].query('data(r/serviceName)') as nvarchar(MAX))
  else s.ServiceName end  ServiceName


,  case when p.ServiceID in(618)
	then  CAST(CAST (p.[PaymentInfo].query('data(root/paid)') as nvarchar) as float) 
	else p.PaySum end PaySum 
, 
--adding providersum to agent 17 and 18

CASE
    when p.Agent in ('17', '18')
	then 
	--checking null values
	case
	when sd.chargecommission is null or sd.purchasecommission is null
	then PaySum
	else PaySum - sd.chargecommission - sd.purchasecommission
	end
    when p.ServiceID in(618) 
	then CAST(CAST (p.[PaymentInfo].query('data(root/payable)') as nvarchar) as float)
	when  p.OsmpProviderID in (18106,18107)
	then (CAST(CAST (p.[PaymentInfo].query('data(root/debt)') as nvarchar) as float))
	when p.ServiceID  in (254,255)
    then p.[ProviderSum] - CAST(CAST(p.PaymentInfo.query('data(r/overpaid)') as nvarchar) as decimal(7,2))
	when p.ProviderSum=p.PaySum
	then p.PaySum-p.CommissionSum
	else p.ProviderSum end ProviderSum
,
--adding cardcommissionsum to agent 17 and 18

CASE
when p.Agent in  ('17', '18')
then (CASE when sd.chargecommission is null then 0.00 else sd.chargecommission end)
 else 0.00 end  as CardCommissionAmount
,
--adding commissionsum to agent 17 and 18

    CASE 
    when p.agent in ('17', '18')
	then (CASE when sd.purchasecommission is null then 0.00 else sd.purchasecommission end)
	WHEN p.OsmpProviderID in (17217, 17218, 17219, 17220) THEN 1.00	  
	when p.ServiceID in(126,127)
	then CAST(CAST(p.[PayFields].query('data(fields/field4)') as nvarchar) as float) 
	when p.ServiceID in(355)
	then CAST(CAST (p.[PaymentInfo].query('data(r/qaliq)') as nvarchar) as float)
	when p.ServiceID in(618)
	then CAST(CAST (p.[PaymentInfo].query('data(root/residual)') as nvarchar) as float)
	when  p.ServiceID in(631,632,649)
	then (p.CommissionSum+CAST(CAST (p.[PaymentInfo].query('data(root/overpaid)') as nvarchar) as float))
	when pp.ProviderID = 135
	then 0.236
	when p.ServiceID  in (254,255)
    then (p.[CommissionSum] + CAST(CAST(p.PaymentInfo.query('data(r/overpaid)') as nvarchar) as decimal(7,2))) 
	when p.CommissionSum is null then 0.00
	ELSE p.CommissionSum  END  AS CommissionSum

,p.agent as  agent

  FROM [DWHTEST].[dbo].[gate_payment] p with (nolock) 
join [DWHTEST].[dbo].gate_Service s with (nolock) on p.ServiceID=s.ServiceID join [DWHTEST].[dbo].gate_Provider pp with (nolock) on s.ProviderID=pp.ProviderID 

--joining sdk and upg through main base

join [DWHTEST].[dbo].[main_payment] m with (nolock) on p.AgentPaymentID = m.PaymentID left join [DWHTEST].[dbo].[sdk_provider_trnsaction] sd with (nolock) on m.TransactionID = sd.p_id

where (StatusDate between '2022-01-01' and '2022-02-01' ) 
and p.agent not in ( '3','10','14')
and p.Status=2  and p.Dublikat=1 
)pb 

group by pb.ID, pb.ServiceName, pb.Agent ,pb.ProviderName

--adding kartdan balansin artirilmasi

 UNION  all

SELECT s.[id] as ID,s.[servicename]  as ServiceName, s.[total] as Amount, s.[amount] as ProviderAmount,
s.[purchascomission] as CommissionAmount, s.[chargecomission] as CardCommissionAmount, s.[count ] as Count,
s.[agent] as Agent ,'MPAY MMC'  as ProviderName  

from [DWHTEST].[dbo].[sdk_report_by_services] s with (nolock) 

where s.id = 1018
