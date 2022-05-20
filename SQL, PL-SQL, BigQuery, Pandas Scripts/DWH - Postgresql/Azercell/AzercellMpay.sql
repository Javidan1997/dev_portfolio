select q.id_operation,q.id_service ,account ,state,substate,time_point,time_process,time_server,sum_income/100 as sum_income 
from reckon.work_master q left join 
"work".operation_attributes_customer ot on q.id_operation =ot.id_operation 
and ot."name" ='transaction-id'
left join 
reckon.work_services s on q.id_service =s.id_service 
where q.id_service=388
and q.state =60
and q.substate =0
and q.time_process >='2022-02-14'
and q.time_process <'2022-03-01'
and q.time_server >=date'2022-02-14'-interval '7 day'
and q.time_server <date'2022-03-01'+interval '7 day'
