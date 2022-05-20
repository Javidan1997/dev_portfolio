select   Tarixugurlu "Tarix"
		,MeblegUgurlu "Mebleg Ugurlu"
		,SayUgurlu "Say Ugurlu"
		,COALESCE(MeblegUgursuz,0) "Mebleg Ugursuz"
		,COALESCE(SayUgursuz,0) "Say Ugursuz"
		,COALESCE(Meblegnovbe,0) "Mebleg Novbe"
		,COALESCE(Saynovbe,0) "Say Novbe" from (
	select   oper_day Tarixugurlu
			,SUM(sum_income)/100  MeblegUgurlu
			,count(*) SayUgurlu
	from operations.master 
	where id_service=844
	and state=60 -- success
	and oper_day between date_trunc('month', CURRENT_DATE) and CURRENT_DATE - INTEGER '1'
	group by oper_day, state 
	order by oper_day, state 
	) s
	LEFT JOIN (
	select   oper_day tarixugursuz
			,SUM(sum_income)/100  MeblegUgursuz
			,count(*) SayUgursuz
	from operations.master 
	where id_service=844
	and state=80 --rejected
	and oper_day between date_trunc('month', CURRENT_DATE) and CURRENT_DATE - INTEGER '1'
	group by oper_day, state 
	order by oper_day, state 
	) r ON s.tarixugurlu=r.tarixugursuz
	LEFT JOIN (
	select   oper_day tarixnovbe
			,SUM(sum_income)/100  Meblegnovbe
			,count(*) Saynovbe
	from operations.master 
	where id_service=844
	and state=40 --pending
	and oper_day between date_trunc('month', CURRENT_DATE) and CURRENT_DATE - INTEGER '1'
	group by oper_day, state 
	order by oper_day, state 
	) q ON s.tarixugurlu=q.tarixnovbe
