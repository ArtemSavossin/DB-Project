--for postgres
-- DROP DATABASE "ESM";
CREATE TABLE Managers (
    id_Manager SERIAL PRIMARY KEY,
    FirstName TEXT,
    Surname TEXT,
    phone_number TEXT NOT NULL UNIQUE,
    orders_closed INTEGER
);

CREATE TABLE Customers (
    id_customer SERIAL PRIMARY KEY,
    FirstName TEXT,
    Surname TEXT,
    phone_number TEXT NOT NULL UNIQUE,
    city TEXT,
    street TEXT,
    email TEXT UNIQUE
);


CREATE TABLE Orders (
    id_order SERIAL PRIMARY KEY,
    created_time timestamp,
    payment_time timestamp,
    total_cost INTEGER,
    is_Finished INTEGER,
    id_customer INTEGER,
    id_manager INTEGER,
    FOREIGN KEY (id_customer) REFERENCES Customers(id_customer) ON DELETE RESTRICT,
    FOREIGN KEY (id_manager) REFERENCES Managers(id_manager) ON DELETE RESTRICT
);

CREATE TABLE Items (
    id_item SERIAL PRIMARY KEY,
    cost INTEGER,
    articul TEXT,
    id_Manager INTEGER,
    FOREIGN KEY (id_Manager) REFERENCES Managers(id_manager) ON DELETE RESTRICT
);


CREATE TABLE Yarn (
    id_yarn SERIAL PRIMARY KEY,
    material TEXT,
    color TEXT,
    length_m REAL,
	id_item INTEGER,
    FOREIGN KEY (id_item) REFERENCES Items(id_item) ON DELETE RESTRICT
);

CREATE TABLE Goods (
    id_good SERIAL PRIMARY KEY,
    goodName TEXT,
    textDescript TEXT,
    id_item INTEGER,
    FOREIGN KEY (id_item) REFERENCES Items(id_item) ON DELETE RESTRICT
);

CREATE TABLE Storages (
    id_storage SERIAL PRIMARY KEY,
    city TEXT,
    street TEXT,
    capacity INTEGER,
    avialable_place INTEGER
);

CREATE TABLE Storage_item (
    amount INTEGER,
    id_storage INTEGER NOT NULL,
    id_item INTEGER NOT NULL,
    FOREIGN KEY (id_storage) REFERENCES Storages(id_storage),
    FOREIGN KEY (id_item) REFERENCES Items(id_item)
);

CREATE TABLE Order_item (
    amount INTEGER DEFAULT 1,
    id_order INTEGER,
    id_item INTEGER,
    FOREIGN KEY (id_order) REFERENCES Orders(id_order),
    FOREIGN KEY (id_item) REFERENCES Items(id_item)
);
