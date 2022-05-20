USE [Main]

-- TODO: Set parameter values here.

EXECUTE  [dbo].[GetNewPayment] 
   @Login='zulphugarlis'
  ,@PasswordMD5='06cdef8fabc2eae05ae7b150633bc20f'
  ,@DealerID=5
  --,@ActDealerID
  --,@TransactionID
  --,@OuterTransactionID
  --,@PaymentID=189250177
  --,@PointID
  --,@UserID
  --,@ServiceID=1276
  --,@ProviderID
    ,@Status=3
  --,@PayType
  --,@Code
  --,@RevokeStatus
  --,@RetryStatus
  --,@Number
  --,@PayTimeFrom
  --,@PayTimeTo
	,@CreateTimeFrom='2015-06-01'
	,@CreateTimeTo='2021-03-01'
  --,@StatusTimeFrom
  --,@StatusTimeTo
 -- ,@RevokeTimeFrom='2018-06-01'
 -- ,@RevokeTimeTo='2018-07-01'  
  --,@RefundedTimeFrom
  --,@RefundedTimeTo
  ,@RetryDateFrom='2021-03-01'
  ,@RetryDateTo='2021-04-01'
  --,@WithRevoke=1
  ,@WithRetry=1
  --,@IsRetried
  --,@IsRefunded=1   --baglanmis odenisleri cixartmaq ucun
  --,@IsFirstInRetryChain
  --,@IsLastInRetryChain
  --,@IsConfirmed
  --,@PointType
  --,@PointAddressCode
  --,@IncludeExtras
  --,@NomenclatureID
  --,@Top
  --,@Debug
GO
