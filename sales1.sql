create database sales;
use sales;

CREATE TABLE customers (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150),
    city VARCHAR(50),
    created_at DATE
);

CREATE TABLE products (
    id INT PRIMARY KEY,
    name VARCHAR(150),
    category VARCHAR(50),
    price DECIMAL(10,2)
);

CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    order_status VARCHAR(20),
    total_amount DECIMAL(12,2),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE order_details (
    id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    subtotal DECIMAL(12,2),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

INSERT INTO customers (id, name, email, city, created_at) VALUES
(1, 'Ravi Kumar', 'ravi@gmail.com', 'Delhi', '2023-01-10'),
(2, 'Anita Sharma', 'anita@gmail.com', 'Mumbai', '2023-02-15'),
(3, 'Suresh Patel', 'suresh@gmail.com', 'Ahmedabad', '2023-03-20'),
(4, 'Neha Verma', 'neha@gmail.com', NULL, '2023-04-05'),
(5, 'Ravi Kumar', 'ravi@gmail.com', 'Delhi', '2023-01-10'), -- duplicate
(6, 'Karan Singh', 'karan@gmail.com', 'Pune', '2023-05-12'),
(7, 'Pooja Mehta', NULL, 'Jaipur', '2023-06-18'),
(8, 'Amit Roy', 'amit@gmail.com', 'Kolkata', '2023-07-01');
INSERT INTO products (id, name, category, price) VALUES
(1, 'iPhone 13', 'Mobile', 65000),
(2, 'Samsung Galaxy S21', 'Mobile', 55000),
(3, 'HP Laptop', 'Laptop', 58000),
(4, 'Dell Laptop', 'Laptop', NULL), -- missing price
(5, 'Sony TV 42"', 'TV', 42000),
(6, 'Boat Headphones', 'Accessories', 2500),
(7, 'Logitech Mouse', 'Accessories', 1200),
(8, 'Canon DSLR', 'Camera', 72000);
INSERT INTO orders (id, customer_id, order_date, order_status, total_amount) VALUES
(101, 1, '2023-07-05', 'paid', 67500),
(102, 2, '2023-07-08', 'delivered', 58000),
(103, 3, '2023-07-15', 'cancelled', 0),
(104, 4, '2023-08-02', 'paid', 42000),
(105, 1, '2023-08-10', 'delivered', 1250),
(106, 5, '2023-08-18', 'shipped', 65000),
(107, 6, '2023-09-01', 'paid', 72000),
(108, 7, '2023-09-12', 'returned', -2500), -- invalid
(109, 8, '2023-09-20', 'delivered', 55000),
(110, 2, '2023-10-05', 'paid', 58000);

INSERT INTO order_details (id, order_id, product_id, quantity, subtotal) VALUES
(1001, 101, 1, 1, 65000),
(1002, 101, 6, 1, 2500),

(1003, 102, 3, 1, 58000),

(1004, 103, 7, 2, 2400),

(1005, 104, 5, 1, 42000),

(1006, 105, 7, 1, 1200),
(1007, 105, 6, 1, 2500),

(1008, 106, 1, 1, 65000),

(1009, 107, 8, 1, 72000),

(1010, 108, 6, 1, -2500), -- wrong subtotal

(1011, 109, 2, 1, 55000),

(1012, 110, 3, 1, 58000);

SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM orders;
SELECT COUNT(*) FROM order_details;
