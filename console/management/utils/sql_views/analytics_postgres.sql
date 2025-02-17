drop view if exists ${DB_SCHEMA_analytics}.latest_registration_activity cascade;

create view ${DB_SCHEMA_analytics}.latest_registration_activity as
select ROW_NUMBER() OVER () as id,
       t.mobile_number,
       t.timestamp,
       t.action             as registered,
       t.tenant
from ${DB_SCHEMA_analytics}.stage_log_auth t
         inner join
     (select mobile_number,
             max(timestamp) as MaxDate
      from ${DB_SCHEMA_analytics}.stage_log_auth
      where action in ('deregister', 'register')
        and result = 'successful'
      group by mobile_number) tm on t.mobile_number = tm.mobile_number
         and t.timestamp = tm.MaxDate;


drop view if exists ${DB_SCHEMA_analytics}.net_registration_activity cascade;

create view ${DB_SCHEMA_analytics}.net_registration_activity as
select ROW_NUMBER() OVER () as id,
       t.mobile_number,
       t.date,
       t1.action,
       t1.tenant
from (
         (select mobile_number,
                 date(timestamp + interval '180 minutes') as date,
                 MAX(timestamp)                           as maxdate
          from ${DB_SCHEMA_analytics}.stage_log_auth
          where action in ('deregister', 'register')
            and result = 'successful'
          group by mobile_number, date) t
             inner join
             (SELECT mobile_number,
                     action,
                     tenant,
                     date(timestamp + interval '180 minutes') as date,
                     MAX(timestamp)                           as maxdate
              from ${DB_SCHEMA_analytics}.stage_log_auth
              where action in ('deregister', 'register')
                and result = 'successful'
              group by mobile_number, date, action, tenant) t1 on t.mobile_number = t1.mobile_number
             and t1.maxdate = t.maxdate);


drop view if exists ${DB_SCHEMA_analytics}.campaign_rolled;

create view ${DB_SCHEMA_analytics}.campaign_rolled AS
SELECT ROW_NUMBER() OVER () AS id,
       channel_id,
       channel,
       intent               AS batch_identifier,
       message,
       timestamp,
       tenant
FROM ${DB_SCHEMA_analytics}.message_log
WHERE source = 'campaign';


drop view if exists ${DB_SCHEMA_analytics}.recent_ticket_activity cascade;

create view ${DB_SCHEMA_analytics}.recent_ticket_activity as
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
      from ${DB_SCHEMA_analytics}.complaint_ticket_logs
      ORDER by srn, last_updated_time DESC) as t;

drop view if exists ${DB_SCHEMA_analytics}.message_log_details cascade;
create view ${DB_SCHEMA_analytics}.message_log_details as
select row_number() over () as id,
       ml.channel_id,
       ml.message,
       ml.session_id,
       ml.timestamp,
       ml.channel,
       ml.context,
       ml.event,
       ml.event_type,
       ml.handled,
       ml.intent,
       ml.source,
       ml.score,
       ml.tenant,
       ml.message_id,
       us.customer_type
from ${DB_SCHEMA_analytics}.message_log ml
         full outer join ${DB_SCHEMA_analytics}.user_sessions us
                         on us.user_session_id = ml.session_id;

drop view if exists ${DB_SCHEMA_analytics}.stage_log_details cascade;
create view ${DB_SCHEMA_analytics}.stage_log_details as
select row_number() over () as id,
       sl.channel_id,
       sl.channel,
       sl.session_id,
       sl.transaction_intent,
       sl.transaction_id,
       sl.stage,
       sl.stage_result,
       sl.remarks,
       sl.timestamp,
       sl.rmn,
       sl.transaction_code,
       sl.node_id,
       sl.tenant,
       sl.amount,
       sl.currency,
       sl.details,
       sl.from_account,
       us.customer_type,
       sl.applicable_charges
from ${DB_SCHEMA_analytics}.stage_log sl
         full outer join ${DB_SCHEMA_analytics}.user_sessions us
                         on us.user_session_id = sl.session_id;

drop view if exists ${DB_SCHEMA_analytics}.api_log_details cascade;
create view ${DB_SCHEMA_analytics}.api_log_details as
select row_number() over () as id,
       al.endpoint,
       al.channel_id,
       al.request_id,
       al.session_id,
       al.api,
       al.stage,
       al.status,
       al.channel,
       al.internal_reference,
       al.external_reference,
       al.data,
       al.timestamp,
       al.exception,
       al.tenant,
       us.customer_type
from ${DB_SCHEMA_analytics}.api_log al
         full outer join ${DB_SCHEMA_analytics}.user_sessions us
                         on us.user_session_id = al.session_id;

drop view if exists ${DB_SCHEMA_analytics}.user_flow cascade;

create view ${DB_SCHEMA_analytics}.user_flow as
select ROW_NUMBER() OVER () as id, shankyModel.*
from (select first_six_messages.channel_id,
             LAG(first_six_messages.intent, 1) over (PARTITION BY channel_id ORDER BY timestamp) as source,
             first_six_messages.intent                                                           as target,
             first_six_messages.channel,
             first_six_messages.timestamp,
             first_six_messages.tenant,
             first_six_messages.rank,
             first_six_messages.customer_type
      from (SELECT ${DB_SCHEMA_analytics}.message_log_details.intent,
                   ${DB_SCHEMA_analytics}.message_log_details.channel_id,
                   ${DB_SCHEMA_analytics}.message_log_details.channel,
                   ${DB_SCHEMA_analytics}.message_log_details.timestamp,
                   ${DB_SCHEMA_analytics}.message_log_details.tenant,
                   ${DB_SCHEMA_analytics}.message_log_details.customer_type,
                   ROW_NUMBER() OVER (PARTITION BY channel_id, date(timestamp), tenant ORDER BY timestamp ASC) as rank
            FROM ${DB_SCHEMA_analytics}.message_log_details
            where source = 'user'
              and intent is not null
              and intent != 'fallback') first_six_messages
      where rank <= 3) shankyModel;


--drop FUNCTION IF EXISTS ${DB_SCHEMA_analytics}.get_session_end cascade;
--
--create or replace function ${DB_SCHEMA_analytics}.get_session_end(estimated_id character varying,
--                                                                  estimated_t timestamp with time zone,
--                                                                  channel_id character varying,
--                                                                  log_t timestamp with time zone) returns boolean
--    language plpgsql
--as
--$$
--BEGIN
--    IF estimated_id = channel_id and log_T > estimated_T THEN
--        return TRUE;
--    ELSIF estimated_id = channel_id THEN
--        return FALSE;
--    ELSE
--        return TRUE;
--    END IF;
--END;
--$$;
--
--drop FUNCTION IF EXISTS ${DB_SCHEMA_analytics}.get_table cascade;
--
--CREATE OR REPLACE FUNCTION ${DB_SCHEMA_analytics}.get_table()
--    RETURNS TABLE
--            (
--                channel_id VARCHAR,
--                log_T      timestamp with time zone,
--                session_T  timestamp with time zone
--            )
--AS
--$$
--
--    # variable_conflict use_column
--DECLARE
--    rec          record;
--    estimated_T  timestamp with time zone := '2001-01-01T00:00:00+00:00';
--    estimated_id VARCHAR                  := '';
--BEGIN
--    For rec in SELECT channel_id, timestamp from ${DB_SCHEMA_analytics}.message_log order by channel_id, timestamp
--        LOOP
--            IF
--                ${DB_SCHEMA_analytics}.get_session_end(estimated_id::VARCHAR, estimated_T::timestamp with time zone,
--                                                       rec.channel_id::VARCHAR,
--                                                       rec.timestamp::timestamp with time zone) = TRUE
--            THEN
--                estimated_T := rec.timestamp + interval '24 hours';
--                estimated_id := rec.channel_id;
--                RETURN QUERY SELECT estimated_id as channel_id, rec.timestamp as log_T, estimated_T as session_T;
--            ELSE
--                RETURN QUERY SELECT estimated_id as channel_id, rec.timestamp as log_T, estimated_T as session_T;
--            END IF;
--        END LOOP;
--END;
--$$
--    LANGUAGE 'plpgsql';
