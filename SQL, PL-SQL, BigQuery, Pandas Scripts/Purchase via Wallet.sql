-- =========================================
-- PURCHASE VIA WALLET (with amount and commission)
-- =========================================
SELECT gt.type,
SUBSTRING(gt.payer_data, '(?<="name":"paymentId".*"value":")(.*?)(?=\s*")') AS payment_id,
SUBSTRING(gt.payer_data, '(?<="name":"account".*"value":")(.*?)(?=\s*")') AS account,
       COALESCE(purchase_process.purchase_process_amount, 0) +
       COALESCE(purchase_process.purchase_process_commission, 0)                   AS total_amount,
       NULL                                                                        AS without_topup_commission,
       purchase_process.purchase_process_commission                                AS purchase_commission,
       purchase_process.purchase_process_amount                                    AS purchase_amount,
       tbbd.status                                                                 AS business_process_status,
       NULL                                                                        AS without_topup_part,
       gtd.status                                                                  AS purchase_status,
       tbbd.error_descr                                                            AS error_description,
       tbb.id                                                                      AS purchase_process_id,
       user_data.login                                                             AS login,
       ec.serial                                                                   AS coin_serial,
      -- NULL                                                                        AS pan,
       ha.performedat                                                              AS data,
product_external_id 
FROM gate_tx gt
         JOIN gate_tx_def gtd ON gt.def_id = gtd.id
         JOIN tx_business_base tbb ON gt.process_id = tbb.id
         JOIN tx_business_base_def tbbd ON tbb.def_id = tbbd.id
         JOIN history_action ha ON tbb.creationaction_id = ha.id
         JOIN (SELECT ec.id     AS emitent_coin_id,
                      uul.value AS login
               FROM emitent_coin ec
                        JOIN org_organization oo ON ec.organization_id = oo.id
                        JOIN org_organization_def ood ON oo.def_id = ood.id
                        JOIN org_prof_profile opp ON oo.profile_id = opp.id
                        JOIN user_user uu ON opp.id = uu.profile_id
                        JOIN user_user_login uul ON uu.id = uul.user_id) AS user_data
              ON gt.coin_id = user_data.emitent_coin_id
         JOIN emitent_coin ec ON gt.coin_id = ec.id
         JOIN (SELECT gproduct.id          AS product_id,
                      gproduct.external_id AS product_external_id,
                      eqp.payment_id       AS payment_id,
                      eqpd.qiwipay_extras  AS extras
               FROM emanat_qiwi_pay eqp
                        JOIN emanat_qiwi_pay_def eqpd ON eqp.id = eqpd.qiwipaydata_id
                        JOIN gate_product gproduct ON eqp.product_id = gproduct.id) AS qiwi_pay_data
              ON SUBSTRING(gt.payer_data, '(?<="name":"paymentId".*"value":")(.*?)(?=\s*")') = qiwi_pay_data.payment_id
         JOIN (SELECT tbg.id         AS purchase_process_id,
                      tbg.amount     AS purchase_process_amount,
                      tbg.commission AS purchase_process_commission
               FROM tx_business_gate tbg) AS purchase_process
              ON tbb.id = purchase_process.purchase_process_id
WHERE --gt.type != 'PURCHASE'
 ha.performedat >'2020-11-30' and ha.performedat <'2020-12-06'
and gtd.status='SUCCESS'
