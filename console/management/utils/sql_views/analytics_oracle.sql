create or replace view ${DB_SCHEMA_analytics}.latest_registration_activity as
select ROW_NUMBER() OVER (ORDER BY NULL) as id,
       t.mobile_number,
       t.timestamp,
       t.action                          as registered,
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

CREATE OR REPLACE VIEW ${DB_SCHEMA_analytics}.recent_ticket_activity AS
SELECT ROW_NUMBER() OVER (ORDER BY NULL) AS id,
       srn,
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
FROM (SELECT DISTINCT srn,
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
      FROM (SELECT srn,
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
            FROM ${DB_SCHEMA_analytics}.complaint_ticket_logs
            ORDER BY srn, last_updated_time DESC)) t;


create or replace view ${DB_SCHEMA_analytics}.message_log_details as
select row_number() OVER (ORDER BY NULL) as id,
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

create or replace view ${DB_SCHEMA_analytics}.stage_log_details as
select row_number() OVER (ORDER BY NULL) as id,
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
       CAST(sl.details as varchar2(4000))            as details,
       sl.from_account,
       sl.applicable_charges,
       us.customer_type
from ${DB_SCHEMA_analytics}.stage_log sl
         full outer join ${DB_SCHEMA_analytics}.user_sessions us
                         on us.user_session_id = sl.session_id;

create or replace view ${DB_SCHEMA_analytics}.api_log_details as
select row_number() OVER (ORDER BY NULL) as id,
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


create or replace view ${DB_SCHEMA_analytics}.user_flow as
select ROW_NUMBER() OVER (ORDER BY NULL) as id, shankyModel.*
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
                   ROW_NUMBER() OVER (PARTITION BY channel_id, trunc(timestamp), tenant ORDER BY timestamp ASC) as rank
            FROM ${DB_SCHEMA_analytics}.message_log_details
            where source = 'user'
              and intent is not null
              and intent != 'fallback') first_six_messages
      where rank <= 3) shankyModel;

CREATE OR REPLACE VIEW ${DB_SCHEMA_analytics}.campaign_rolled AS
SELECT ROW_NUMBER() OVER (ORDER BY NULL) AS id,
       channel_id,
       channel,
       intent                            AS batch_identifier,
       message,
       timestamp,
       tenant
FROM ${DB_SCHEMA_analytics}.message_log
WHERE source = 'campaign';


CREATE OR REPLACE VIEW ${DB_SCHEMA_analytics}.campaign_notification AS
WITH campaign_data_cte AS (SELECT sru.campaign_id                            AS campaign_variants,
                                  CAST(c.campaign_id AS varchar2(250))       AS campaign_id,
                                  CAST(c.campaign_name AS varchar2(150))     AS campaign_name,
                                  c.created_timestamp,
                                  c.last_modified,
                                  CAST(SCD.IDENTIFIER AS varchar2(250))      AS sub_campaign_identifier,
                                  CAST(SCD.NAME AS varchar2(150))            AS sub_campaign_name,
                                  sru.run_id                                 AS run_id,
                                  CAST(sru.notification_id AS VARCHAR2(250)) AS notification_id
                           FROM ${DB_SCHEMA_campaign}.sub_campaign_run sru
                                    JOIN
                                ${DB_SCHEMA_campaign}.sub_campaign_detail scd ON sru.sub_campaign_id = scd.id
                                    JOIN
                                ${DB_SCHEMA_campaign}.campaign c ON sru.campaign_id = c.id),
     notification_data_cte AS (select nd.batch_id,
                                      bi.identifier    as batch_identifier,
                                      bi.channel_id,
                                      bi.channel_name,
                                      nd.tenant,
                                      nd.message_id_id as message_id,
                                      nd.status        as notification_status,
                                      nd.timestamp     as notification_timestamp,
                                      cd.profile_id,
                                      p.user_name      as profile_name
                               from ${DB_SCHEMA_profile}.notification_data nd
                                        join
                                    ${DB_SCHEMA_profile}.batch_identifier bi on nd.batch_id = bi.id
                                        join
                                    ${DB_SCHEMA_profile}.campaign_data cd
                                    on cd.batch_id = bi.id and cd.tenant = nd.tenant
                                        join
                                    ${DB_SCHEMA_profile}.profile p
                                    on p.profile_id = cd.profile_id and p.tenant = cd.tenant),
     notification_sunshine_mapped AS (SELECT nd.batch_id,
                                             nd.batch_identifier,
                                             nd.channel_name,
                                             nd.tenant,
                                             nd.message_id,
                                             nd.notification_status,
                                             nd.notification_timestamp,
                                             nd.profile_id,
                                             nd.profile_name,
                                             nd.channel_id as initial_channel_id,
                                             CASE
                                                 WHEN nd.channel_name = 'whatsapps' AND sm.mobile_number IS NOT NULL
                                                     THEN sm.conversation_id
                                                 ELSE nd.channel_id
                                                 END       AS channel_id
                                      FROM notification_data_cte nd
                                               LEFT JOIN
                                           ${DB_SCHEMA_analytics}.sunshine_mapping sm
                                           ON nd.tenant = sm.tenant AND nd.channel_id = sm.mobile_number),
     campaign_notification AS (SELECT cd.campaign_variants,
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
                                      nsm.profile_name,
                                      Case
                                          when nsm.notification_status <> 'Failure' then CAST('sent' AS VARCHAR2(50))
                                          else null end                       as status,
                                      Case
                                          when ms.timestamp is not null then ms.timestamp
                                          else nsm.notification_timestamp end as message_timestamp,
                                      nsm.notification_timestamp
                               FROM campaign_data_cte cd
                                        JOIN
                                    notification_sunshine_mapped nsm ON cd.notification_id = nsm.batch_identifier
                                        LEFT OUTER JOIN
                                    ${DB_SCHEMA_analytics}.message_status ms
                                    ON nsm.tenant = ms.tenant AND nsm.message_id = ms.message_id and ms.status = 'sent'
                               UNION
                               SELECT cd.campaign_variants,
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
                                      nsm.profile_name,
                                      CAST(ms.status AS VARCHAR2(50))         AS STATUS,
                                      Case
                                          when ms.timestamp is not null then ms.timestamp
                                          else nsm.notification_timestamp end as message_timestamp,
                                      nsm.notification_timestamp
                               FROM campaign_data_cte cd
                                        JOIN
                                    notification_sunshine_mapped nsm ON cd.notification_id = nsm.batch_identifier
                                        JOIN
                                    ${DB_SCHEMA_analytics}.message_status ms
                                    ON nsm.tenant = ms.tenant AND nsm.message_id = ms.message_id and
                                       ms.status in ('read', 'delivered'))
SELECT ROW_NUMBER() OVER (ORDER BY NULL) AS id, cn.*
FROM campaign_notification cn;