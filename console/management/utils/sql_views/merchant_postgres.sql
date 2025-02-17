drop view if exists ${DB_SCHEMA_analytics}.merchant_hierarchy cascade;
CREATE OR REPLACE VIEW ${DB_SCHEMA_analytics}.merchant_hierarchy AS
WITH NodeWithChildren AS (
    SELECT
        nm1.node_id AS parent_node_id,
        nm1.node_name AS parent_node_name,
        nm1.level_id AS parent_level_id,
        ARRAY_AGG(nm2.node_id) AS child_ids
    FROM
        merchant.merchant_users_nodemaster nm1
    LEFT JOIN
        merchant.merchant_users_nodemaster nm2 ON nm1.node_id = nm2.parent_node_id
    GROUP BY
        nm1.node_id, nm1.node_name, nm1.level_id
)

SELECT
    nwc.parent_node_id AS node_id,
    nwc.parent_node_name AS node_name,
    nwc.parent_level_id AS level_id,
    nwc.child_ids AS node_id_of_children
FROM
    NodeWithChildren nwc
ORDER BY
    nwc.parent_level_id;