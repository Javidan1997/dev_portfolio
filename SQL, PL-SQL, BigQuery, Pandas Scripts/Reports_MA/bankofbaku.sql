SELECT 
PaymentID,AgentPaymentID,Number,PaySum,ProviderSum,StatusDate,
CAST([PaymentInfo].query('data(r/transactionid)') as nvarchar) transactionid ,
CAST([PaymentInfo].query('data(r/providerpaymentid)') as nvarchar) providerpaymentid ,
CAST([PaymentInfo].query('data(r/batchid)') as nvarchar) batchid,
CAST([ExtraParams].query('data(r/bob_debet_batchId)') as nvarchar) bob_debet_batchId,
CAST([ExtraParams].query('data(r/bob_debet_transactionid)') as nvarchar) bob_debet_transactionid,
CAST([ExtraParams].query('data(r/trm_prv_id)') as nvarchar) trm_prv_id
FROM [DWHTEST].dbo.paymentupg WHERE ServiceID in (323,324,325,326,556,1123)
 --(323,324,325)
and (StatusDate between '2021-12-01' and '2022-01-01') and Status =2 and dublikat = 1
