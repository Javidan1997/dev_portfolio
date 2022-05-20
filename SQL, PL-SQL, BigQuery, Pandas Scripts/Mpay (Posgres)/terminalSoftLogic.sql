select   EqSt.id_point as id_point , P.name as point_name, EqSt.last_payment as last_payment, CashUnits.last_collection as last_collect, 
CashUnits.units_count as units_count,CashUnits.units_sum as units_sum,
CASE 
WHEN EqSt.validator_state = 1 THEN 'Pulqabi Dolub'
WHEN EqSt.validator_state = 2 THEN 'Kasset çıxarılıb'
ELSE '' END as validator_state
 from equipment_status EqSt
left join points P on EqSt.id_point = P.id_point
left join (
            select CashBox.id_point, CashBox.last_collection, 
                    sum(CashBox.count) as units_count, /*количество всех купюр на точке*/
                   (sum (CashBox.sum_unit))::numeric(20,2) as units_sum /*сумма всех купюр на точке*/
            from (
                    select CB.id_point,CB.id_cash_box, CB.last_collection, CBC.count /*количество купюр по номиналам*/, 
                            (MU.nominal/100 * CBC.count)::numeric(20,2) as sum_unit /*сумма купюр по номиналам*/
                    from cash_boxes CB
                    left join cash_boxes_counts CBC on (CB.id_cash_box=CBC.id_cash_box) /*cash_boxes_counts хранит информацию о купюрах в боксе купюроприемника*/
                    left join money_units MU on (MU.id_money_unit = CBC.id_money_unit) /*таблица money_units определяет купюры процессинга*/
                    where CB.device_class=3 /*устройство купюроприемник*/) as CashBox
              group by CashBox.id_point,CashBox.last_collection) as CashUnits on (EqSt.id_point = CashUnits.id_point)
              
where P.point_type=0 /*для точек типа Терминал*/ and CashUnits.last_collection is not null 

and CashUnits.last_collection between date_trunc('day', CURRENT_DATE -1) and date_trunc('day', CURRENT_DATE)
AND EqSt.validator_state=1 
  OR CashUnits.units_count>500
