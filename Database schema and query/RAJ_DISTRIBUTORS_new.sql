-- Drop and Create Database
DROP DATABASE IF EXISTS RAJDISTRIBUTORS_DATABASE;
CREATE DATABASE RAJDISTRIBUTORS_DATABASE;
USE RAJDISTRIBUTORS_DATABASE;

-- Step 1: Independent Tables
-- Shop
CREATE TABLE shop (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  gst VARCHAR(16) NOT NULL,
  mobile VARCHAR(15) NOT NULL,
  email VARCHAR(60) NOT NULL,
  raw_data_temp TEXT NOT NULL,
  role VARCHAR(40) NOT NULL,
  debit DECIMAL(10,2) not null,
  credit DECIMAL(10,2) not null,
  on_bill_payment_retail DECIMAL(10,2) not null,
  SPEND DECIMAL(10,2) not null
);

-- Spend Table
CREATE TABLE spend (
  spend_id INT PRIMARY KEY AUTO_INCREMENT,
  spend_type ENUM('REPAIR', 'EMPLOYEE TOOL', 'LEGAL AND PROFESSIONAL EXPENSES', 'OFFICE EXPENSES AND SUPPLIES', 'UTILITIES', 'PRINTING', 'RENT', 'SALARIES AND OTHER COMPENSATION', 'TRAVEL', 'CLIENT GIFT') NOT NULL,
  description_SPEND TEXT NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  paid_by VARCHAR(255) NOT NULL,
  TIME_SPEND DATETIME NOT NULL
);

-- Dealer Table
CREATE TABLE dealer (
  dealer_id VARCHAR(50) PRIMARY KEY NOT NULL,
  company_name VARCHAR(255) NOT NULL,
  name_agent VARCHAR(50) NOT NULL,
  gst VARCHAR(16) NOT NULL,
  ACOUNT_NO VARCHAR(50) NOT NULL,
  ifsc_NO VARCHAR(50) NOT NULL,
  bank VARCHAR(50) NOT NULL,
  branch VARCHAR(50) NOT NULL,
  mobile VARCHAR(15) NOT NULL,
  email VARCHAR(255)
);

-- Customer Table
CREATE TABLE Customer (
  cust_id VARCHAR(60) PRIMARY KEY NOT NULL,
  person_name VARCHAR(100) NOT NULL,
  mobile VARCHAR(16),
  location VARCHAR(255),
  cust_type ENUM('WHOLE_SALE', 'RETAIL_SALE') NOT NULL
);

-- Employee Table
CREATE TABLE employ (
  emp_id VARCHAR(60) PRIMARY KEY NOT NULL,
  emp_name VARCHAR(100) NOT NULL,
  mobile VARCHAR(16) NOT NULL,
  location VARCHAR(255) NOT NULL,
  salary DECIMAL(10,2) NOT NULL,
  stardate DATE NOT NULL,
  enddate DATE,
  advance DECIMAL(10,2) DEFAULT 0,
  balance DECIMAL(10,2) DEFAULT 0
);

-- Step 2: Dependent Tables
-- Item Table
CREATE TABLE item (
  item_id VARCHAR(100) PRIMARY KEY NOT NULL,
  item_description TEXT NOT NULL,
  item_buy_rate DECIMAL(10,2) NOT NULL,
  gst_percentage DECIMAL(3,1) NOT NULL,
  profit_retail DECIMAL(10,2) NOT NULL,
  profit_wholesale DECIMAL(10,2) NOT NULL,
  sudo_rate DECIMAL(10,2) NOT NULL,
  unit VARCHAR(100) NOT NULL,
  dealer_id VARCHAR(60) NOT NULL,
  stock BIGINT NOT NULL,
  reorder_level INT NOT NULL,
  FOREIGN KEY (dealer_id) REFERENCES dealer(dealer_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Collection Table
CREATE TABLE collection (
  payment_id VARCHAR(100) PRIMARY KEY NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  cust_id VARCHAR(60) NOT NULL,
  remark TEXT,
  collection_date DATE NOT NULL,
  collected VARCHAR(255) NOT NULL,
  FOREIGN KEY (cust_id) REFERENCES Customer(cust_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Transportation Table
CREATE TABLE Transportation (
  transportation_id VARCHAR(150) PRIMARY KEY NOT NULL,
  invoice_number VARCHAR(150) NOT NULL,
  sender_transport_name VARCHAR(255) NOT NULL,
  gr_no_s VARCHAR(50) NOT NULL,
  receiving_transport_name VARCHAR(255) NOT NULL,
  gr_no_r VARCHAR(50) NOT NULL,
  nag INT NOT NULL,
  charge DECIMAL(10,2),
  dealer_id VARCHAR(50),
  FOREIGN KEY (dealer_id) REFERENCES dealer(dealer_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Payment Table
CREATE TABLE payment (
  payment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  pay_date DATETIME NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  dealer_id VARCHAR(255) NOT NULL,
  remark TEXT,
  FOREIGN KEY (dealer_id) REFERENCES dealer(dealer_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Temporary Invoice Data
CREATE TABLE temp_invoice_data (
  cust_id VARCHAR(60),
  item_id VARCHAR(100),
  FOREIGN KEY (cust_id) REFERENCES Customer(cust_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (item_id) REFERENCES item(item_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Buy Table
CREATE TABLE buy (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  invoice_number VARCHAR(255),
  invoice_date DATE,
  amount DECIMAL(10,2),
  dealer_id VARCHAR(50),
  status ENUM('PAID', 'UNPAID'),
  FOREIGN KEY (dealer_id) REFERENCES dealer(dealer_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Sell Retail Table
CREATE TABLE sell_retail (
  invoice_no VARCHAR(255) PRIMARY KEY NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  sell_time TIMESTAMP NOT NULL,
  cust_id VARCHAR(60) NOT NULL,
  FOREIGN KEY (cust_id) REFERENCES Customer(cust_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Sell Wholesale Table
CREATE TABLE sell_wholesale (
  invoice_no VARCHAR(255) PRIMARY KEY NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  remark TEXT,
  sell_time TIMESTAMP NOT NULL,
  pdf BLOB NOT NULL,
  days INT DEFAULT 0,
  cust_id VARCHAR(60) NOT NULL,
  sell_wholesale_status ENUM('PAID', 'UNPAID') NOT NULL,
  FOREIGN KEY (cust_id) REFERENCES Customer(cust_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Sales Table
CREATE TABLE sales (
  sale_id INT PRIMARY KEY AUTO_INCREMENT,
  sale_date DATE NOT NULL,
  cust_id VARCHAR(60),
  total_amount DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (cust_id) REFERENCES Customer(cust_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Sales Details Table
CREATE TABLE salesDetails (
  sale_details_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  sale_id INT NOT NULL,
  item_id VARCHAR(100) NOT NULL,
  quantity INT NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (sale_id) REFERENCES sales(sale_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (item_id) REFERENCES item(item_id) ON DELETE CASCADE ON UPDATE CASCADE
);
