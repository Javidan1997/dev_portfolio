select CAST([ExtraParams].query('data(r/trm_prv_id)') as  nvarchar(max) ) TRID
				,p.PaymentID
				,p.AgentPaymentID
				,p.ServiceID
				,p.PayDate
				,p.StatusDate
				,p.Number
				,p.PaySum
				,p.ProviderSum
				,p.CommissionSum
				,p.Status
				,p.OsmpProviderID
				,CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) AS Agent_ID
					from gate211.dbo.Payment p
					where  (StatusDate between '2021-07-01' and '2021-08-01' )
					   and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) = '18' --17
					   					--into [march_recon].dbo.Payment18

/*select 	CAST([ExtraParams].query('data(r/trm_prv_id)') as  nvarchar(max) ) TRN,
					*from gate211.dbo.Payment p
					where  (StatusDate between '2021-03-01' and '2021-04-01' )
					   and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) = '18'*/ --17
					   					--into [march_recon].dbo.Payment18
