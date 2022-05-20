--Purchase via Card
select gtd.external_id ,* from tx_business_base tbb 
left join tx_business_base_def tbbd on tbb.def_id =tbbd.id
left join gate_tx gt on gt.process_id =tbb.id 
left join gate_tx_def gtd on gtd.id=gt.def_id
where tbb.type='gate_purchase' and tbb.parent_id is not null --and tbbd.status ='processed'
and tbb.performedat >'2021-01-01 00:00:00' and tbb.performedat <'2021-01-29'
--and external_id = '1000258111'


--Purchase via Wallet
select gtd.external_id ,* from tx_business_base tbb 
left join tx_business_base_def tbbd on tbb.def_id =tbbd.id
left join gate_tx gt on gt.process_id =tbb.id 
left join gate_tx_def gtd on gtd.id=gt.def_id
where tbb.type='gate_purchase' and tbb.parent_id is null and tbbd.status ='processed'
and tbb.performedat >'2021-01-01' and tbb.performedat <'2021-01-29'


--Top Up
select gtd.external_id ,* from tx_business_base tbb 
left join tx_business_base_def tbbd on tbb.def_id =tbbd.id
left join gate_tx gt on gt.process_id =tbb.id 
left join gate_tx_def gtd on gtd.id=gt.def_id
where tbb.type='gate_charge' and tbb.parent_id is null and tbbd.status ='processed'
and tbb.performedat >'2021-01-01' and tbb.performedat <'2021-01-29'



--select * from tx_business_client_op tbco 