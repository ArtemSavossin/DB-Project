
CREATE OR REPLACE FUNCTION order_cost_count_trg()
RETURNS trigger AS
$$
BEGIN
	UPDATE orders SET total_cost = (SELECT SUM(cost  * amount) FROM Order_item JOIN Items ON Items.id_item = Order_item.id_item 
	WHERE order_item.id_order = NEW.id_order) WHERE orders.id_order = new.id_order;
  RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER order_cost_count
  AFTER INSERT
  ON "order_item"
  FOR EACH ROW
  EXECUTE PROCEDURE order_cost_count_trg();

CREATE OR REPLACE FUNCTION order_cost_count_del_trg()
RETURNS trigger AS
$$
BEGIN
	UPDATE orders SET total_cost = (SELECT coalesce(SUM(cost  * amount),0) FROM Order_item JOIN Items ON Items.id_item = Order_item.id_item 
  WHERE order_item.id_order = old.id_order) WHERE orders.id_order = old.id_order;
  RETURN OLD;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER order_cost_count_del
  AFTER DELETE
  ON "order_item"
  FOR EACH ROW
  EXECUTE PROCEDURE order_cost_count_del_trg();

CREATE OR REPLACE FUNCTION order_cost_count_upd_trg()
RETURNS trigger AS
$$
BEGIN
	UPDATE orders SET total_cost = (SELECT SUM(cost  * amount) FROM Order_item JOIN Items ON Items.id_item = Order_item.id_item 
	WHERE order_item.id_order = NEW.id_order) WHERE orders.id_order = new.id_order;
  RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER order_cost_count_upd
  AFTER UPDATE
  ON "order_item"
  FOR EACH ROW
  EXECUTE PROCEDURE order_cost_count_upd_trg();

CREATE OR REPLACE FUNCTION storage_place_count_trg()
RETURNS trigger AS
$$
BEGIN
	UPDATE Storages SET avialable_place = (SELECT capacity - SUM(amount) FROM storage_item JOIN Items ON Items.id_item = storage_item.id_item 
  WHERE storage_item.id_storage = NEW.id_storage) WHERE Storages.id_storage = new.id_storage;
  RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';
 
CREATE TRIGGER storage_place_count
  AFTER INSERT
  ON "storage_item"
  FOR EACH ROW
  EXECUTE PROCEDURE storage_place_count_trg();

CREATE OR REPLACE FUNCTION storage_place_count_upd_trg()
RETURNS trigger AS
$$
BEGIN
	UPDATE Storages SET avialable_place = (SELECT capacity - SUM(amount) FROM storage_item JOIN Items ON Items.id_item = storage_item.id_item 
  WHERE storage_item.id_storage = NEW.id_storage) WHERE Storages.id_storage = new.id_storage;
  RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';
 
CREATE TRIGGER storage_place_count_upd
  AFTER UPDATE
  ON "storage_item"
  FOR EACH ROW
  EXECUTE PROCEDURE storage_place_count_upd_trg();

CREATE OR REPLACE FUNCTION storage_place_count_del_trg()
RETURNS trigger AS
$$
BEGIN
	UPDATE Storages SET avialable_place = (SELECT capacity - coalesce(SUM(amount),0) FROM Storage_item JOIN Items ON Items.id_item = Storage_item.id_item 
  WHERE storage_item.id_storage = old.id_storage) WHERE Storages.id_storage = old.id_storage;
  RETURN OLD;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER storage_place_count_del
  AFTER DELETE
  ON "storage_item"
  FOR EACH ROW
  EXECUTE PROCEDURE storage_place_count_del_trg();
  
CREATE OR REPLACE FUNCTION check_available_place_trg()
RETURNS trigger AS
$$
BEGIN
   IF (SELECT avialable_place FROM storages WHERE id_storage = NEW.id_storage) - NEW.amount < 0 
   THEN
      RAISE EXCEPTION 'No place for such amount';
   END IF;
   RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER check_available_place
  BEFORE INSERT
  ON "storage_item"
  FOR EACH ROW
  EXECUTE PROCEDURE check_available_place_trg();
  

CREATE OR REPLACE FUNCTION check_available_place_upd_trg()
RETURNS trigger AS
$$
BEGIN
   IF (SELECT avialable_place FROM storages WHERE id_storage = NEW.id_storage) - NEW.amount < 0 
   THEN
      RAISE EXCEPTION 'No place for such amount';
   END IF;
   RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER check_available_place_upd
  BEFORE UPDATE
  ON "storage_item"
  FOR EACH ROW
  EXECUTE PROCEDURE check_available_place_upd_trg();
