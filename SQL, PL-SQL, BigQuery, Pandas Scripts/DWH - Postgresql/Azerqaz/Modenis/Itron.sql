SELECT agentdate as PaymentCreateDate,
      AgentPaymentID as AzerqazId, --CAST([PayFields].query('data(fields/field2)') as nvarchar) AzerqazId,--AgentPaymentID etdik cunki AzerqazID null olanlari var idi
    p."Number" as GPG,
    Status,
    PaySum as PayValue,
	ServiceID
    INTO test.Itron_Modenis
FROM reckon.gate_payment p
where ServiceID in( 175 ,745 )  and status = 2
and StatusDate Between '2022-02-01'and'2022-03-01'
