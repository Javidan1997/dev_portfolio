select  r.ayin_gunleri,kechen_ay , cari_ay, cari_ay - kechen_ay as ferq, ROUND(((cari_ay - kechen_ay)/kechen_ay)*100,0)  as ferq_faiz 
 from ( 
select oper_day as ayin_gunleri,SUM(sum_income)/100 as  kechen_ay
from operations.master 
where state=60 and id_point != 8 and id_provider not in (20,16,17)
and oper_day between date_trunc('month',current_date-interval '1' month) and date_trunc('day', CURRENT_DATE - interval '1 month'- interval '1 day') 
group by oper_day, state 
order by oper_day, state 
) s
LEFT JOIN (
select oper_day as ayin_gunleri,SUM(sum_income)/100 as cari_ay
from operations.master 
where state=60 and id_point != 8 and id_provider not in (20,16,17)
and oper_day between
case 
when Extract(day from Current_date)=1
then date_trunc('month',current_date-interval '1' month)
else
date_trunc('month',current_date )
end 
and date_trunc('day', CURRENT_DATE -1)
--date_trunc('month', CURRENT_DATE) and CURRENT_DATE - interval '1 day'
group by oper_day, state 
order by oper_day, state 
) r ON Extract(day from s.ayin_gunleri)=Extract(day from r.ayin_gunleri)
group by r.ayin_gunleri,kechen_ay,cari_ay
