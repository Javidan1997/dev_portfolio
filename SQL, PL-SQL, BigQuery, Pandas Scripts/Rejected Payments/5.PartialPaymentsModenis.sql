EXECUTE  [dbo].[GetNewPayment] 
 @Login = N'aqammadzadae'
,@PasswordMD5 = N'c2caea1c32db0492a967feb3743fb168'
,@DealerID=16 --5
  --,@TransactionID
  --,@PaymentID=189250177
  --,@ServiceID=1276
  --,@ProviderID
  --,@CreateTimeFrom='2015-06-01'
  ,@CreateTimeTo='2021-07-01'
  ,@RevokeTimeFrom='2021-06-01'
  ,@RevokeTimeTo='2021-07-01'  
  ,@Status=2
  ,@RevokeStatus=5
  --,@WithRevoke=1
  --,@WithRetry
  --,@IsRetried
GO
