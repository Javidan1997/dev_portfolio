EXECUTE  [dbo].[GetNewPayment] 
 @Login = N'abdullayevc'
,@PasswordMD5 = N'0eda0f98bb80d3b83bbfec0d9a7c7e38'
,@DealerID=16 --5
  --,@TransactionID
  --,@PaymentID=189250177
  --,@ServiceID=1276
  --,@ProviderID
  ,@CreateTimeFrom='2021-06-01'
  ,@CreateTimeTo='2021-07-01'
  ,@Status=3
  ,@RetryStatus=1
  ,@PointType=1
  ,@RevokeStatus=1 --4
  --,@WithRetry=1
  --,@WithRevoke=1
  --,@IsRetried

GO
