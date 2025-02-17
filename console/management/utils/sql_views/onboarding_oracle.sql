CREATE OR REPLACE VIEW ${DB_SCHEMA_onboarding}.detailed_report_table_rt AS
SELECT
    t1.external_reference,
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
        THEN CAST(t2.ACTION_PERFORMED_BY AS VARCHAR2(50 CHAR))
        ELSE ' '
    END AS "ACTION_PERFORMED_BY",
    CASE
    WHEN t1.INTERNAL_REFERENCE = t2.INTERNAL_REFERENCE
         AND t1.VERSION_NO = t2.VERSION_NO
         AND t2.EVENT_NAME = 'VERIFY'
    THEN t2.ACTION_PERFORM_TIMESTAMP
    ELSE NULL
    END AS "ACTION_PERFORM_TIMESTAMP"
FROM
    ${DB_SCHEMA_onboarding}.SINGLE_CIF_RETAIL_DATA t1
LEFT JOIN
    ${DB_SCHEMA_onboarding}.RT_APPLICATION_LOG t2
ON
    t1.INTERNAL_REFERENCE = t2.INTERNAL_REFERENCE
    AND t1.VERSION_NO = t2.VERSION_NO
    AND t1.TENANT = t2.TENANT AND t2.EVENT_NAME = 'VERIFY';

CREATE OR REPLACE VIEW ${DB_SCHEMA_onboarding}.detailed_report_table_sp AS
SELECT
    t1.external_reference,
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
    t1.ONBOARDING_CHANNEL,
    t1.tenant,
    t1.customer_type,
    t2.internal_reference,
    t2.version_no,
    t2.event_name,
    CASE
        WHEN t1.INTERNAL_REFERENCE = t2.INTERNAL_REFERENCE
             AND t1.VERSION_NO = t2.VERSION_NO
             AND t2.EVENT_NAME = 'VERIFY'
        THEN CAST(t2.ACTION_PERFORMED_BY AS VARCHAR2(50 CHAR))
        ELSE ' '
    END AS "ACTION_PERFORMED_BY",
    CASE
    WHEN t1.INTERNAL_REFERENCE = t2.INTERNAL_REFERENCE
         AND t1.VERSION_NO = t2.VERSION_NO
         AND t2.EVENT_NAME = 'VERIFY'
    THEN t2.ACTION_PERFORM_TIMESTAMP
    ELSE NULL
    END AS "ACTION_PERFORM_TIMESTAMP"
FROM
    ${DB_SCHEMA_onboarding}.SINGLE_CIF_SP_DATA t1
LEFT JOIN
    ${DB_SCHEMA_onboarding}.SP_APPLICATION_LOG t2
ON
    t1.INTERNAL_REFERENCE = t2.INTERNAL_REFERENCE
    AND t1.VERSION_NO = t2.VERSION_NO
    AND t1.TENANT = t2.TENANT AND t2.EVENT_NAME = 'VERIFY'