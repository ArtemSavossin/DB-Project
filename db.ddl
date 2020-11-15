CREATE DATABASE ESM;

CREATE TABLE Managers (
    id_Manager INT PRIMARY KEY,
    name VARCHAR(50),
    Surname VARCHAR(50),
    phone_number INT,
    orders_closed INT
);

CREATE TABLE Customers (
    id_customer INT PRIMARY KEY,
    name VARCHAR(50),
    Surname VARCHAR(50),
    phone_number INT,
    city VARCHAR(50),
    street VARCHAR(50),
    email VARCHAR(100),
);

CREATE TABLE Oders (
    id_order INT PRIMARY KEY,
    created_time DATETIME,
    payment_time DATETIME,
    total_cost INT,
    is_Finished BIT,
    FOREIGN KEY (id_customer) REFERENCES Customers(id_customer),
    FOREIGN KEY (id_manager) REFERENCES Managers(id_manager)
);

CREATE TABLE Items (
    id_item INT PRIMARY KEY,
    cost INT,
    code VARCHAR(100),
    FOREIGN KEY (id_Manager) REFERENCES Managers(id_manager)
);


CREATE TABLE Yarn (
    id_order INT PRIMARY KEY,
    material VARCHAR(50),
    color VARCHAR(50),
    length_m FLOAT,
    FOREIGN KEY (id_item) REFERENCES Items(id_item)
);

CREATE TABLE Goods (
    id_good INT PRIMARY KEY,
    name VARCHAR(50),
    description VARCHAR(2000),
    FOREIGN KEY (id_item) REFERENCES Items(id_item)
);

CREATE TABLE Storages (
    id_storage INT PRIMARY KEY,
    city VARCHAR(100),
    street VARCHAR(100),
    capacity INT,
    avialable_place INT,
);

CREATE TABLE Storage_item (
    amount INT,
    FOREIGN KEY (id_storage) REFERENCES Storages(id_storage),
    FOREIGN KEY (id_item) REFERENCES Items(id_item)
);

CREATE TABLE Order_item (
    amount INT,
    FOREIGN KEY (id_order) REFERENCES Orders(id_order),
    FOREIGN KEY (id_item) REFERENCES Items(id_item)
);
