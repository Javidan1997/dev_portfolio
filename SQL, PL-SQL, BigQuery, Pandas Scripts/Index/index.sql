create clustered index PK_Payment on [gate211].[dbo].[Payment](PaymentID)

create nonclustered index IX_Payment_AgentID_AgentPaymentID on [gate211].[dbo].[Payment](AgentID, AgentPaymentID)
create nonclustered index IX_Payment_Status on [gate211].[dbo].[Payment]([Status])
create nonclustered index IX_Payment_ServiceID on [gate211].[dbo].[Payment](ServiceID)
create nonclustered index IX_Payment_StatusDate on [gate211].[dbo].[Payment](StatusDate)
create nonclustered index IX_Payment_ServiceID_StatusDate on [gate211].[dbo].[Payment](ServiceID, StatusDate)

create nonclustered index IX_Payment_AgentPaymentID on [gate211].[dbo].[Payment](AgentPaymentID)






