-- DDL Generated from https:/databasediagram.com

CREATE TABLE dealer (
  dealer_id varchar PRIMARY KEY,
  company_name varchar,
  name_agent name,
  gst varchar,
  ACOUNT_NO integer,
  IAFC_NO VARCHAR,
  BANK VARCHAR,
  BRANCH VARCHAR,
  mobile integer,
  email varchar,
  remaining_amount decimal(10,2),
FOREIGN KEY (dealer_id) REFERENCES Trasportation(dearler_id),
FOREIGN KEY (dealer_id) REFERENCES buy(dealer_id),
FOREIGN KEY (dealer_id) REFERENCES item(dealerid)
);

CREATE TABLE shop (
  id integer PRIMARY KEY,
  username varchar,
  password varchar2,
  gst varchar,
  mobile integer,
  email varchar,
  raw_data_temp varchar,
  role varchar,
  debit integer,
  credit integer,
  on_bill_payment_retail integer,
  SPEND integer
);

CREATE TABLE Customer (
  cust_id varchar PRIMARY KEY,
  name name,
  mobile integer,
  location varchar,
  type varchar,
FOREIGN KEY (cust_id) REFERENCES sell_retail(custid),
FOREIGN KEY (cust_id) REFERENCES sell_wholesale(custid),
FOREIGN KEY (cust_id) REFERENCES collection(custid),
FOREIGN KEY (cust_id) REFERENCES temp_invoice_data(cust_id)
);

CREATE TABLE Trasportation (
  transportation_id varchar PRIMARY KEY,
  sender_transport_name varchar,
  gr_no_s integer,
  recieving_transport_name varchar,
  gr_no_r integer,
  nag int,
  charge integer,
  dearler_id varchar
);

CREATE TABLE buy (
  id varchar PRIMARY KEY,
  invoice_number varchar,
  date date,
  amount integer,
  dealer_id varchar,
  status varchar
);

CREATE TABLE sell_retail (
  invoice_no varchar PRIMARY KEY,
  amount integer,
  time timestamp,
  custid varchar
);

CREATE TABLE sell_wholesale (
  invoice_no varchar PRIMARY KEY,
  amount integer,
  remark varchar,
  time timestamp,
  pdf BLOB,
  days number,
  custid varchar,
  status varchar
);

CREATE TABLE employ (
  emp_id varchar PRIMARY KEY,
  name name,
  mobile int,
  location varchar,
  salary integer,
  stardate date,
  enddate date,
  advance integer,
  balance integer
);

CREATE TABLE spend (
  spend_id INT,
  type ENUM,
  description VARCHAR,
  amount DECIMAL(10,2),
  paid_by VARCHAR,
  date date
);

CREATE TABLE item (
  item_id varchar PRIMARY KEY,
  item_description text,
  item_buy_rate integer,
  gst_percentage int,
  profit_retail integer,
  profilt_wholesale integer,
  sudo_rate integer,
  unit varchar,
  dealerid varchar,
  stock integer,
  reorder_level integer,
FOREIGN KEY (item_id) REFERENCES temp_invoice_data(item_id)
);

CREATE TABLE collection (
  payment_id varchar PRIMARY KEY,
  amount integer,
  custid varchar,
  remark varchar,
  date date,
  paid_by varchar
);

CREATE TABLE temp_invoice_data (
  cust_id varchar,
  item_id varchar
);

CREATE TABLE Visiting_shop (
  cust_id varchar PRIMARY KEY,
  visiting integer,
  date date,
  amount integer,
FOREIGN KEY (cust_id) REFERENCES Customer(cust_id)
);

CREATE TABLE payment (
  payment_id varchar PRIMARY KEY,
  date date,
  amount integer,
  dealer_id varchar,
FOREIGN KEY (dealer_id) REFERENCES dealer(dealer_id)
);

CREATE TABLE sales (
  sale_id integer PRIMARY KEY,
  sale_date date,
  cust_id varchar,
  total_amount decimal(10,2),
FOREIGN KEY (cust_id) REFERENCES Customer(cust_id),
FOREIGN KEY (sale_id) REFERENCES salesDetails(sale_id)
);

CREATE TABLE salesDetails (
  sale_detail_id Integer PRIMARY KEY,
  sale_id integer,
  item_id varchar,
  quantity integer,
  price Decimal(10,2),
FOREIGN KEY (item_id) REFERENCES item(item_id)
);
