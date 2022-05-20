SELECT id_operation ,m.id_service ,id_provider ,id_city ,id_point ,time_point ,time_server ,time_process, sum_income/100 as sum_income , sum_comm/100 as sum_comm , sum_outcome/100 as sum_outcome ,(sum_income - (sum_outcome + sum_comm))/100 as qaliq, operation_number , time_provider,sf."name" 
from operations.master m 
full join public.services sf 
on m.id_service = sf.id_service 
where sum_income - (sum_outcome + sum_comm) > 0
and sum_outcome != 0
and 
time_point between '2021-09-01' and '2021-10-01'
