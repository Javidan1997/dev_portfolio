select distinct gtd.external_id,tbg.amount ,tbg.commission ,tbg.provider_commission from gate_tx gt left join gate_tx_def gtd on gt.def_id =gtd.id
left join tx_business_base tbb on tbb.id=gt.process_id
left join tx_business_gate tbg on tbb.id=tbg.id
left join emitent_coin ec on ec.id=gt.coin_id
left join org_organization_def ood on ood.organization_id =ec.organization_id
left join history_action ha on tbb.creationaction_id =ha.id
where gtd.external_id in (
select external_id from gate_tx_def gtd
where gtd.status ='SUCCESS' and external_id is not null
group by external_id having count(1)>1)
and tbb.performedat between '2021-01-01' and '2021-02-01'
order by gtd.external_id desc