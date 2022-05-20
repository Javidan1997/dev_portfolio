SELECT p.PointID as 'TerminalID',s.OSMPProviderID as 'OsmpID',s.Name as N'Servis adı', SUM(PayValue) as N'Ümumi Məbləğ'
  FROM Main.[dbo].[Payment] p with (nolock)
  full join [dbo].[Service] s on p.ServiceID = s.ServiceID
  where p.Status = 2 and p.PayTime between DATEADD(DAY, -1, CAST(GETDATE() AS date)) and  DATEADD(DAY, 0, CAST(GETDATE() AS date))
  group by p.PointID, s.OSMPProviderID, s.Name
  order by p.PointID
