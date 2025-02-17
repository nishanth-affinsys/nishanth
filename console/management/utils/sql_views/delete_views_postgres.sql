DO $do$
DECLARE
    x text;
BEGIN
    FOR x IN (select 'DROP VIEW ' || table_schema || '.' || table_name || ' CASCADE;' as drop_views
              from information_schema.views
              WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
                AND table_name !~ '^pg_') LOOP
        EXECUTE x;
    END LOOP;
END;
$do$;