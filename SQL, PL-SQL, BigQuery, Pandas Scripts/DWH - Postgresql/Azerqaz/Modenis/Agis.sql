----Create-----

SELECT --top 120-- AzerQazDirect 
p.OsmpProviderID,
p.AgentPaymentID as AzeriQazID, p.ReceiveDate, p."Number", p.PaySum, p.Status
  INTO   test.Agis_Modenis
  FROM   reckon.gate_payment p
where  ServiceID = 275 and 
  StatusDate Between '2022-02-01'and'2022-03-01'
    order by agentdate
    
    
-----Find difference--------

SELECT *

  FROM   test.agis_azerqaz a
  full join test.agis_modenis m on cast (a.trn as varchar) = cast (m.azeriqazid as varchar)
where  a.trn  is null and m.status = 2 or m.azeriqazid is null and m.status = 2
