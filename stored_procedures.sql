CREATE OR REPLACE FUNCTION get_order_items (ind INT) 
    RETURNS TABLE (
        articul TEXT,
        amount INT,
	total_cost INT
)
AS $$
BEGIN
    RETURN QUERY SELECT
        items.articul,
        order_item.amount,
	order_item.amount * items.cost AS total_cost
    FROM
        orders JOIN order_item ON order_item.id_order = orders.id_order JOIN items ON order_item.id_item = items.id_item
    WHERE
        orders.id_order = ind;
END; $$ 

LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION get_storage_items (ind INT) 
    RETURNS TABLE (
        articul TEXT,
        amount INT
)
AS $$
BEGIN
    RETURN QUERY SELECT
        items.articul,
        storage_item.amount
    FROM
        storages JOIN storage_item ON storage_item.id_storage = storages.id_storage JOIN items ON storage_item.id_item = items.id_item
    WHERE
        storages.id_storage = ind;
END; $$ 

LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION count_item_everywhere (INT) 
    RETURNS INT
AS $$
BEGIN
    RETURN 
	SUM(storage_item.amount)
    FROM
        storages JOIN storage_item ON storage_item.id_storage = storages.id_storage JOIN items ON storage_item.id_item = items.id_item
    WHERE
        items.id_item = $1;
END; $$ 

LANGUAGE 'plpgsql'
