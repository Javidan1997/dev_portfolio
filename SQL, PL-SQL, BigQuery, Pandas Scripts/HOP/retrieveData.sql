select [PaymentID],[AgentPaymentID] as 'PortalPaymentID',[AgentTerminalID] as 'TerminalID', PayDate,[StatusDate],[Number],ServiceName,[Terminal Sum] 'Terminal məbləği',
[Terminal Sum]-QaliqMeblegh as 'HÖP-Ə köçürülən',
[Terminal Sum]-QaliqMeblegh-coalesce([Üst kommisiya],'0') as 'Müştəriyə köçürülən',QaliqMeblegh,
coalesce([Üst kommisiya],'0') as 'Üst kommisiya',coalesce([Alt kommisiya],'0') 'Alt kommisiya',QaliqMeblegh+coalesce([Üst kommisiya],'0')+coalesce([Alt kommisiya],'0') as 'Yekun kommisiya'
from (
Select [PaymentID],[AgentPaymentID],[AgentTerminalID],PayDate,[StatusDate],[Number],s.ServiceId,s.ServiceName,Paysum as 'Terminal Sum',
case when cast([PaymentInfo].query('data(root/QaliqMeblegh)') as nvarchar(max)) is null or
cast([PaymentInfo].query('data(root/QaliqMeblegh)') as nvarchar(max))='' or
cast([PaymentInfo].query('data(root/QaliqMeblegh)') as nvarchar(max))='0.00'
then '0'
when cast([PaymentInfo].query('data(root/QaliqMeblegh)') as nvarchar(max))=-0.4
then 0.6
else 
round(cast([PaymentInfo].query('data(root/QaliqMeblegh)') as nvarchar(max)),2)
end as 'QaliqMeblegh',
cast([PayFields].query('data(fields/field2)') as nvarchar(max)) Commision,
case when p.ServiceID in (1289) ---Belediyye(2572) 
then 
     case when  p.ServiceID in (1289) and  round(Paysum/100,2)>15
						then 15
					    else round(Paysum/100,2)
				end  
    when p.ServiceID in (1293,1294,1295)   --İSB(2576,2577,2578) 
	   then case 
	         when p.ServiceID in (1293,1294,1295)  and round((PaySum*0.5)/100,2)<0.2
	                     then 0.2
			when p.ServiceID in (1293,1294,1295)  and round((PaySum*0.5)/100,2)>15
			             then 15
						 else round((PaySum*0.5)/100,2)
						 end 
    when p.ServiceID in (1720,1721,1722,1723,1724,1725) and  cast([PayFields].query('data(fields/field2)') as nvarchar(max)) is null--DYP(2663,2664,2665,2666,2667,2668)
	                      then round(Paysum/100,2)
    when p.ServiceID in (1742) --Azerisiq(Q) (2684)
	                      then round(Paysum/100,2)
	when p.ServiceID in (1296,1297,1298) --IKZF (2579,2580,2581)
	                     then round((Paysum*0.15)/100,2)
	when p.ServiceID in (1299,1300,1301) --BNA(2582,2583,2584)
	                      then round(Paysum/100,2)
end as 'Alt Kommisiya',
case  when p.ServiceID in (1290,1291,1292) ---Ali Tehsil(2573,2574,2575)
    then case  
		     when (cast([PayFields].query('data(fields/field2)') as nvarchar(max))='0' or cast([PayFields].query('data(fields/field2)') as nvarchar(max)) is null
			 or cast([PayFields].query('data(fields/field2)') as nvarchar(max))=' ')
				    then case when round((Paysum*0.15)/100,2)>15
					then 15
					          when round((Paysum*0.15)/100,2)<0.4  
					then 0.4
					          else 
				        round((Paysum*0.15)/100,2)
					end
			 else 
			cast([PayFields].query('data(fields/field2)') as nvarchar(max))
			     end  	
		  when  p.ServiceID in  (1720,1721,1722,1723,1724,1725) and  cast([PayFields].query('data(fields/field2)') as nvarchar(max)) is not  null 
		       then cast([PayFields].query('data(fields/field2)') as nvarchar(max))  --round((Paysum)/100,2)
		 when p.ServiceID in (1730,1731) --DANX(2672,2673)
		   then case 
		   when round((Paysum*0.15)/100,2)>15
		   then 15
		   when round((Paysum*0.15)/100,2)<0.4
		   then 0.4
		   else     round((Paysum*0.15)/100,2)
		   end 
			  end as 'Üst kommisiya',	
			  			   
PaymentInfo,
PayFields,
ExtraParams
from [dbo].[Payment] p with (nolock)
join [dbo].[Service] s with (nolock) on p.ServiceID=s.ServiceID where p.ServiceID in (
1289,1290,1291,1292,1293,1294,1295,1296,1297,1298,1299,1300,1301,1720,1721,1722,1723,1724,1725,1730,1731,1742 )and status=2 and p.ReceiveDate between '2022-03-01' and '2022-04-01'
) t  
