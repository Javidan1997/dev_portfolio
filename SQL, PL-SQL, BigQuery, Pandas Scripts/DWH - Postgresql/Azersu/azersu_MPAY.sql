SELECT q.id_operation,  q.id_provider, q.id_service, account,sum_income/100 AS sum_income,sum_outcome/100 AS sum_outcome,
state, substate, time_point, time_server, time_process, ot.value azersu_txn
from reckon.work_master q
LEFT join "work".operation_attributes_customer ot on ot.id_operation =q.id_operation 
and ot."name" ='transaction-id'
left join reckon.work_services s on (q.id_service=s.id_service)
where q.state = 60      
       and q.substate = 0
       and q.id_service IN (803,1461,1462,1463)
       and q.time_process >= '2022-02-01' 
       and q.time_process < '2022-03-01' 
       and q.time_server >= date '2022-02-01' - interval '7day'
       and q.time_server < date '2022-03-01' + interval '7day'
