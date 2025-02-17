DO $$
DECLARE
    tenantName RECORD;
    schemaName VARCHAR(255);
    schemaName_etbprovider VARCHAR(255);
    sqlQuery_userflow TEXT;
    sqlQuery_latest_registration_activity TEXT;
    sqlQuery_net_registration_activity TEXT;
    sqlQuery_campaign_rolled TEXT;
    sqlQuery_recent_ticket_activity TEXT;
    sqlQuery_etb_user_details TEXT;
    dbSchema VARCHAR(255) := '${DB_SCHEMA_analytics}';
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

            sqlQuery_userflow := '
                DROP VIEW IF EXISTS ' || schemaName || '.user_flow CASCADE;
                CREATE OR REPLACE VIEW ' || schemaName || '.user_flow AS
                SELECT ROW_NUMBER() OVER () AS id, shankyModel.*
                FROM (
                    SELECT first_six_messages.channel_id,
                        LAG(first_six_messages.intent, 1) OVER (PARTITION BY channel_id ORDER BY timestamp) AS source,
                        first_six_messages.intent AS target,
                        first_six_messages.channel,
                        first_six_messages.timestamp,
                        first_six_messages.tenant,
                        first_six_messages.rank
                    FROM (
                        SELECT ' || schemaName || '.message_log.intent,
                            ' || schemaName || '.message_log.channel_id,
                            ' || schemaName || '.message_log.channel,
                            ' || schemaName || '.message_log.timestamp,
                            ' || schemaName || '.message_log.tenant,
                            ROW_NUMBER() OVER (PARTITION BY channel_id, date(timestamp), tenant ORDER BY timestamp ASC) AS rank
                        FROM ' || schemaName || '.message_log
                        WHERE source = ''user'' AND intent IS NOT NULL AND intent != ''fallback''
                    ) AS first_six_messages
                    WHERE rank <= 3
                ) AS shankyModel;
            ';
            EXECUTE sqlQuery_userflow;

            sqlQuery_latest_registration_activity := '
            DROP VIEW IF EXISTS ' || schemaName || '.latest_registration_activity CASCADE;
            CREATE OR REPLACE VIEW ' || schemaName || '.latest_registration_activity AS
            SELECT ROW_NUMBER() OVER () AS id,
                   t.mobile_number,
                   t.timestamp,
                   t.action AS registered,
                   t.tenant
            FROM ' || schemaName || '.stage_log_auth t
                     INNER JOIN
                 (SELECT mobile_number,
                         MAX(timestamp) AS MaxDate
                  FROM ' || schemaName || '.stage_log_auth
                  WHERE action IN (''deregister'', ''register'')
                    AND result = ''successful''
                  GROUP BY mobile_number) tm ON t.mobile_number = tm.mobile_number
                     AND t.timestamp = tm.MaxDate;
                ';
            EXECUTE sqlQuery_latest_registration_activity;
            sqlQuery_net_registration_activity :=
            'drop view if exists ' || schemaName || '.net_registration_activity cascade;

            create or replace view ' || schemaName || '.net_registration_activity as
            select ROW_NUMBER() OVER () as id,
                   t.mobile_number,
                   t.date,
                   t1.action,
                   t1.tenant
            from (
                     (select mobile_number,
                             date(timestamp + interval ''180 minutes'') as date,
                             MAX(timestamp)                           as maxdate
                      from ' || schemaName || '.stage_log_auth
                      where action in (''deregister'', ''register'')
                        and result = ''successful''
                      group by mobile_number, date) t
                         inner join
                         (SELECT mobile_number,
                                 action,
                                 tenant,
                                 date(timestamp + interval ''180 minutes'') as date,
                                 MAX(timestamp)                           as maxdate
                          from ' || schemaName || '.stage_log_auth
                          where action in (''deregister'', ''register'')
                            and result = ''successful''
                          group by mobile_number, date, action, tenant) t1 on t.mobile_number = t1.mobile_number
                         and t1.maxdate = t.maxdate);';

            EXECUTE sqlQuery_net_registration_activity;
            sqlQuery_campaign_rolled := 'drop view if exists ' || schemaName || '.campaign_rolled;
            CREATE VIEW ' || schemaName || '.campaign_rolled AS
            SELECT ROW_NUMBER() OVER () AS id,
                   channel_id,
                   channel,
                   intent               AS batch_identifier,
                   message,
                   timestamp,
                   tenant
            FROM ' || schemaName || '.message_log
            WHERE source = ''campaign'';';

            EXECUTE sqlQuery_campaign_rolled;
            sqlQuery_recent_ticket_activity := 'drop view if exists ' || schemaName || '.recent_ticket_activity cascade;
            create or replace view ' || schemaName || '.recent_ticket_activity as
            SELECT ROW_NUMBER() OVER () as id, *
            from (SELECT DISTINCT on (srn) srn,
                                           last_updated_time,
                                           status,
                                           priority,
                                           source,
                                           category_name,
                                           user_name,
                                           tenant,
                                           hold_time,
                                           created_timestamp,
                                           breached_status
                  from ' || schemaName || '.complaint_ticket_logs
                  ORDER by srn, last_updated_time DESC) as t;';

            EXECUTE sqlQuery_recent_ticket_activity;

            EXECUTE format('
            DROP FUNCTION IF EXISTS %I.get_session_end(character varying, timestamp with time zone, character varying, timestamp with time zone) CASCADE;

            CREATE OR REPLACE FUNCTION %I.get_session_end(estimated_id character varying,
                                                            estimated_t timestamp with time zone,
                                                            channel_id character varying,
                                                            log_t timestamp with time zone) RETURNS BOOLEAN
            LANGUAGE plpgsql AS $function$
            BEGIN
                IF estimated_id = channel_id AND log_t > estimated_t THEN
                    RETURN TRUE;
                ELSIF estimated_id = channel_id THEN
                    RETURN FALSE;
                ELSE
                    RETURN TRUE;
                END IF;
            END;
            $function$',
            schemaName, schemaName);

        EXECUTE format('
            DROP FUNCTION IF EXISTS %I.get_table() CASCADE;

            CREATE OR REPLACE FUNCTION %I.get_table()
                RETURNS TABLE
                        (
                            channel_id VARCHAR,
                            log_T      timestamp with time zone,
                            session_T  timestamp with time zone
                        )
            AS
            $function$
            DECLARE
                rec          record;
                estimated_T  timestamp with time zone := ''2001-01-01T00:00:00+00:00'';
                estimated_id VARCHAR := '''';
            BEGIN
                FOR rec IN SELECT channel_id, timestamp FROM %I.message_log ORDER BY channel_id, timestamp
                LOOP
                    IF %I.get_session_end(estimated_id::VARCHAR, estimated_T::timestamp with time zone,
                                           rec.channel_id::VARCHAR,
                                           rec.timestamp::timestamp with time zone) = TRUE
                    THEN
                        estimated_T := rec.timestamp + interval ''24 hours'';
                        estimated_id := rec.channel_id;
                        RETURN QUERY SELECT estimated_id AS channel_id, rec.timestamp AS log_T, estimated_T AS session_T;
                    ELSE
                        RETURN QUERY SELECT estimated_id AS channel_id, rec.timestamp AS log_T, estimated_T AS session_T;
                    END IF;
                END LOOP;
            END;
            $function$ language plpgsql;',
            schemaName, schemaName, schemaName, schemaName);
        ELSE
            continue;
        END IF;
    END LOOP;
END
$$;
