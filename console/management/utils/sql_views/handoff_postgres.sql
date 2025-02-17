drop view if exists ${DB_SCHEMA_handoff}.new_user_in_handoff cascade;

create or replace view ${DB_SCHEMA_handoff}.new_user_in_handoff as
with tempuser as
         (SELECT id,
                 username,
                 phone_number,
                 channel_id,
                 email
          from ${DB_SCHEMA_handoff}.socialconversation_tempsocialuser),
     first_date as
         (select social_id,
                 username,
                 phone_number,
                 email,
                 channel_id,
                 tenant,
                 min(timestamp) as time,
                 channel
          from ${DB_SCHEMA_handoff}.analytics_socialevent
                   inner join tempuser on social_id = tempuser.id
          where event = 'handoff-initial'
          group by username,
                   phone_number,
                   email,
                   channel_id,
                   social_id,
                   channel,
                   tenant)
select ROW_NUMBER() OVER () as id, *
from first_date;

drop view if exists ${DB_SCHEMA_handoff}.returning_user_in_handoff cascade;

create or replace view ${DB_SCHEMA_handoff}.returning_user_in_handoff as
with tempuser as
         (SELECT id,
                 username,
                 phone_number,
                 channel_id,
                 email
          from ${DB_SCHEMA_handoff}.socialconversation_tempsocialuser),
     first_date as
         (select social_id,
                 username,
                 phone_number,
                 email,
                 channel_id,
                 tenant,
                 max(timestamp) as return_time,
                 channel
          from ${DB_SCHEMA_handoff}.analytics_socialevent
                   inner join tempuser on social_id = tempuser.id
          where event = 'handoff-initial'
          group by username,
                   phone_number,
                   email,
                   channel_id,
                   channel,
                   social_id,
                   tenant
          HAVING date(min(timestamp)) <> date(max(timestamp)))
SELECT ROW_NUMBER() OVER () as id, *
from first_date;

drop view if exists ${DB_SCHEMA_handoff}.abandoned_details cascade;

create or replace view ${DB_SCHEMA_handoff}.abandoned_details as
with tempuser as
         (SELECT id,
                 username,
                 phone_number,
                 email
          from ${DB_SCHEMA_handoff}.socialconversation_tempsocialuser),
     abandoned as
         (SELECT a.timestamp,
                 a.session,
                 tempuser.username,
                 phone_number,
                 email,
                 a.social_id,
                 a.channel,
                 a.event,
                 a.tenant
          from ${DB_SCHEMA_handoff}.analytics_socialevent as a
                   INNER join tempuser on a.social_id = tempuser.id)
SELECT ROW_NUMBER() OVER () as id, *
from abandoned;

drop view if exists ${DB_SCHEMA_handoff}.handoffduration cascade;

create or replace view ${DB_SCHEMA_handoff}.handoffduration as
with minutes as
         (SELECT max(timestamp)                                     as timestamp,
                 extract(epoch
                         from max(timestamp) - min(timestamp)) / 60 as minutes,
                 session,
                 agent_id,
                 social_id,
                 tenant
          from ${DB_SCHEMA_handoff}.analytics_socialevent
          where event not in ('handoff-notification')
          GROUP by session,
                   agent_id,
                   social_id,
                   tenant),
     agent_name as
         (SELECT a.username,
                 timestamp,
                 a.id as "user_id",
                 session,
                 minutes,
                 agent_id,
                 social_id,
                 minutes.tenant
          from ${DB_SCHEMA_handoff}.socialconversation_agent as a
                   inner join minutes on a.id = minutes.agent_id)
select ROW_NUMBER() OVER () as id, *
from agent_name;


drop view if exists ${DB_SCHEMA_handoff}.agent_last_activity_time cascade;

create or replace view ${DB_SCHEMA_handoff}.agent_last_activity_time as
with timeframe as
         (SELECT (date((timestamp))) as dt,
                 agent_id,
                 max((timestamp))    as diff,
                 tenant
          from ${DB_SCHEMA_handoff}.analytics_socialevent
          group by agent_id,
                   date((timestamp)),
                   tenant),
     agent as
         (select *
          from ${DB_SCHEMA_handoff}.socialconversation_agent)
SELECT ROW_NUMBER() OVER () as id,
       timeframe.dt,
       timeframe.diff,
       agent.id             as "user_id",
       agent.username,
       timeframe.tenant
from timeframe
         INNER join agent on timeframe.agent_id = agent.id
order by diff desc;

drop view if exists ${DB_SCHEMA_handoff}.agent_skill cascade;

create or replace view ${DB_SCHEMA_handoff}.agent_skill as
select ROW_NUMBER() OVER () as id, a.agent_id, a.skill_id, b.skill_name, c.username, e.tenant_name as tenant
from ${DB_SCHEMA_handoff}.socialconversation_agentskill as a
         join ${DB_SCHEMA_handoff}.socialconversation_skill as b on a.skill_id = b.id
         join ${DB_SCHEMA_handoff}.socialconversation_agent as c on a.agent_id = c.id
         join ${DB_SCHEMA_handoff}.socialconversation_agenttenant as d on c.id = d.agent_id
         join ${DB_SCHEMA_handoff}.socialconversation_tenant as e on d.tenant_id = e.id;

drop view if exists ${DB_SCHEMA_handoff}.current_logged_in cascade;

create or replace view ${DB_SCHEMA_handoff}.current_logged_in as
select a.agent_id, b.skill_name, c.username, c.is_online, c.id, e.tenant_name as tenant
from ${DB_SCHEMA_handoff}.socialconversation_agentskill as a
         join ${DB_SCHEMA_handoff}.socialconversation_skill as b on a.skill_id = b.id
         join ${DB_SCHEMA_handoff}.socialconversation_agent as c on a.agent_id = c.id
         join ${DB_SCHEMA_handoff}.socialconversation_agenttenant as d on c.id = d.agent_id
         join ${DB_SCHEMA_handoff}.socialconversation_tenant as e on d.tenant_id = e.id;

drop view if exists ${DB_SCHEMA_handoff}.agent_productivity cascade;
CREATE OR REPLACE VIEW ${DB_SCHEMA_handoff}.agent_productivity AS
WITH agent_events AS (
    SELECT p2.username,
           p1.event,
           p1.session AS session_id,
           p1.tenant,
           p1.channel,
           p3.username AS agent,
           p1.timestamp,
           p2.tenant AS tenant_alias
    FROM ${DB_SCHEMA_handoff}.analytics_socialevent p1
    INNER JOIN ${DB_SCHEMA_handoff}.socialconversation_tempsocialuser p2 ON p1.social_id = p2.id AND p1.tenant = p2.tenant
    LEFT JOIN ${DB_SCHEMA_handoff}.socialconversation_agent p3 ON p3.id = p1.agent_id
    WHERE p1.event IN ('handoff-initial', 'handoff-notification', 'agent-accept')
),
agent_acceptime AS (
    SELECT session_id,
           TO_CHAR((EXTRACT(EPOCH FROM MAX(timestamp) - MIN(timestamp)) * INTERVAL '1 second')::interval, 'HH24:MI:SS') AS accept_time
    FROM agent_events
    WHERE event IN ('handoff-initial', 'agent-accept')
    GROUP BY session_id
),
agent_initialTime AS (
    SELECT session_id,
           MIN(timestamp) AS initial_time
    FROM agent_events
    WHERE event = 'handoff-initial'
    GROUP BY session_id
)
SELECT ROW_NUMBER() OVER () AS id,
       e.username,
       e.tenant_alias AS tenant,
       ARRAY_AGG(DISTINCT CASE WHEN e.event = 'handoff-notification' THEN e.agent END) AS agent_routed,
       e.session_id,
       e.channel,
       ARRAY_AGG(DISTINCT CASE WHEN e2.event = 'agent-accept' THEN e2.agent END) AS agent_accept,
       at.accept_time,
       it.initial_time
FROM agent_events e
LEFT JOIN agent_events e2 ON e.session_id = e2.session_id AND e2.event = 'agent-accept'
INNER JOIN agent_acceptime at ON e.session_id = at.session_id
INNER JOIN agent_initialTime it ON e.session_id = it.session_id
WHERE e.event = 'handoff-notification'
GROUP BY e.username, e.tenant_alias, e.session_id, e.channel, at.accept_time, it.initial_time;


drop view if exists ${DB_SCHEMA_handoff}.agent_transfer cascade;
create or replace view ${DB_SCHEMA_handoff}.agent_transfer as
with events as (select p2.username,
                       p1.timestamp,
                       p1.event,
                       p1.parent_session_id,
                       p3.username as "agent",
                       p1.channel,
                       p2.tenant   AS tenant_alias
                from ${DB_SCHEMA_handoff}.analytics_socialevent p1
                         inner join ${DB_SCHEMA_handoff}.socialconversation_tempsocialuser p2
                                    on p1.social_id = p2.id
                         left join ${DB_SCHEMA_handoff}.socialconversation_agent p3
                                   ON p3.id = p1.agent_id
                where p1.event in ('handoff-initial', 'handoff-transfer-from', 'handoff-transfer-to', 'agent-accept',
                                   'user-cancel-routing', 'agent-force-end', 'user-inactive', 'agent-end-confirm',
                                   'user-end-confirm')
                  and parent_session_id <> ''),
     totalSession as (select parent_session_id,
                             TO_CHAR(
                                     (EXTRACT(EPOCH FROM MAX(timestamp) - MIN(timestamp)) *
                                      INTERVAL '1 second')::interval,
                                     'HH24:MI:SS'
                             ) as Total_session
                      from events
                      where event in ('handoff-initial', 'agent-end-confirm', 'user-end-confirm', 'agent-force-end',
                                      'user-inactive')
                      group by parent_session_id),
     initialtime as (select parent_session_id, timestamp as initial_time
                     from events
                     where event = 'handoff-initial'
                     group by parent_session_id, timestamp),
     accepttime as (select parent_session_id, timestamp as accept_time
                    from events
                    where event = 'agent-accept'
                    group by parent_session_id, timestamp)
SELECT ROW_NUMBER() OVER ()                                                AS id,
       e.parent_session_id,
       e.username,
       e.tenant_alias                                                      as tenant,
       ARRAY_AGG(s.agent) FILTER (WHERE s.event = 'handoff-transfer-to')   AS transferred_agents,
       ARRAY_AGG(DISTINCT x.agent) FILTER (WHERE x.event = 'agent-accept') AS initial_agent,
       ts.total_session,
       it.initial_time,
       at.accept_time,
       e.channel
FROM events e
         LEFT JOIN
     totalSession ts ON e.parent_session_id = ts.parent_session_id
         LEFT JOIN
     accepttime at ON e.parent_session_id = at.parent_session_id
         LEFT JOIN
     initialtime it ON e.parent_session_id = it.parent_session_id
         LEFT JOIN
     events s ON e.parent_session_id = s.parent_session_id
         LEFT JOIN
     events x ON e.parent_session_id = x.parent_session_id
GROUP BY e.parent_session_id, e.username, ts.total_session, it.initial_time, at.accept_time, e.channel, e.tenant_alias;

drop view if exists ${DB_SCHEMA_handoff}.handoff_flow cascade;
create or replace view ${DB_SCHEMA_handoff}.handoff_flow as
select ROW_NUMBER() OVER ()                                                  as id,
       flow.session_id,
       LAG(flow.events, 1) over (PARTITION by session_id order by timestamp) as source,
       flow.events                                                           as target,
       flow.channel,
       flow.timestamp,
       flow.tenant
from (select distinct(event) as events, parent_session_id as session_id, channel, min(timestamp) as timestamp, tenant
      from ${DB_SCHEMA_handoff}.analytics_socialevent
      where parent_session_id <> ''
        and event not like '%transfer%'
        and event not like '%note%'
        and event not in ('agent-end-trigger', 'social-message', 'chat-message')
      group by events, session_id, channel, tenant
      order by session_id, timestamp) as flow;
