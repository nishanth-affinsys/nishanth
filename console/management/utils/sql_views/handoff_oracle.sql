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
      inner join tempuser on social_id=tempuser.id
      where event='handoff-initial'
      group by username,
               phone_number,
               email,
               channel_id,
               social_id,
               channel,
               tenant) select ROW_NUMBER() OVER (ORDER BY NULL) as id, first_date.*
   from first_date;

create or replace view ${DB_SCHEMA_handoff}.returning_user_in_handoff as
WITH tempuser AS (
  SELECT
    id,
    username,
    phone_number,
    channel_id,
    email
  FROM
    ${DB_SCHEMA_handoff}.socialconversation_tempsocialuser
),
first_date AS (
  SELECT
    social_id,
    username,
    phone_number,
    email,
    channel_id,
    tenant,
    MAX(timestamp) AS return_time,
    channel
  FROM
    ${DB_SCHEMA_handoff}.analytics_socialevent
    INNER JOIN tempuser ON social_id = tempuser.id
  WHERE
    event = 'handoff-initial'
  GROUP BY
    username,
    phone_number,
    email,
    channel_id,
    channel,
    social_id,
    tenant
  HAVING
    TRUNC(MIN(timestamp)) <> TRUNC(MAX(timestamp))
)
SELECT
  ROW_NUMBER() OVER (ORDER BY NULL) AS id,
  first_date.*
FROM
  first_date;

create or replace view ${DB_SCHEMA_handoff}.abandoned_details as
WITH tempuser AS (
  SELECT
    id,
    username,
    phone_number,
    email
  FROM
    ${DB_SCHEMA_handoff}.socialconversation_tempsocialuser
),
abandoned AS (
  SELECT
    a.timestamp,
    a."SESSION",
    tempuser.username,
    phone_number,
    email,
    a.social_id,
    a.channel,
    a.event,
    a.tenant
  FROM
    ${DB_SCHEMA_handoff}.analytics_socialevent a
    INNER JOIN tempuser ON a.social_id = tempuser.id
)
SELECT
  ROW_NUMBER() OVER (ORDER BY NULL) AS id,
  a.*
FROM
  abandoned a;

create or replace view ${DB_SCHEMA_handoff}.handoffduration as
WITH minutes AS (
  SELECT
    MAX(timestamp) AS timestamp,
    (MAX(timestamp) - MIN(timestamp)) AS minutes,
    "SESSION",
    agent_id,
    social_id,
    tenant
  FROM
    ${DB_SCHEMA_handoff}.analytics_socialevent
  WHERE
    event NOT IN ('handoff-notification')
  GROUP BY
    "SESSION",
    agent_id,
    social_id,
    tenant
),
agent_name AS (
  SELECT
    a.username,
    timestamp,
    a.id AS "user_id",
    m."SESSION",
    ((sysdate + m.minutes) - sysdate)*3600 AS MINUTES ,
    agent_id,
    social_id,
    m.tenant
  FROM
    ${DB_SCHEMA_handoff}.socialconversation_agent a
    INNER JOIN minutes m ON a.id = m.agent_id
)
SELECT
  ROW_NUMBER() OVER (ORDER BY NULL) AS id,
  an.*
FROM
  agent_name an;

create or replace view ${DB_SCHEMA_handoff}.agent_last_activity_time as
WITH timeframe AS (
  SELECT
    TRUNC(timestamp) AS dt,
    agent_id,
    MAX(timestamp) AS diff,
    tenant
  FROM
    ${DB_SCHEMA_handoff}.analytics_socialevent
  GROUP BY
    agent_id,
    TRUNC(timestamp),
    tenant
),
agent AS (
  SELECT
    *
  FROM
    ${DB_SCHEMA_handoff}.socialconversation_agent
)
SELECT
  ROW_NUMBER() OVER (ORDER BY NULL) AS id,
  TO_CHAR(timeframe.dt, 'YYYY-MM-DD') AS dt,
  timeframe.diff,
  agent.id AS "user_id",
  agent.username,
  timeframe.tenant
FROM
  timeframe
INNER JOIN
  agent ON timeframe.agent_id = agent.id
ORDER BY
  diff DESC;

create or replace view ${DB_SCHEMA_handoff}.agent_skill as
SELECT
  ROW_NUMBER() OVER (ORDER BY NULL) AS id,
  a.agent_id,
  a.skill_id,
  b.skill_name,
  c.username,
  e.tenant_name AS tenant
FROM
  ${DB_SCHEMA_handoff}.socialconversation_agentskill a
JOIN
  ${DB_SCHEMA_handoff}.socialconversation_skill b ON a.skill_id = b.id
JOIN
  ${DB_SCHEMA_handoff}.socialconversation_agent c ON a.agent_id = c.id
JOIN
  ${DB_SCHEMA_handoff}.socialconversation_agenttenant d ON c.id = d.agent_id
JOIN
  ${DB_SCHEMA_handoff}.socialconversation_tenant e ON d.tenant_id = e.id;

create or replace view ${DB_SCHEMA_handoff}.current_logged_in as
SELECT
  a.agent_id,
  b.skill_name,
  c.username,
  c.is_online,
  c.id,
  e.tenant_name AS tenant
FROM
  ${DB_SCHEMA_handoff}.socialconversation_agentskill a
JOIN
  ${DB_SCHEMA_handoff}.socialconversation_skill b ON a.skill_id = b.id
JOIN
  ${DB_SCHEMA_handoff}.socialconversation_agent c ON a.agent_id = c.id
JOIN
  ${DB_SCHEMA_handoff}.socialconversation_agenttenant d ON c.id = d.agent_id
JOIN
  ${DB_SCHEMA_handoff}.socialconversation_tenant e ON d.tenant_id = e.id;

create or replace view ${DB_SCHEMA_handoff}.agent_productivity as
WITH events AS (
  SELECT
    p2.username,
    p1.event,
    p1."SESSION" AS "SESSION_ID",
    p1.tenant,
    p1.channel,
    p3."agent",
    p1.timestamp
  FROM
    ${DB_SCHEMA_handoff}.analytics_socialevent p1
  INNER JOIN
    ${DB_SCHEMA_handoff}.socialconversation_tempsocialuser p2 ON p1.social_id = p2.id AND p1.tenant = p2.tenant
  LEFT JOIN (
    SELECT
      t2.agent_id,
      t1.username AS "agent",
      t3.tenant_name AS "tenant"
    FROM
      ${DB_SCHEMA_handoff}.socialconversation_agent t1
    INNER JOIN
      ${DB_SCHEMA_handoff}.socialconversation_agenttenant t2 ON t1.id = t2.agent_id
    INNER JOIN
      ${DB_SCHEMA_handoff}.socialconversation_tenant t3 ON t2.tenant_id = t3.id
  ) p3 ON p3.agent_id = p1.agent_id AND p3."tenant" = p1.tenant
  WHERE
    p1.event IN ('handoff-initial', 'handoff-notification', 'agent-accept')
  ORDER BY
    p2.username, p1.timestamp
),
accepttime AS (
  SELECT
    "SESSION_ID",
      REGEXP_SUBSTR(MAX(timestamp) - MIN(timestamp),'\d{2}:\d{2}:\d{2}')
    AS "ACCEPT_TIME"
  FROM
    events
  WHERE
    events.event IN ('handoff-initial', 'agent-accept')
  GROUP BY
    "SESSION_ID"
),
initialtime AS (
  SELECT
    "SESSION_ID",
    timestamp AS "INITIAL_TIME"
  FROM
    events
  WHERE
    events.event IN ('handoff-initial')
),
productivity AS (
  SELECT
  ROW_NUMBER() OVER (ORDER BY NULL) AS id,
  username,
  LISTAGG(DISTINCT CASE WHEN events.event = 'handoff-notification' THEN events."agent" ELSE NULL END, ',') WITHIN GROUP (ORDER BY "agent") AS "AGENT_ROUTED",
  events."SESSION_ID",
  channel,
  LISTAGG(DISTINCT CASE WHEN events.event = 'agent-accept' THEN events."agent" ELSE NULL END, ',') WITHIN GROUP (ORDER BY "agent") AS "AGENT_ACCEPT",
  MAX("ACCEPT_TIME") AS "ACCEPT_TIME",
  MAX("INITIAL_TIME") AS "INITIAL_TIME",
  tenant
FROM
  events
INNER JOIN
  accepttime ON events."SESSION_ID" = accepttime."SESSION_ID"
INNER JOIN
  initialtime ON events."SESSION_ID" = initialtime."SESSION_ID"
WHERE
  events.event IN ('handoff-notification', 'agent-accept')
GROUP BY
  username, events."SESSION_ID", channel, tenant
)
SELECT
  *
FROM
  productivity;

create or replace view ${DB_SCHEMA_handoff}.agent_transfer as
WITH events AS (
    SELECT
        p2.username,
        p1.timestamp,
        p1.event,
        p1.parent_session_id,
        p3.agent,
        p1.channel,
        p2.tenant
    FROM
        ${DB_SCHEMA_handoff}.analytics_socialevent p1
    INNER JOIN
        ${DB_SCHEMA_handoff}.socialconversation_tempsocialuser p2 ON p1.social_id = p2.id
    LEFT JOIN (
        SELECT
            t1.username AS agent,
            t1.id AS agentid,
            t3.tenant_name AS tenant
        FROM
            ${DB_SCHEMA_handoff}.socialconversation_agent t1
        INNER JOIN
            ${DB_SCHEMA_handoff}.socialconversation_agenttenant t2 ON t1.id = t2.agent_id
        INNER JOIN
            ${DB_SCHEMA_handoff}.socialconversation_tenant t3 ON t2.tenant_id = t3.id
    ) p3 ON p1.agent_id = p3.agentid AND p2.tenant = p3.tenant
    WHERE
        p1.event IN ('handoff-initial','handoff-transfer-from','handoff-transfer-to','agent-accept','user-cancel-routing','agent-force-end','user-inactive','agent-end-confirm','user-end-confirm')
        AND p1.parent_session_id IS NOT NULL
),
totalSession AS (
    SELECT
        parent_session_id,
        REGEXP_SUBSTR(MAX(timestamp) - MIN(timestamp),'\d{2}:\d{2}:\d{2}') AS Total_session
    FROM
        events
    WHERE
        event IN ('handoff-initial','agent-end-confirm','user-end-confirm','agent-force-end','user-inactive')
    GROUP BY
        parent_session_id
),
initialtime AS (
    SELECT
        parent_session_id,
        timestamp AS initial_time
    FROM
        events
    WHERE
        event = 'handoff-initial'
    GROUP BY
        parent_session_id, timestamp
),
accepttime AS (
    SELECT
        parent_session_id,
        timestamp AS accept_time
    FROM
        events
    WHERE
        event = 'agent-accept'
    GROUP BY
        parent_session_id, timestamp
)
SELECT
    ROW_NUMBER() OVER (ORDER BY NULL) AS id,
    e.parent_session_id,
    e.username,
    LISTAGG(CASE WHEN e.event = 'handoff-transfer-to' THEN e.agent ELSE NULL END, ',') WITHIN GROUP (ORDER BY NULL) AS transferred_agents,
    LISTAGG(DISTINCT CASE WHEN e.event = 'agent-accept' THEN e.agent ELSE NULL END, ',') WITHIN GROUP (ORDER BY agent) AS initial_agent,
    ts.Total_session AS total_session,
    it.initial_time,
    at.accept_time,
    e.channel,
    e.tenant
FROM
    events e
LEFT JOIN
    totalSession ts ON e.parent_session_id = ts.parent_session_id
LEFT JOIN
    accepttime at ON e.parent_session_id = at.parent_session_id
LEFT JOIN
    initialtime it ON e.parent_session_id = it.parent_session_id
GROUP BY
    e.parent_session_id, e.username, ts.total_session, it.initial_time, at.accept_time, e.channel, e.tenant;

create or replace view ${DB_SCHEMA_handoff}.handoff_flow as
SELECT
    ROW_NUMBER() OVER (ORDER BY NULL) AS id,
    flow.session_id,
    LAG(flow.events, 1) OVER (PARTITION BY flow.session_id ORDER BY flow.timestamp) AS source,
    flow.events AS target,
    flow.channel,
    flow.timestamp,
    flow.tenant
FROM (
    SELECT DISTINCT
        event AS events,
        parent_session_id AS session_id,
        channel,
        MIN(timestamp) AS timestamp,
        tenant
    FROM
        ${DB_SCHEMA_handoff}.analytics_socialevent
    WHERE
        parent_session_id IS NOT NULL
        AND event NOT LIKE '%transfer%'
        AND event NOT LIKE '%note%'
        AND event NOT IN ('agent-end-trigger', 'social-message', 'chat-message')
    GROUP BY
        event, parent_session_id, channel, tenant
    ORDER BY
        parent_session_id, timestamp
) flow