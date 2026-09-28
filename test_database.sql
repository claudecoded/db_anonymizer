-- Mock Production Database Dump Example
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20)
);

INSERT INTO users (id, username, email, phone) VALUES 
(1, 'alex_dev', 'alex.jones@corporate.com', '+1-555-987-6543'),
(2, 'sam_secure', 'sam.miller@provider.net', '555-123-4567');

CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY,
    user_id INT,
    card_number VARCHAR(25),
    amount DECIMAL(10,2)
);

INSERT INTO transactions (transaction_id, user_id, card_number, amount) VALUES 
(101, 1, '4111222233334444', 299.90),
(102, 2, '5155999988887777', 15.00);
