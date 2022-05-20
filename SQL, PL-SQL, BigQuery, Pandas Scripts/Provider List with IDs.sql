select gp.external_id id, 
					gmpam.productname "name", 
					replace( (gpad.settings::json-> 'merchantId')::text,'"','') mid,
					egpd.emanat_details::json -> 'details'  ->> 'lName' display_name,
					egpd.emanat_details::json -> 'details'  ->> 'sName' description,
					gp.id product_id,
					gpd.id product_def_id,
					gpad.settings settings 
				from gate_millikart_provider_account_member gmpam 
				left join gate_product gp on gp.id=gmpam.product_id 
				left join gate_product_def gpd on gpd.id =gp.definition_id 
				left join gate_provider_account gpa on gmpam.account_id =gpa.id
				left join emanat_gate_product egp on egp.external_id =gp.external_id 
				left join emanat_gate_product_def egpd on egpd.id=egp.def_id 
				left join gate_provider_account_def gpad  on gpa.def_id =gpad.id
				where gmpam.deleteaction_id is null and gpa.deleteaction_id is null and gpd.active =true