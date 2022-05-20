select 	OM.time_process
		, OM.id_operation
		, OM.account
		, OM.id_point as point
		, OM.sum_outcome
		, length(cast(OM.operation_number as varchar))
		, OM.operation_number as operation
		, length(cast(OM.id_point as varchar )),
       case
           when length(cast(OM.operation_number as varchar)) = 9 then '1' || cast(OM.operation_number as varchar)
           when length(cast(OM.operation_number as varchar)) = 8 then '10' || cast(OM.operation_number as varchar)
           when length(cast(OM.operation_number as varchar)) = 7 then '100' || cast(OM.operation_number as varchar)
           when length(cast(OM.operation_number as varchar)) = 6 then '1000' || cast(OM.operation_number as varchar)
           when length(cast(OM.operation_number as varchar)) = 5 then '10000' || cast(OM.operation_number as varchar)
           when length(cast(OM.operation_number as varchar)) = 4 then '100000' || cast(OM.operation_number as varchar)
           when length(cast(OM.operation_number as varchar)) = 3 then '1000000' || cast(OM.operation_number as varchar)
           when length(cast(OM.operation_number as varchar)) = 2 then '10000000' || cast(OM.operation_number as varchar)
           when length(cast(OM.operation_number as varchar)) = 1 then '100000000' || cast(OM.operation_number as varchar)
           else cast(OM.operation_number as varchar)
        end,
        case
           when length(cast(OM.id_point as varchar)) = 4 then '0' || cast(OM.id_point as varchar)
           when length(cast(OM.id_point as varchar)) = 3 then '00' || cast(OM.id_point as varchar)
           when length(cast(OM.id_point as varchar)) = 2 then '000' || cast(OM.id_point as varchar)
           when length(cast(OM.id_point as varchar)) = 1 then '0000' || cast(OM.id_point as varchar)
           else cast(OM.id_point as varchar)
        end
from operations.master OM
where OM."state" = 60
    AND substate = 0
    AND OM.time_process >= '2021-07-01'
    AND OM.time_process < '2021-08-31'
 --  and OM.time_server >= '2021-08-01'::date - interval '14days'
 --  and OM.time_server < '#time_end#'::date + interval '14days'
 --and account ='63UKB4T'
    AND OM.id_provider = '11'
