DO $$
DECLARE
    tenantName RECORD;
    schemaName VARCHAR(255);
    sqlQuery TEXT;
    dbSchema VARCHAR(255) := '${DB_SCHEMA_handoff}';
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

            sqlQuery :='drop view if exists ' || schemaName || '.new_user_in_handoff cascade;
                create or replace view ' || schemaName || '.new_user_in_handoff as
                with tempuser as
                     (SELECT id,
                             username,
                             phone_number,
                             channel_id,
                             email
                      from ' || schemaName || '.socialconversation_tempsocialuser),
                        first_date as
                     (select social_id,
                             username,
                             phone_number,
                             email,
                             channel_id,
                             tenant,
                             min(timestamp) as time,
                             channel
                      from ' || schemaName || '.analytics_socialevent
                      inner join tempuser on social_id=tempuser.id
                      where event=''handoff-initial''
                      group by username,
                               phone_number,
                               email,
                               channel_id,
                               social_id,
                               channel,
                               tenant) select ROW_NUMBER() OVER () as id, *
                   from first_date;

                drop view if exists ' || schemaName || '.returning_user_in_handoff cascade;

                create or replace view ' || schemaName || '.returning_user_in_handoff as
                with tempuser as
                     (SELECT id,
                             username,
                             phone_number,
                             channel_id,
                             email
                      from ' || schemaName || '.socialconversation_tempsocialuser),
                        first_date as
                     (select social_id,
                             username,
                             phone_number,
                             email,
                             channel_id,
                             tenant,
                             max(timestamp) as return_time,
                             channel
                      from ' || schemaName || '.analytics_socialevent
                      inner join tempuser on social_id=tempuser.id
                      where event=''handoff-initial''
                      group by username,
                               phone_number,
                               email,
                               channel_id,
                               channel,
                               social_id,
                               tenant
                      HAVING date(min(timestamp))<> date(max(timestamp))) SELECT ROW_NUMBER() OVER () as id, *
                   from first_date;

                drop view if exists ' || schemaName || '.abandoned_details cascade;

                create or replace view ' || schemaName || '.abandoned_details as
                with tempuser as
                     (SELECT id,
                             username,
                             phone_number,
                             email
                      from ' || schemaName || '.socialconversation_tempsocialuser),
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
                      from ' || schemaName || '.analytics_socialevent as a
                      INNER join tempuser on a.social_id =tempuser.id) SELECT ROW_NUMBER() OVER () as id, *
                   from abandoned;

                drop view if exists ' || schemaName || '.handoffduration cascade;

                create or replace view ' || schemaName || '.handoffduration as
                with minutes as
                     (SELECT max(timestamp) as timestamp,
                             extract(epoch
                                     from max(timestamp)-min(timestamp))/60 as minutes,
                             session,
                             agent_id,
                             social_id,
                             tenant
                      from ' || schemaName || '.analytics_socialevent
                      where event not in (''handoff-notification'')
                      GROUP by
                               session,
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
                      from ' || schemaName || '.socialconversation_agent as a
                      inner join minutes on a.id=minutes.agent_id) select ROW_NUMBER() OVER () as id, *
                   from agent_name;


                drop view if exists ' || schemaName || '.agent_last_activity_time cascade;

                create or replace view ' || schemaName || '.agent_last_activity_time as
                with timeframe as
                     (SELECT (date((timestamp))) as dt,
                             agent_id,
                             max((timestamp)) as diff,
                             tenant
                      from ' || schemaName || '.analytics_socialevent
                      group by agent_id,
                               date((timestamp)),
                               tenant),
                        agent as
                     (select *
                      from ' || schemaName || '.socialconversation_agent)SELECT ROW_NUMBER() OVER () as id,timeframe.dt,
                                                                         timeframe.diff,
                                                                         agent.id as "user_id",
                                                                         agent.username,
                                                                         timeframe.tenant
                   from timeframe
                   INNER join agent on timeframe.agent_id=agent.id
                   order by diff desc;

                drop view if exists ' || schemaName || '.agent_skill cascade;

                create or replace view ' || schemaName || '.agent_skill as
                select ROW_NUMBER() OVER () as id,a.agent_id,a.skill_id,b.skill_name,c.username,e.tenant_name as tenant from ' || schemaName || '.socialconversation_agentskill as a
                join ' || schemaName || '.socialconversation_skill as b on a.skill_id=b.id
                join ' || schemaName || '.socialconversation_agent as c on a.agent_id=c.id
                join ' || schemaName || '.socialconversation_agenttenant as d on c.id=d.agent_id
                join ' || schemaName || '.socialconversation_tenant as e on d.tenant_id=e.id;

                drop view if exists ' || schemaName || '.current_logged_in cascade;

                create or replace view ' || schemaName || '.current_logged_in as
                select a.agent_id,b.skill_name,c.username,c.is_online,c.id,e.tenant_name as tenant from ' || schemaName || '.socialconversation_agentskill as a
                join ' || schemaName || '.socialconversation_skill as b on a.skill_id=b.id
                join ' || schemaName || '.socialconversation_agent as c on a.agent_id=c.id
                join ' || schemaName || '.socialconversation_agenttenant as d on c.id=d.agent_id
                join ' || schemaName || '.socialconversation_tenant as e on d.tenant_id=e.id;

                drop view if exists ' || schemaName || '.agent_productivity cascade;

                create or replace view ' || schemaName || '.agent_productivity as
                with events as (select p2.username,
                                p1.event,
                                p1.session as "session_id",
                                p1.tenant,
                                p1.channel,
                                p3.agent,
                                p1.timestamp
                        from ' || schemaName || '.analytics_socialevent p1
                        inner join ' || schemaName || '.socialconversation_tempsocialuser p2
                        on p1.social_id = p2.id and p1.tenant = p2.tenant
                        left join (select  t2.agent_id,
                                            t1.username as "agent",
                                            t3.tenant_name as "tenant"
                                    from ' || schemaName || '.socialconversation_agent t1
                                    inner join ' || schemaName || '.socialconversation_agenttenant t2
                                    on t1.id = t2.agent_id
                                    inner join ' || schemaName || '.socialconversation_tenant t3
                                    on t2.tenant_id = t3.id) as p3
                        on p3.agent_id = p1.agent_id and p3.tenant = p1.tenant
                        where event in (''handoff-initial'',''handoff-notification'',''agent-accept'')
                        order by p2.username,p1.timestamp),
                acceptTime AS (
                    SELECT
                        session_id,
                        TO_CHAR(
                            (EXTRACT(EPOCH FROM MAX(timestamp) - MIN(timestamp)) * INTERVAL ''1 second'')::interval,
                            ''HH24:MI:SS''
                        ) AS "accept_time"
                    FROM
                        events
                    WHERE
                        events.event IN (''handoff-initial'', ''agent-accept'')
                    GROUP BY
                        session_id
                ),
                initialTime as (select session_id, timestamp as "initial_time" from events where events.event in (''handoff-initial'')),
                productivity as (select ROW_NUMBER() OVER () as id,username,
                                     array(select distinct x.agent from events x where x.session_id = events.session_id and x.event in (''handoff-notification'')) as "agent_routed",
                                     events.session_id,
                                     channel,
                                     array(select distinct y.agent from events y where y.session_id = events.session_id and y.event in (''agent-accept'')) as "agent_accept",
                                     "accept_time",
                                     "initial_time",
                                     tenant
                                     from events
                                     inner join acceptTime
                                     on events.session_id = acceptTime.session_id
                                     inner join initialTime
                                     on events.session_id = initialTime.session_id
                                     where events.event in (''handoff-notification'')
                                     group by username,"agent_routed",events.session_id,channel,"agent_accept","accept_time","initial_time",tenant
                                     )select * from productivity;

                drop view if exists ' || schemaName || '.agent_transfer cascade;

                create or replace view ' || schemaName || '.agent_transfer as
                with events as(select p2.username,
                       p1.timestamp,
                       p1.event,
                       p1.parent_session_id,
                       p3.agent,
                       p1.channel,
                       p2.tenant
                from ' || schemaName || '.analytics_socialevent p1
                inner join ' || schemaName || '.socialconversation_tempsocialuser p2
                on p1.social_id = p2.id
                left join (select t1.username as agent,
                       t1.id as agentid,
                       t3.tenant_name as tenant
                from ' || schemaName || '.socialconversation_agent t1
                inner join ' || schemaName || '.socialconversation_agenttenant t2
                on t1.id=t2.agent_id
                inner join ' || schemaName || '.socialconversation_tenant t3
                on t2.tenant_id=t3.id) as p3
                on p1.agent_id = p3.agentid and p2.tenant = p3.tenant
                where p1.event in (''handoff-initial'',''handoff-transfer-from '',''handoff-transfer-to'',''agent-accept'',''user-cancel-routing'',''agent-force-end'',''user-inactive'',''agent-end-confirm'',''user-end-confirm'')
                and parent_session_id <> ''''),
                totalSession as(select parent_session_id, TO_CHAR(
                            (EXTRACT(EPOCH FROM MAX(timestamp) - MIN(timestamp)) * INTERVAL ''1 second'')::interval,
                            ''HH24:MI:SS''
                        ) as Total_session  from events where event in (''handoff-initial'',''agent-end-confirm'',''user-end-confirm'',''agent-force-end'',''user-inactive'') group by parent_session_id),
                initialtime as (select parent_session_id, timestamp as initial_time from events where event=''handoff-initial'' group by parent_session_id,timestamp),
                accepttime as (select parent_session_id, timestamp as accept_time from events where event=''agent-accept'' group by parent_session_id, timestamp)
                select ROW_NUMBER() OVER () as id,
                       e.parent_session_id,
                    e.username,
                    array(select agent
                             from events s
                             where s.event in (''handoff-transfer-to'') and s.parent_session_id = e.parent_session_id)
                             as transferred_agents,
                    array(select distinct agent
                             from events x
                             where x.event in (''agent-accept'')
                              and x.parent_session_id = e.parent_session_id) as initial_agent,
                       ts.Total_session as total_session,
                       it.initial_time,
                       at.accept_time,
                    e.channel,
                    e.tenant
                from events e
                left join totalSession ts
                on e.parent_session_id = ts.parent_session_id
                left join accepttime at
                on e.parent_session_id = at.parent_session_id
                left join initialtime it
                on e.parent_session_id = it.parent_session_id
                group by e.parent_session_id,e.username, ts.total_session, it.initial_time, at.accept_time, e.channel, e.tenant;

                drop view if exists ' || schemaName || '.handoff_flow cascade;

                create or replace view ' || schemaName || '.handoff_flow as
                select ROW_NUMBER() OVER () as id,flow.session_id, LAG(flow.events, 1) over (PARTITION by session_id order by timestamp) as source, flow.events as target, flow.channel, flow.timestamp, flow.tenant
                from (select distinct(event) as events,parent_session_id as session_id,channel,min(timestamp) as timestamp,tenant
                       from ' || schemaName || '.analytics_socialevent
                       where parent_session_id <> ''''
                       and event not like ''%transfer%'' and event not like ''%note%'' and event not in (''agent-end-trigger'',''social-message'',''chat-message'')
                       group by events,session_id,channel,tenant
                       order by session_id,timestamp) as flow;
                ';
            EXECUTE sqlQuery;
        else
            continue;
        end if;
    END LOOP;
END
$$;