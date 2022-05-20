SELECT m.id_operation,  id_provider, id_service, account,  state, substate, time_point, time_server,time_process,sum_income/100 as sum_income, c."comment" 
from operations.master m 
full join public.operation_comments c on m.id_operation = c.id_operation 
where id_service in (800,802) and state in (80) and c."comment"  is null
AND time_process >= '2021-12-19'
and time_process < '2021-12-21'
