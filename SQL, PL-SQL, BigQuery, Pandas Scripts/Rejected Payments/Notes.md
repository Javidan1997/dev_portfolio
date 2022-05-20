Better design edits are on the way1!!
10.203.180.32\AZDB
username mail


RevokedPayments
 -- ,@RevokeTimeFrom='uzlesme ayi bas'
  --,@RevokeTimeTo='uzlesme ayi son'  
Rejected status=2 @RevokeStatus=5  - natamam legvler
və tam legvler - status=3 RevokeStatus=4 


RevokedCurrentMonth
 -- ,@CreateTimeTo "uzlesme ayina qeder"
 -- ,@RevokeTimeFrom='uzlesme ayi bas'
  --,@RevokeTimeTo='uzlesme ayi son'
Rejected status=2 @RevokeStatus=5  - natamam legvler
və tam legvler - status=3 RevokeStatus=4 	


PartialPayments
 -- ,@CreateTimeTo "uzlesme ayina sonuna qeder
 -- ,@RevokeTimeFrom='uzlesme ayi bas'
  --,@RevokeTimeTo='uzlesme ayi son'  
Rejected status=2 @RevokeStatus=5  - natamam legvler


RetryPayments
 -- ,@CreateTimeTo='uzlesme ayina qeder'
 -- ,@RetryDateFrom='uzlesme ayi bas'
 -- ,@RetryDateTo='uzlesme ayi son'
 -- ,@status=3
 -- ,@WithRetry=1

SuccessCurrentMonth
 ,@CreateTimeTo='2021-04-01'
  ,@RevokeTimeFrom='2021-04-01'
  ,@RevokeTimeTo='2021-05-01' 
  ,@Status=2
  ,@RevokeStatus=3 --2 3 kecmis ay
 

RejectedPayments

  ,@CreateTimeFrom='2021-06-01'
  ,@CreateTimeTo='2021-07-01'
  ,@Status=3
  ,@RetryStatus=1
  ,@PointType=1
  ,@RevokeStatus=1 --4

Retried da olan odenisler kecen ayin rejectedinde var mi? yoxsa sil

 RevokedCurrentMonth(Evvelki ayin odenisleri current monthda qaytarilanlar)
 ,@RevokeTimeFrom='2018-10-01'
 ,@RevokeTimeTo='2018-11-01' 
      ,@WithRevoke=1
   ,@CreateTimeFrom = '2015-06-01'
   ,@CreateTimeTo = '2018-10-01'

sonda baxmaq lazimdir revoked current month kecen ay revokad payments de vermemeliyik     
sonda baxmaq lazimdir revoked current month kecen ay revoked current month da vermemliyik  
