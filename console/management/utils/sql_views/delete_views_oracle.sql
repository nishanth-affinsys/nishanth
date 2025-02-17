DECLARE
    statement VARCHAR2(1000);
BEGIN
    FOR x IN (SELECT 'DROP VIEW ' || OWNER || '.' || view_name || ' CASCADE CONSTRAINTS' as drop_views
                from all_views
                WHERE owner = '${DB_ALIAS}') LOOP
        statement := x.drop_views;
        EXECUTE IMMEDIATE statement;
    END LOOP;
END;
