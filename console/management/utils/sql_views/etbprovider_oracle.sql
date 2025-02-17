CREATE OR REPLACE VIEW ${DB_SCHEMA_etbprovider}.etb_user_details
       AS
SELECT ROW_NUMBER()                         OVER (ORDER BY ${DB_SCHEMA_etbprovider}.users_userdetails.id) AS id, CAST(
        JSON_VALUE(${DB_SCHEMA_etbprovider}.users_userdetails.user_details, '$.account_number') AS VARCHAR2 (100)) AS account_number,
       TO_CHAR(${DB_SCHEMA_etbprovider}.users_user.mobile_number) AS mobile_number,
       ${DB_SCHEMA_etbprovider}.users_user.date_joined AS timestamp, CASE WHEN ${DB_SCHEMA_etbprovider}.users_user.is_active = 1 THEN 1 ELSE 0 END AS is_active
FROM ${DB_SCHEMA_etbprovider}.users_user JOIN ${DB_SCHEMA_etbprovider}.users_userdetails
ON ${DB_SCHEMA_etbprovider}.users_user.user_details_id = ${DB_SCHEMA_etbprovider}.users_userdetails.id;