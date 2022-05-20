select sum(m.paysum) from ZennerM m left join ZennerA a on m.trm_prv_id=a.REF_NUM where a.REF_NUM is not null
 select sum(a.TOTAL_AMOUNT) from ZennerA a left join ZennerM m on m.trm_prv_id=a.REF_NUM where m.trm_prv_id is not null

 select * from ZennerM m left join ZennerA a on m.trm_prv_id=a.REF_NUM where a.REF_NUM is  null
 select * from ZennerA a left join ZennerM m on m.trm_prv_id=a.REF_NUM where m.trm_prv_id is  null

select * from ZennerM where number=0189200035187


select * from ZennerA where meter_id=0189200035187



--select * from ZennerM where OsmpProviderID=18050


--DELETE FROM ZennerM WHERE  OsmpProviderID=18050 and PaySum=0 ;
select  sum(paysum) from ZennerM 
select sum(TOTAL_AMOUNT)  from ZennerA 



select * from zennera where total_amount<0


 select sum(total_amount) from zennera
 select sum(paysum) from zennerm

 SELECT  ref_num
FROM zennera
GROUP BY ref_num
HAVING COUNT(ref_num) > 1;

 SELECT  trm_prv_id,number,paysum
FROM zennerm
GROUP BY trm_prv_id,number,paysum
HAVING COUNT(trm_prv_id) > 1;

SELECT left ([trm_prv_id], len([trm_prv_id]) -20)+
right ([trm_prv_id], len([trm_prv_id]) -20) from ZennerM where len([trm_prv_id])>20;


UPDATE ZennerM
SET trm_prv_id = left ([trm_prv_id], len([trm_prv_id]) -20)+
right ([trm_prv_id], len([trm_prv_id]) -20) 
where len([trm_prv_id])>20 ;


SELECT left (REF_NUM, len(REF_NUM) -20)+
right (REF_NUM, len(REF_NUM) -20) from ZennerA where len(REF_NUM)>20;


select REF_NUM from zennera where len(REF_NUM)>20;