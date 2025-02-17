drop view if exists ${DB_SCHEMA_etbprovider}.etb_user_details;
create view ${DB_SCHEMA_etbprovider}.etb_user_details as
SELECT row_number() OVER () AS id, CAST(users_userdetails.user_details::json ->> 'account_number' AS CHARACTER VARYING) AS account_number,
       users_user.mobile_number::CHARACTER VARYING AS mobile_number,
        users_user.date_joined as timestamp,
       users_user.is_active
FROM etbprovider.users_user
JOIN etbprovider.users_userdetails ON users_user.user_details_id = users_userdetails.id;
