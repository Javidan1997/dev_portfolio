select StatusDate as PaymentCreateDate,OsmpProviderID, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,
AgentPaymentID as AzeriQazID, ReceiveDate, p."Number", PaySum, Status,ServiceID,transactionid 
 into test.zenner_mart_modenis
	from reckon.gate_payment  p where ServiceID in ( 992)
and StatusDate Between '2022-03-01'and'2022-04-01'
  and status=2
  
  
  
  
 select count(a.ref_num) count_gaz from  test.zenner_mart_gaz a;

select sum(cast(a.total_amount as float)) sum_gaz from  test.zenner_mart_gaz a;

select count(b.providerpaymentidstring) count_modenis FROM test.zenner_mart_modenis b;

select sum(b.paysum) sum_modenis FROM test.zenner_mart_modenis b;


select * from test.zenner_mart_modenis a
full join test.zenner_mart_gaz b on a.providerpaymentidstring = b.ref_num 
where a.providerpaymentidstring is null or b.ref_num is null;




select count(a.ref_num),a.ref_num,sum(cast(a.total_amount as float) )/2 onepaymentsum
from test.zenner_mart_gaz a
group by a.ref_num,a.total_amount
having count(a.ref_num) > 1;

select count(a.providerpaymentidstring),a.providerpaymentidstring,sum(a.paysum)/2 onepaymentsum
from test.zenner_mart_modenis a
group by a.providerpaymentidstring,a.paysum 
