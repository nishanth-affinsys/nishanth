drop view if exists ${DB_SCHEMA_analytics}.campaign_notification cascade;

CREATE OR REPLACE VIEW ${DB_SCHEMA_analytics}.campaign_notification AS
WITH campaign_data AS (SELECT sru.campaign_id     AS campaign_filter_id,
                              c.campaign_id       AS campaign_id,
                              c.campaign_name     AS campaign_name,
                              c.created_timestamp,
                              c.last_modified,
                              scd.identifier      AS sub_campaign_identifier,
                              scd.name            AS sub_campaign_name,
                              sru.run_id          AS run_id,
                              sru.notification_id AS notification_id
                       FROM ${DB_SCHEMA_campaign}.sub_campaign_run sru
                                JOIN
                            ${DB_SCHEMA_campaign}.sub_campaign_detail scd ON sru.sub_campaign_id = scd.id
                                JOIN
                            ${DB_SCHEMA_campaign}.campaign c ON sru.campaign_id = c.id),
     notification_data AS (select nd.batch_id,
                                  bi.identifier    as batch_identifier,
                                  bi.channel_id,
                                  bi.channel_name,
                                  nd.tenant,
                                  nd.message_id_id as message_id,
                                  nd.status        as notification_status,
                                  nd.timestamp     as notification_timestamp,
                                  cd.profile_id,
                                  p.user_name
                           from ${DB_SCHEMA_profile}.notification_data nd
                                    join
                                ${DB_SCHEMA_profile}.batch_identifier bi on nd.batch_id = bi.id
                                    join
                                ${DB_SCHEMA_profile}.campaign_data cd on cd.batch_id = bi.id and cd.tenant = nd.tenant
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
                                             nd.user_name,
                                             nd.channel_id as initial_channel_id,
                                             CASE
                                                 WHEN nd.channel_name = 'whatsapps' AND sm.mobile_number IS NOT NULL
                                                     THEN sm.conversation_id
                                                 ELSE nd.channel_id
                                                 END       AS channel_id
                                      FROM notification_data nd
                                               LEFT JOIN
                                           ${DB_SCHEMA_analytics}.sunshine_mapping sm
                                           ON nd.tenant = sm.tenant AND nd.channel_id = sm.mobile_number),
     campaign_notification AS (SELECT cd.campaign_filter_id,
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
                                      nsm.user_name                                                            as profile_name,
                                      Case when nsm.notification_status <> 'Failure' then 'sent' else null end as status,
                                      Case
                                          when ms.timestamp is not null then ms.timestamp
                                          else nsm.notification_timestamp end                                  as message_timestamp,
                                      nsm.notification_timestamp
                               FROM campaign_data cd
                                        JOIN
                                    notification_sunshine_mapped nsm ON cd.notification_id = nsm.batch_identifier
                                        LEFT OUTER JOIN
                                    ${DB_SCHEMA_analytics}.message_status ms
                                    ON nsm.tenant = ms.tenant AND nsm.message_id = ms.message_id and ms.status = 'sent'
                               UNION
                               SELECT
                                   cd.campaign_filter_id, cd.campaign_id, cd.campaign_name, cd.sub_campaign_identifier, cd.sub_campaign_name, cd.run_id, cd.created_timestamp, cd.last_modified, nsm.batch_id, nsm.batch_identifier, nsm.channel_id, nsm.initial_channel_id, nsm.channel_name, nsm.message_id, nsm.tenant, nsm.notification_status, nsm.user_name as profile_name, ms.status, Case when ms.timestamp is not null then ms.timestamp else nsm.notification_timestamp end as message_timestamp, nsm.notification_timestamp
                               FROM
                                   campaign_data cd
                                   JOIN
                                   notification_sunshine_mapped nsm
                               ON cd.notification_id = nsm.batch_identifier
                                   JOIN
                                   ${DB_SCHEMA_analytics}.message_status ms ON nsm.tenant = ms.tenant AND nsm.message_id = ms.message_id and ms.status in ('read' ,'delivered'))
select ROW_NUMBER() OVER () AS id, *
from campaign_notification;