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

CREATE OR REPLACE FUNCTION items_sold_by_manager () 
    RETURNS TABLE (
        surname TEXT,
        amount bigint
)
AS $$
BEGIN
    RETURN QUERY 
	SELECT managers.surname as surname, SUM(order_item.amount) as amount FROM managers
	JOIN items ON managers.id_manager = items.id_manager
	JOIN order_item ON items.id_item = order_item.id_item
	GROUP BY managers.surname;
END; $$ 

LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION items_sold () 
    RETURNS TABLE (
        surname TEXT,
        amount bigint
)
AS $$
BEGIN
    RETURN QUERY 
	SELECT items.articul, SUM(order_item.amount) FROM items
	JOIN order_item ON items.id_item = order_item.id_item
	GROUP BY items.articul;
END; $$ 

LANGUAGE 'plpgsql';
