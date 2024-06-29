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
    c_contact VARCHAR(15)
    );
CREATE TABLE IF NOT EXISTS Staff(
    s_ID SERIAL PRIMARY KEY, 
    s_name VARCHAR(100) NOT NULL, 
    s_email VARCHAR(100) NOT NULL UNIQUE, 
    s_isAdmin BOOLEAN NOT NULL, 
    s_contact VARCHAR(15)
    );
CREATE TABLE IF NOT EXISTS Transaction(
    t_ID SERIAL PRIMARY KEY,
    c_ID INT REFERENCES Customer(c_ID),
    s_ID INT REFERENCES Staff(s_ID),
    Item_SKU INT REFERENCES InventoryItem(Item_SKU),
    t_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    t_amount NUMERIC(10, 2) NOT NULL,
    t_category VARCHAR(50)
    );
CREATE INDEX IF NOT EXISTS idx_item_sku ON InventoryItem(Item_SKU);
CREATE INDEX IF NOT EXISTS idx_customer_email ON Customer(c_email);
