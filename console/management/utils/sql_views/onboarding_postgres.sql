drop view if exists ${DB_SCHEMA_onboarding}.detailed_report_table_rt cascade;
CREATE OR REPLACE VIEW ${DB_SCHEMA_onboarding}.detailed_report_table_rt AS
SELECT t1.external_reference,
       t1.product_name,
       t1.first_name,
       t1.middle_name,
       t1.last_name,
       t1.primary_contact_number,
       t1.created_by,
       t1.create_timestamp,
       t1.last_modified_by,
       t1.last_modified_timestamp,
       t1.submit_by,
       t1.ONBOARDING_CHANNEL,
       t1.submit_timestamp,
       t1.account_num1,
       t1.account_num2,
       t1.created_at_branch_code,
       t1.present_at_branch_code,
       t1.queue_name,
       t1.tenant,
       t1.customer_type,
       t2.internal_reference,
       t2.version_no,
       t2.event_name,
       CASE
           WHEN t1.INTERNAL_REFERENCE = t2.INTERNAL_REFERENCE
               AND t1.VERSION_NO = t2.VERSION_NO
               AND t2.EVENT_NAME = 'VERIFY'
               THEN CAST(t2.ACTION_PERFORMED_BY AS VARCHAR(50))
           ELSE ' '
           END AS "action_performed_by",
       CASE
           WHEN t1.INTERNAL_REFERENCE = t2.INTERNAL_REFERENCE
               AND t1.VERSION_NO = t2.VERSION_NO
               AND t2.EVENT_NAME = 'VERIFY'
               THEN t2.ACTION_PERFORM_TIMESTAMP
           ELSE NULL
           END AS "action_perform_timestamp"
FROM ${DB_SCHEMA_onboarding}.single_cif_retail_data t1
         LEFT JOIN
     ${DB_SCHEMA_onboarding}.rt_application_log t2
     ON
         t1.INTERNAL_REFERENCE = t2.INTERNAL_REFERENCE
             AND t1.VERSION_NO = t2.VERSION_NO
             AND t1.TENANT = t2.TENANT
             AND t2.EVENT_NAME = 'VERIFY';


drop view if exists ${DB_SCHEMA_onboarding}.detailed_report_table_sp cascade;

CREATE OR REPLACE VIEW ${DB_SCHEMA_onboarding}.detailed_report_table_sp AS
SELECT t1.external_reference,
       t1.product_name,
       t1.business_name,
       t1.primary_contact_number,
       t1.created_by,
       t1.create_timestamp,
       t1.last_modified_by,
       t1.last_modified_timestamp,
       t1.submit_by,
       t1.submit_timestamp,
       t1.account_num1,
       t1.account_num2,
       t1.created_at_branch_code,
       t1.present_at_branch_code,
       t1.queue_name,
       t1.onboarding_channel, -- Updated column name to lowercase
       t1.tenant,
       t1.customer_type,
       t2.internal_reference,
       t2.version_no,
       t2.event_name,
       CASE
           WHEN t1.internal_reference = t2.internal_reference
               AND t1.version_no = t2.version_no
               AND t2.event_name = 'VERIFY'
               THEN CAST(t2.action_performed_by AS VARCHAR)
           ELSE ' '
           END AS action_performed_by,
       CASE
           WHEN t1.internal_reference = t2.internal_reference
               AND t1.version_no = t2.version_no
               AND t2.event_name = 'VERIFY'
               THEN t2.action_perform_timestamp
           ELSE NULL
           END AS action_perform_timestamp
FROM ${DB_SCHEMA_onboarding}.single_cif_sp_data t1
         LEFT JOIN
     ${DB_SCHEMA_onboarding}.sp_application_log t2
     ON
         t1.internal_reference = t2.internal_reference
             AND t1.version_no = t2.version_no
             AND t1.tenant = t2.tenant AND t2.event_name = 'VERIFY';

drop view if exists ${DB_SCHEMA_analytics}.onboarding_retail_comments cascade;
CREATE OR REPLACE VIEW ${DB_SCHEMA_analytics}.onboarding_retail_comments AS
SELECT ROW_NUMBER() OVER () AS id,
       s.internal_reference,
       s.product_name,
       s.primary_contact_number,
       s.created_by,
       s.create_timestamp,
       s.last_modified_by,
       s.last_modified_timestamp,
       s.last_action_performed_by,
       s.last_action_perform_timestamp,
       s.submit_by,
       s.submit_timestamp,
       s.account_num1,
       s.account_num2,
       s.created_at_branch_code,
       s.present_at_branch_code,
       s.application_status,
       s.customer_type,
       s.queue_name,
       s.tenant,
       a.action_code,
       a.comments
FROM ${DB_SCHEMA_onboarding}.single_cif_retail_data s
         LEFT JOIN
     ${DB_SCHEMA_onboarding}.rt_audit_comments a
     ON
         s.internal_reference = a.internal_reference
             AND s.version_no = a.version_no;

drop view if exists ${DB_SCHEMA_analytics}.kyc_account_opening_details cascade;
CREATE OR REPLACE VIEW ${DB_SCHEMA_analytics}.kyc_account_opening_details AS
SELECT ROW_NUMBER() OVER ()                                         AS id,
       kyc_master.internal_reference                                as "kyc_reference",
       single_cif_retail_data.internal_reference                    as "application_reference_number",
       kyc_master.primary_contact_number,
       kyc_master.primary_email_address,
       kyc_master.first_name,
       kyc_master.last_name,
       kyc_master.queue_name                                        as "kyc_state",
       kyc_master.tenant,
       COALESCE(single_cif_retail_data.queue_name, 'Not Available') as "account_opening_status",
       kyc_master.create_timestamp,
       kyc_master.last_modified_timestamp
FROM ${DB_SCHEMA_kyc}.kyc_master AS kyc_master
         LEFT JOIN
     ${DB_SCHEMA_onboarding}.single_cif_retail_data AS single_cif_retail_data
     ON
         kyc_master.internal_reference = single_cif_retail_data.kyc_reference
             AND
         single_cif_retail_data.queue_code IN
         ('QDAYTWOREMEDIATED', 'QDAYTWOPASS', 'QDAYTWOFAIL', 'QBANKINGASSURANCE', 'QDAYTWOREJECT', 'QSUCCESS')
         INNER JOIN (SELECT internal_reference, MAX(version_no) AS max_version_no
                     FROM ${DB_SCHEMA_kyc}.kyc_master
                     GROUP BY internal_reference) AS latest_kyc
                    ON kyc_master.internal_reference = latest_kyc.internal_reference
                        AND kyc_master.version_no = latest_kyc.max_version_no
WHERE kyc_master.queue_code = 'QSUCCESS';

drop view if exists ${DB_SCHEMA_analytics}.kyc_applications_details cascade;
CREATE OR REPLACE VIEW ${DB_SCHEMA_analytics}.kyc_applications_details AS
SELECT ROW_NUMBER() OVER ()                                          AS id,
       km.internal_reference,
       km.kyc_number,
       CONCAT(km.first_name, ' ', km.middle_name, ' ', km.last_name) AS customer_name,
       km.product_name,
       km.primary_contact_number,
       km.created_by,
       km.create_timestamp,
       km.last_action_performed_by,
       km.last_action_perform_timestamp,
       km.customer_type,
       km.channel,
       km.queue_code,
       km.queue_name,
       km.submit_by,
       km.submit_timestamp,
       km.rejected_by,
       km.rejected_timestamp,
       km.last_modified_by,
       km.last_modified_timestamp,
       km.tenant,
       kac.action_code,
       kac.comments
FROM ${DB_SCHEMA_kyc}.kyc_master km
         LEFT JOIN
     ${DB_SCHEMA_kyc}.kyc_audit_comments kac
     ON
         km.internal_reference = kac.internal_reference
             AND
         km.version_no = kac.version_no
WHERE km.display_in_queue = 'Y'
ORDER BY km.last_modified_timestamp DESC;

drop view if exists ${DB_SCHEMA_analytics}.onboarding_audit_details cascade;
CREATE OR REPLACE VIEW ${DB_SCHEMA_analytics}.onboarding_audit_details AS
WITH latest_kyc AS (SELECT km.internal_reference, MAX(km.version_no) AS version_no
                    FROM ${DB_SCHEMA_kyc}.kyc_master km
                             JOIN ${DB_SCHEMA_onboarding}.single_cif_retail_data scd
                                  ON km.internal_reference = scd.kyc_reference
                    WHERE km.display_in_queue = 'Y'
                    GROUP BY km.internal_reference),
     kyc_data AS (SELECT DISTINCT scd.internal_reference             AS single_cifrt_internal_reference,
                                  kal.event_name                     AS event,
                                  kal.internal_reference             as kyc_reference,
                                  kal.action_performed_by            AS action_by,
                                  kal.action_perform_timestamp       AS action_perform_timestamp,
                                  kac.comments                       AS comments,
                                  kal.tenant                         as tenant,
                                  ROW_NUMBER()
                                  OVER (PARTITION BY scd.internal_reference, kal.action_performed_by, kal.action_perform_timestamp,kal.internal_reference
                                      ORDER BY kac.create_timestamp) AS rn
                  FROM ${DB_SCHEMA_kyc}.kyc_application_log kal
                           JOIN latest_kyc lk
                                ON kal.internal_reference = lk.internal_reference
                                    AND kal.version_no = lk.version_no
                           JOIN ${DB_SCHEMA_onboarding}.single_cif_retail_data scd
                                ON scd.kyc_reference = lk.internal_reference
                           LEFT JOIN ${DB_SCHEMA_kyc}.kyc_audit_comments kac
                                     ON kal.internal_reference = kac.internal_reference
                                         AND kal.version_no = kac.version_no
                                         AND kal.action_performed_by_uuid =
                                             kac.created_by_uuid),
     onboarding_data AS (SELECT DISTINCT scd.internal_reference       AS single_cifrt_internal_reference,
                                         ral.event_name               AS event,
                                         ral.action_performed_by      AS action_by,
                                         ral.action_perform_timestamp AS action_perform_timestamp,
                                         rac.comments                 AS comments,
                                         scd.kyc_reference            as kyc_reference,
                                         scd.tenant                   as tenant,
                                         ROW_NUMBER() OVER (
                                             PARTITION BY scd.internal_reference, ral.event_name, ral.action_performed_by, ral.action_perform_timestamp
                                             ORDER BY ABS(EXTRACT(EPOCH FROM
                                                                  (ral.action_perform_timestamp - rac.create_timestamp))) ASC
                                             )                        AS rn
                         FROM ${DB_SCHEMA_onboarding}.rt_application_log ral
                                  JOIN ${DB_SCHEMA_onboarding}.single_cif_retail_data scd
                                       ON ral.internal_reference = scd.internal_reference
                                  LEFT JOIN ${DB_SCHEMA_onboarding}.rt_audit_comments rac
                                            ON ral.internal_reference = rac.internal_reference
                                                AND ral.version_no = rac.version_no
                                                AND ral.action_performed_by_uuid = rac.created_by_uuid)
SELECT ROW_NUMBER() OVER (ORDER BY action_perform_timestamp) AS id,
       single_cifrt_internal_reference,
       event,
       action_by,
       action_perform_timestamp,
       comments,
       kyc_reference,
       tenant
FROM (SELECT DISTINCT single_cifrt_internal_reference,
                      event,
                      action_by,
                      action_perform_timestamp,
                      comments,
                      kyc_reference,
                      tenant
      FROM kyc_data
      WHERE single_cifrt_internal_reference IS NOT NULL
        AND single_cifrt_internal_reference != ''
        AND rn = 1
      UNION ALL
      SELECT DISTINCT single_cifrt_internal_reference,
                      event,
                      action_by,
                      action_perform_timestamp,
                      comments,
                      kyc_reference,
                      tenant
      FROM onboarding_data
      WHERE single_cifrt_internal_reference IS NOT NULL
        AND single_cifrt_internal_reference != ''
        AND rn = 1) AS combined_data;



