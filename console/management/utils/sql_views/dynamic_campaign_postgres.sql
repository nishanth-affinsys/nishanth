DO $$
DECLARE
    tenantName RECORD;
    schemaName_analytics VARCHAR(255);
    schemaName_profile VARCHAR(255);
    schemaName_campaign VARCHAR(255);
    dbSchema_analytics VARCHAR(255) := '${DB_SCHEMA_analytics}';
    dbSchema_campaign VARCHAR(255) := '${DB_SCHEMA_campaign}';
    dbSchema_profile VARCHAR(255) := '${DB_SCHEMA_profile}';
    sqlQuery TEXT;
    schema_exists_analytics BOOLEAN;
    schema_exists_campaign BOOLEAN;
    schema_exists_profile BOOLEAN;
BEGIN
    FOR tenantName IN select tenant from botbuilder.botbuilder_project where is_active = true
    LOOP
        IF tenantName.tenant = 'default' THEN
            CONTINUE;
        end if;

        schemaName_analytics := dbSchema_analytics || '_' || tenantName.tenant;
        schemaName_campaign := dbSchema_campaign || '_' || tenantName.tenant;
        schemaName_profile := dbSchema_profile || '_' || tenantName.tenant;

        SELECT EXISTS (
        SELECT 1
        FROM information_schema.schemata
        WHERE schema_name = schemaName_analytics
        ) INTO schema_exists_analytics;

        SELECT EXISTS (
            SELECT 1
            FROM information_schema.schemata
            WHERE schema_name = schemaName_campaign
        ) INTO schema_exists_campaign;

        SELECT EXISTS (
            SELECT 1
            FROM information_schema.schemata
            WHERE schema_name = schemaName_profile
        ) INTO schema_exists_profile;

        IF schema_exists_analytics AND schema_exists_campaign AND schema_exists_profile THEN
            sqlQuery := '
                drop view if exists ' || schemaName_analytics || '.campaign_notification cascade;

                CREATE OR REPLACE VIEW ' || schemaName_analytics || '.campaign_notification AS
                WITH campaign_data AS (
                SELECT
                        sru.campaign_id AS campaign_filter_id,
                        c.campaign_id AS campaign_id,
                        c.campaign_name AS campaign_name,
                        c.created_timestamp,
                        c.last_modified,
                        scd.identifier AS sub_campaign_identifier,
                        scd.name AS sub_campaign_name,
                        sru.run_id AS run_id,
                        sru.notification_id AS notification_id
                    FROM
                         ' || schemaName_campaign || '.sub_campaign_run sru
                    JOIN
                         ' || schemaName_campaign || '.sub_campaign_detail scd ON sru.sub_campaign_id = scd.id
                    JOIN
                         ' || schemaName_campaign || '.campaign c ON sru.campaign_id = c.id
                ),
                notification_data AS (
                select
                    nd.batch_id,
                    bi.identifier as batch_identifier,
                    bi.channel_id ,
                    bi.channel_name,
                    nd.tenant,
                    nd.message_id_id as message_id,
                    nd.status as notification_status,
                    nd.timestamp as notification_timestamp,
                    cd.profile_id,
                    p.user_name
                from
                      ' || schemaName_profile || '.notification_data nd
                join
                      ' || schemaName_profile || '.batch_identifier bi on nd.batch_id = bi.id
                join
                      ' || schemaName_profile || '.campaign_data cd on cd.batch_id = bi.id and cd.tenant=nd.tenant
                join
                      ' || schemaName_profile || '.profile p on p.profile_id = cd.profile_id and p.tenant = cd.tenant
                ),
                notification_sunshine_mapped AS (
                    SELECT
                        nd.batch_id,
                        nd.batch_identifier,
                        nd.channel_name,
                        nd.tenant,
                        nd.message_id,
                        nd.notification_status,
                        nd.notification_timestamp,
                        nd.profile_id,
                        nd.user_name,
                        nd.channel_id as initial_channel_id,
                        CASE
                            WHEN nd.channel_name = ''whatsapps'' AND sm.mobile_number IS NOT NULL THEN sm.conversation_id
                            ELSE nd.channel_id
                        END AS channel_id
                    FROM
                        notification_data nd
                    LEFT JOIN
                        ' || schemaName_analytics || '.sunshine_mapping sm ON nd.tenant = sm.tenant AND nd.channel_id = sm.mobile_number
                ),
                campaign_notification AS (
                    SELECT
                        cd.campaign_filter_id,
                        cd.campaign_id,
                        cd.campaign_name,
                        cd.sub_campaign_identifier,
                        cd.sub_campaign_name,
                        cd.run_id,
                        cd.created_timestamp,
                        cd.last_modified,
                        nsm.batch_id,
                        nsm.batch_identifier,
                        nsm.channel_id,
                        nsm.initial_channel_id,
                        nsm.channel_name,
                        nsm.message_id,
                        nsm.tenant,
                        nsm.notification_status,
                        nsm.user_name as profile_name,
                        Case when nsm.notification_status <> ''Failure'' then ''sent'' else null end as status,
                        Case when ms.timestamp is not null then ms.timestamp else nsm.notification_timestamp end as message_timestamp,
                        nsm.notification_timestamp
                    FROM
                        campaign_data cd
                    JOIN
                        notification_sunshine_mapped nsm ON cd.notification_id = nsm.batch_identifier
                    LEFT OUTER JOIN
                        ' || schemaName_analytics || '.message_status ms ON nsm.tenant = ms.tenant AND nsm.message_id = ms.message_id and ms.status = ''sent''
                    UNION
                    SELECT
                        cd.campaign_filter_id,
                        cd.campaign_id,
                        cd.campaign_name,
                        cd.sub_campaign_identifier,
                        cd.sub_campaign_name,
                        cd.run_id,
                        cd.created_timestamp,
                        cd.last_modified,
                        nsm.batch_id,
                        nsm.batch_identifier,
                        nsm.channel_id,
                        nsm.initial_channel_id,
                        nsm.channel_name,
                        nsm.message_id,
                        nsm.tenant,
                        nsm.notification_status,
                        nsm.user_name as profile_name,
                        ms.status,
                        Case when ms.timestamp is not null then ms.timestamp else nsm.notification_timestamp end as message_timestamp,
                        nsm.notification_timestamp
                    FROM
                        campaign_data cd
                    JOIN
                        notification_sunshine_mapped nsm ON cd.notification_id = nsm.batch_identifier
                    JOIN
                        ' || schemaName_analytics || '.message_status ms ON nsm.tenant = ms.tenant AND nsm.message_id = ms.message_id and ms.status in (''read'',''delivered'')
                )
                select  ROW_NUMBER() OVER () AS id, * from campaign_notification;
                ';
                RAISE NOTICE 'Query: %',schemaName_analytics;
                EXECUTE sqlQuery;
            else
                continue;
            end if;


    END LOOP;
END
$$;
