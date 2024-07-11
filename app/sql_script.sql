CREATE TABLE IF NOT EXISTS InventoryItem(
    Item_SKU SERIAL PRIMARY KEY,
    Item_Name VARCHAR(100) NOT NULL,
    Item_Description TEXT,
    Item_Price NUMERIC(10, 2) NOT NULL , 
    Item_Qty INT NOT NULL
    );
CREATE TABLE IF NOT EXISTS Customer(
    c_ID SERIAL PRIMARY KEY, 
    c_name VARCHAR(100) NOT NULL,  
    c_email VARCHAR(100) NOT NULL UNIQUE, 
    c_password TEXT NOT NULL,
    c_contact VARCHAR(15),
    c_role VARCHAR NOT NULL,
    c_status VARCHAR(20) DEFAULT 'active'
    );
CREATE TABLE IF NOT EXISTS Staff(
    s_ID SERIAL PRIMARY KEY, 
    s_name VARCHAR(100) NOT NULL, 
    s_email VARCHAR(100) NOT NULL UNIQUE, 
    s_password TEXT NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE, 
    is_approved BOOLEAN NOT NULL DEFAULT FALSE,
    s_role VARCHAR NOT NULL,
    s_contact VARCHAR(15)
    
    );
CREATE TABLE IF NOT EXISTS Transaction(
    t_ID SERIAL PRIMARY KEY,
    c_ID INT REFERENCES Customer(c_ID),
    s_ID INT REFERENCES Staff(s_ID),
    -- product_amount_list JSONB,
    t_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    t_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    t_amount NUMERIC(10, 2) NOT NULL,
    t_category VARCHAR(50)
    );
-- CREATE TABLE IF NOT EXISTS Roles (
--     role_id SERIAL PRIMARY KEY,
--     role_name VARCHAR(20) NOT NULL UNIQUE
-- );
CREATE INDEX IF NOT EXISTS idx_item_sku ON InventoryItem(Item_SKU);
CREATE INDEX IF NOT EXISTS idx_customer_email ON Customer(c_email);
