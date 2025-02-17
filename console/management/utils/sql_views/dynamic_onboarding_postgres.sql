DO $$
DECLARE
    tenantName RECORD;
    schemaName VARCHAR(255);
    sqlQuery TEXT;
    dbSchema VARCHAR(255) := '${DB_SCHEMA_onboarding}';
    schema_exists boolean;
BEGIN
    FOR tenantName IN select tenant from botbuilder.botbuilder_project where is_active = true
    LOOP

        IF tenantName.tenant = 'default' THEN
            CONTINUE;
        end if;

        schemaName := dbSchema || '_' || tenantName.tenant;

        SELECT EXISTS (
        SELECT schema_name
        FROM information_schema.schemata
        WHERE schema_name = schemaName
        ) INTO schema_exists;

        IF schema_exists THEN

            sqlQuery := 'drop view if exists ' || schemaName || '.detailed_report_table_rt cascade;
                CREATE OR REPLACE VIEW ' || schemaName || '.detailed_report_table_rt AS
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
                             AND t2.EVENT_NAME = ''VERIFY''
                        THEN CAST(t2.ACTION_PERFORMED_BY AS VARCHAR(50))
                        ELSE '' ''
                    END AS "action_performed_by",
                    CASE
                        WHEN t1.INTERNAL_REFERENCE = t2.INTERNAL_REFERENCE
                             AND t1.VERSION_NO = t2.VERSION_NO
                             AND t2.EVENT_NAME = ''VERIFY''
                        THEN t2.ACTION_PERFORM_TIMESTAMP
                        ELSE NULL
                    END AS "action_perform_timestamp"
                FROM
                    ' || schemaName || '.single_cif_retail_data t1
                LEFT JOIN
                    ' || schemaName || '.rt_application_log t2
                ON
                    t1.INTERNAL_REFERENCE = t2.INTERNAL_REFERENCE
                    AND t1.VERSION_NO = t2.VERSION_NO
                    AND t1.TENANT = t2.TENANT
                    AND t2.EVENT_NAME = ''VERIFY'';


                drop view if exists ' || schemaName || '.detailed_report_table_sp cascade;

                CREATE OR REPLACE VIEW ' || schemaName || '.detailed_report_table_sp AS
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
                    t1.onboarding_channel, -- Updated column name to lowercase
                    t1.tenant,
                    t1.customer_type,
                    t2.internal_reference,
                    t2.version_no,
                    t2.event_name,
                    CASE
                        WHEN t1.internal_reference = t2.internal_reference
                             AND t1.version_no = t2.version_no
                             AND t2.event_name = ''VERIFY''
                        THEN CAST(t2.action_performed_by AS VARCHAR)
                        ELSE '' ''
                    END AS action_performed_by,
                    CASE
                    WHEN t1.internal_reference = t2.internal_reference
                         AND t1.version_no = t2.version_no
                         AND t2.event_name = ''VERIFY''
                    THEN t2.action_perform_timestamp
                    ELSE NULL
                    END AS action_perform_timestamp
                FROM
                    ' || schemaName || '.single_cif_sp_data t1
                LEFT JOIN
                    ' || schemaName || '.sp_application_log t2
                ON
                    t1.internal_reference = t2.internal_reference
                    AND t1.version_no = t2.version_no
                    AND t1.tenant = t2.tenant AND t2.event_name = ''VERIFY'';';

            EXECUTE sqlQuery;
        else
            continue;
        end if;
    END LOOP;
END
$$;