
CREATE DATABASE ESM;

USE ESM;

CREATE TABLE Managers (
    id_Manager INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50),
    Surname VARCHAR(50),
    phone_number INT NOT NULL UNIQUE,
    orders_closed INT
);

CREATE TABLE Customers (
    id_customer INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50),
    Surname VARCHAR(50),
    phone_number INT NOT NULL UNIQUE,
    city VARCHAR(50),
    street VARCHAR(50),
    email VARCHAR(100) UNIQUE
);


CREATE TABLE Orders (
    id_order INT PRIMARY KEY AUTO_INCREMENT,
    created_time TIMESTAMP,
    payment_time TIMESTAMP,
    total_cost INT,
    is_Finished BIT,
    id_customer INT,
    id_manager INT,
    FOREIGN KEY (id_customer) REFERENCES Customers(id_customer) ON DELETE RESTRICT,
    FOREIGN KEY (id_manager) REFERENCES Managers(id_manager) ON DELETE RESTRICT
);

CREATE TABLE Items (
    id_item INT PRIMARY KEY AUTO_INCREMENT,
    cost INT,
    articul VARCHAR(100),
    id_Manager INT,
    FOREIGN KEY (id_Manager) REFERENCES Managers(id_manager) ON DELETE RESTRICT
);


CREATE TABLE Yarn (
    id_yarn INT PRIMARY KEY AUTO_INCREMENT,
    material VARCHAR(50),
    color VARCHAR(50),
    length_m FLOAT,
	id_item INT,
    FOREIGN KEY (id_item) REFERENCES Items(id_item) ON DELETE RESTRICT
);

CREATE TABLE Goods (
    id_good INT PRIMARY KEY AUTO_INCREMENT,
    goodName VARCHAR(50),
    textDescript VARCHAR(2000),
    id_item INT,
    FOREIGN KEY (id_item) REFERENCES Items(id_item) ON DELETE RESTRICT
);

CREATE TABLE Storages (
    id_storage INT PRIMARY KEY AUTO_INCREMENT,
    city VARCHAR(100),
    street VARCHAR(100),
    capacity INT,
    avialable_place INT
);

CREATE TABLE Storage_item (
    amount INT,
    id_storage INT,
    id_item INT,
    FOREIGN KEY (id_storage) REFERENCES Storages(id_storage),
    FOREIGN KEY (id_item) REFERENCES Items(id_item)
);

CREATE TABLE Order_item (
    amount INT,
    id_order INT,
    id_item INT,
    FOREIGN KEY (id_order) REFERENCES Orders(id_order),
    FOREIGN KEY (id_item) REFERENCES Items(id_item)
);
