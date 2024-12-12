-- DDL Generated from https:/databasediagram.com
CREATE DATABASE RAJDISTRIBUTORS_DATABASE;
-- RAJdISTRIBUTORS_DATABASE CREATED
USE RAJDISTRIBUTORS_DATABASE;

CREATE TABLE dealer (
  dealer_id varchar(50) PRIMARY KEY NOT NULL,
  company_name varchar(255) NOT NULL,
  name_agent VARCHAR(50) NOT NULL,
  gst varchar(16) NOT NULL,
  ACOUNT_NO VARCHAR(50) NOT NULL,
  ifsc_NO VARCHAR(50) NOT NULL,
  bank VARCHAR(50) NOT NULL,
  branch VARCHAR(50) NOT NULL,
  mobile VARCHAR (15)NOT NULL,
  email varchar(255),
FOREIGN KEY (dealer_id) REFERENCES Trasportation(dearler_id),
FOREIGN KEY (dealer_id) REFERENCES buy(dealer_id),
FOREIGN KEY (dealer_id) REFERENCES item(dealerid)
);

CREATE TABLE shop (
  id integer PRIMARY KEY AUTO_INCREMENT,
  username varchar(255) NOT NULL,
  password varchar(255)NOT NULL,
  gst varchar(16)NOT NULL,
  mobile integer(15)NOT NULL,
  email varchar(60)NOT NULL,
  raw_data_temp text NOT NULL,
  role varchar(40)NOT NULL,
  debit DECIMAL(10,2) DEFAULT 0,
  credit DECIMAL(10,2) DEFAULT 0,
  on_bill_payment_retail DECIMAL(10,2) DEFAULT 0,
  SPEND DECIMAL(10,2) DEFAULT 0
);

CREATE TABLE Customer (
  cust_id varchar(60) PRIMARY KEY NOT NULL,
  person_name VARCHAR(100) NOT NULL,
  mobile integer(16),
  location varchar(255),
  cust_type ENUM('WHOLE_SALE','RETAIL_SALE'),
FOREIGN KEY (cust_id) REFERENCES sell_retail(custid),
FOREIGN KEY (cust_id) REFERENCES sell_wholesale(custid),
FOREIGN KEY (cust_id) REFERENCES collection(custid),
FOREIGN KEY (cust_id) REFERENCES temp_invoice_data(cust_id)
);

CREATE TABLE Trasportation (
  transportation_id varchar(150) PRIMARY KEY NOT NULL,
  sender_transport_name varchar(255) NOT NULL,
  gr_no_s VARCHAR(50) NOT NULL,
  recieving_transport_name varchar(255)NOT NULL,
  gr_no_r VARCHAR(50) NOT NULL,
  nag int NOT NULL,
  charge DECIMAL(10,2),
  dearler_id varchar(50)
);

CREATE TABLE buy (
  id BIGINT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  invoice_number varchar(255),
  invoice_date date,
  amount DECIMAL(10,2),
  dealer_id varchar(50),
  status ENUM('PAID','UNPAID')
);

CREATE TABLE sell_retail (
  invoice_no varchar(255) PRIMARY KEY NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  sell_time timestamp NOT NULL,
  custid varchar(60) NOT NULL
);

CREATE TABLE sell_wholesale (
  invoice_no varchar(255) PRIMARY KEY NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  remark TEXT ,
  sell_time timestamp NOT NULL,
  pdf BLOB NOT NULL,
  days INTEGER DEFAULT 0 NOT NULL,
  custid varchar(60) NOT NULL,
  sell_wholesale_status ENUM('PAID','UNPAID') NOT NULL
);

CREATE TABLE employ (
  emp_id varchar(60) PRIMARY KEY NOT NULL,
  emp_name varchar(100) NOT NULL,
  mobile INTEGER(16)NOT NULL,
  location varchar(255)NOT NULL,
  salary DECIMAL(10,2)NOT NULL,
  stardate date NOT NULL,
  enddate date NOT NULL,
  advance DECIMAL(10,2) NOT NULL,
  balance DECIMAL(10,2) NOT NULL
);

CREATE TABLE spend (
  spend_id INT AUTO_INCREMENT PRIMARY KEY ,
  spend_type ENUM('REPAIR','EMPLOYEE TOOL','LEGAL AND PROFESSINAL EXPENSES','OFFICE EXPENSES AND SUPPLIES','UTILITIES','PRINITING','RENT','SALARIES AND OTHER COMPENSATION','TRAVEL','CLIENT GIFT') NOT NULL,
  description_SPEND TEXT NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  paid_by VARCHAR(255) NOT NULL,
  TIME_SPEND DATETIME NOT NULL
);

CREATE TABLE item (
  item_id varchar(100) PRIMARY KEY NOT NULL,
  item_description text NOT NULL,
  item_buy_rate DECIMAL(10,2) NOT NULL,
  gst_percentage DECIMAL(3,1)NOT NULL,
  profit_retail DECIMAL(10,2)NOT NULL,
  profilt_wholesale  DECIMAL(10,2)NOT NULL,
  sudo_rate DECIMAL(10,2)NOT NULL,
  unit VARCHAR(100) NOT NULL,
  dealerid varchar(60)NOT NULL,
  stock BIGINT NOT NULL,
  reorder_level INT NOT NULL,
FOREIGN KEY (item_id) REFERENCES temp_invoice_data(item_id)
);

CREATE TABLE collection (
  payment_id VARCHAR(100) PRIMARY KEY NOT NULL,
  amount DECIMAL(10,2),
  custid varchar(60),
  remark TEXT,
  collection_date date,
  collected varchar(255)
);

CREATE TABLE temp_invoice_data (
  cust_id varchar(60),
  item_id varchar(100)
);

CREATE TABLE Visiting_shop (
  cust_id varchar(60) PRIMARY KEY not null,
 --  visiting integer not null,
  visitingdate date NOT NULL,
  amount integer not null,   -- for only retail person 
FOREIGN KEY (cust_id) REFERENCES Customer(cust_id)
);

CREATE TABLE payment (
  payment_id varchar(255) PRIMARY KEY NOT NULL,
  pay_date datetime NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  dealer_id varchar(255) NOT NULL,
FOREIGN KEY (dealer_id) REFERENCES dealer(dealer_id)
);
-- REMAINING TABLE CHECK OSVER THAT 
CREATE TABLE sales (
  sale_id integer PRIMARY KEY NOT NULL,
  sale_date date NOT NULL,
  cust_id varchar(60),
  total_amount decimal(10,2) NOT NULL,
FOREIGN KEY (cust_id) REFERENCES Customer(cust_id),
FOREIGN KEY (sale_id) REFERENCES salesDetails(sale_id)
);

CREATE TABLE salesDetails (
sale__id BIGINT PRIMARY KEY AUTO_INCREMENT ,
sal_id integer NOT NULL,
item_id varchar(100) NOT NULL,
quantity integer NOT NULL,
price Decimal(10,2) NOT NULL,
FOREIGN KEY (item_id) REFERENCES item(item_id)
);
