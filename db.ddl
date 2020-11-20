/*FOR SQLite*/

CREATE TABLE Managers (
    id_Manager INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName TEXT,
    Surname TEXT,
    phone_number TEXT NOT NULL UNIQUE,
    orders_closed INTEGER
);

CREATE TABLE Customers (
    id_customer INTEGER PRIMARY KEY AUTOINCREMENT ,
    FirstName TEXT,
    Surname TEXT,
    phone_number TEXT NOT NULL UNIQUE,
    city TEXT,
    street TEXT,
    email TEXT UNIQUE
);


CREATE TABLE Orders (
    id_order INTEGER PRIMARY KEY AUTOINCREMENT ,
    created_time TEXT,
    payment_time TEXT,
    total_cost INTEGER,
    is_Finished INTEGER,
    id_customer INTEGER,
    id_manager INTEGER,
    FOREIGN KEY (id_customer) REFERENCES Customers(id_customer) ON DELETE RESTRICT,
    FOREIGN KEY (id_manager) REFERENCES Managers(id_manager) ON DELETE RESTRICT
);

CREATE TABLE Items (
    id_item INTEGER PRIMARY KEY AUTOINCREMENT,
    cost INTEGER,
    articul TEXT,
    id_Manager INTEGER,
    FOREIGN KEY (id_Manager) REFERENCES Managers(id_manager) ON DELETE RESTRICT
);


CREATE TABLE Yarn (
    id_yarn INTEGER PRIMARY KEY AUTOINCREMENT,
    material TEXT,
    color TEXT,
    length_m REAL,
	id_item INTEGER,
    FOREIGN KEY (id_item) REFERENCES Items(id_item) ON DELETE RESTRICT
);

CREATE TABLE Goods (
    id_good INTEGER PRIMARY KEY AUTOINCREMENT ,
    goodName TEXT,
    textDescript TEXT,
    id_item INTEGER,
    FOREIGN KEY (id_item) REFERENCES Items(id_item) ON DELETE RESTRICT
);

CREATE TABLE Storages (
    id_storage INTEGER PRIMARY KEY AUTOINCREMENT,
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
