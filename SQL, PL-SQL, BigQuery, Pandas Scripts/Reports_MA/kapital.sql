select
 LEFT(CAST([ExtraParams].query('data(r/trm_prv_id)') as nvarchar ),10)+LEFT(CAST([ExtraParams].query('data(r/online_trm_prv_id)') as nvarchar ),10)+RIGHT('0000000000'+cast(AgentTerminalID as varchar(10)),10)  trm_prv_id,
 *
	into [10october2021_recon].dbo.KapitalModenis
	from gate211.dbo.Payment where ServiceID in ( 544,964)

and StatusDate Between '2021-10-01'and'2021-11-01'
 and
  CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) <> '3'  and status=2
