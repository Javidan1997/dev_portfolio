-- =========================================
-- PURCHASE VIA CARD (with amounts and commissions)
-- =========================================
SELECT 
qiwi_pay_data.payment_id                            AS payment_id,
       topup_process.topup_process_amount                  AS total_amount,
       topup_process.topup_process_commission              AS topup_commission,
       purchase_process.purchase_process_commission        AS purchase_commission,
       purchase_process.purchase_process_amount            AS purchase_amount,
       tbbd.status                                         AS business_process_status,
       topup_tx.topup_status                               AS topup_gate_tx_status,
       purchase_tx.purchase_status                         AS purchase_gate_tx_status,
       purchase_business_process_data.purchase_error_descr AS error_description,
       tbb.id                                              AS business_process_id,
       user_data.login                                     AS login,
       NULL                                                AS coin_serial,
       pt.card_mask_data                                   AS pan,
       ha.performedat                                      AS data
FROM tx_purchase_via_gate tpvg
         JOIN tx_business_base tbb ON tpvg.id = tbb.id
         JOIN tx_business_base_def tbbd ON tbb.def_id = tbbd.id
         JOIN history_action ha ON tbb.creationaction_id = ha.id
         JOIN gate_tx_purchase_via_gate gtpvg ON tpvg.id = gtpvg.process_id
         JOIN gate_product_purchase gpp ON tpvg.purchase_id = gpp.id
         JOIN payment_tool pt ON gpp.id = pt.purchase_id
         JOIN (SELECT gt.id         AS topup_id,
                      gtd.status    AS topup_status,
                      gt.coin_id    AS topup_tx_coin_id,
                      gt.process_id AS process_id
               FROM gate_tx gt
                        JOIN gate_tx_def gtd ON gt.def_id = gtd.id) AS topup_tx
              ON gtpvg.tx_id = topup_tx.topup_id
         JOIN (SELECT tbg.id         AS topup_process_id,
                      tbg.amount     AS topup_process_amount,
                      tbg.commission AS topup_process_commission
               FROM tx_business_gate tbg) AS topup_process
              ON topup_tx.process_id = topup_process.topup_process_id
         JOIN (SELECT gt.id         AS purchase_id,
                      gtd.status    AS purchase_status,
                      gt.coin_id    AS purchase_tx_coin_id,
                      gt.process_id AS process_id
               FROM gate_tx gt
                        JOIN gate_tx_def gtd ON gt.def_id = gtd.id) AS purchase_tx
              ON gpp.tx_id = purchase_tx.purchase_id
         JOIN (SELECT tbg.id         AS purchase_process_id,
                      tbg.amount     AS purchase_process_amount,
                      tbg.commission AS purchase_process_commission
               FROM tx_business_gate tbg) AS purchase_process
              ON purchase_tx.process_id = purchase_process.purchase_process_id
         JOIN (SELECT tbb.id           AS purchase_process_id,
                      tbbd.error_descr AS purchase_error_descr
               FROM tx_business_base tbb
                        JOIN tx_business_base_def tbbd ON tbb.def_id = tbbd.id) AS purchase_business_process_data
              ON purchase_tx.process_id = purchase_business_process_data.purchase_process_id
         JOIN (SELECT ec.id     AS user_coin_id,
                      ec.serial AS user_coin_serial
               FROM emitent_coin ec) AS user_coin_data
              ON topup_tx.topup_tx_coin_id = user_coin_data.user_coin_id
         JOIN (SELECT gproduct.id          AS product_id,
                      gproduct.external_id AS product_external_id,
                      eqp.payment_id       AS payment_id,
                      eqpd.qiwipay_extras  AS extras
               FROM emanat_qiwi_pay eqp
                        JOIN emanat_qiwi_pay_def eqpd ON eqp.id = eqpd.qiwipaydata_id
                        JOIN gate_product gproduct ON eqp.product_id = gproduct.id) AS qiwi_pay_data
              ON SUBSTRING(tpvg.payer_data, '(?<="name":"paymentId".*"value":")(.*?)(?=\s*")') =
                 qiwi_pay_data.payment_id
         JOIN (SELECT ec.id     AS emitent_coin_id,
                      uul.value AS login
               FROM emitent_coin ec
                        JOIN org_organization oo ON ec.organization_id = oo.id
                        JOIN org_organization_def ood ON oo.def_id = ood.id
                        JOIN org_prof_profile opp ON oo.profile_id = opp.id
                        JOIN user_user uu ON opp.id = uu.profile_id
                        JOIN user_user_login uul ON uu.id = uul.user_id) AS user_data
              ON purchase_tx.purchase_tx_coin_id = user_data.emitent_coin_id
--WHERE  ha.performedat >'2021-01-17' and ha.performedat <'2021-01-18'
--and qiwi_pay_data.payment_id ='1000247304'	
