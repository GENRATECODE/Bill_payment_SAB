create DATABASE bill_payment;
USE  bill_payment;
-- user table
CREATE TABLE user_table(
    user_id INT(11) AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phoneNumber VARCHAR(255) NOT NULL,
    flag char(50) NOT NULL,
    INDEX user_name_index (user_name)  -- Add index on user_name column
);

-- customer table

create table customer(
	cust_id char(255) not null primary key,
    cust_name varchar(255) not null,
    mobile_no int(10) not null,
    cust_address varchar(255) not null
);

-- purchase_buyer_id

CREATE TABLE purchase_person(
    purchase_buyer_id  varchar(15) not null PRIMARY KEY,
    buyer_name  varchar(50) not null,
    buyer_mobile int(10) not null,
    buyer_email   varchar(255) not null,
    bill_no varchar(255) not null,
    bank_account  VARCHAR(255) not null
    
);

-- item table

CREATE TABLE item(
    item_id  VARCHAR(255) NOT NULL PRIMARY key ,
    product_name VARCHAR(255) NOT NULL,
    purchase_buyer_id varchar(100) not null,
    FOREIGN KEY(purchase_buyer_id) REFERENCES purchase_person(purchase_buyer_id),
    gst_percentage int(50) not null,
    buying_rate DECIMAL(10,2) not null,
    cost_price  DECIMAL(10,2) not null,
    profit  DECIMAL(10,2),
    normal_sell_price DECIMAL(10,2) not null,
    stock_status Bigint not NULL
);

-- cust_trans table

CREATE TABLE cust_trans(
    trans_id varchar(100) not null primary key,
    cust_id varchar(255),
    FOREIGN key (cust_id) references customer(cust_id),
    debit FLOAT,
    credit FLOAT,
    balance FLOAT not null,
    remark varchar(255) not null,
    date_time DATETIME not NULL,
    user_name varchar(255) not null,
    FOREIGN key (user_name) references user_table(user_name)   
);

-- buy_trans table 

CREATE TABLE buy_trans(
	trans_id varchar(100) primary key,
    buyer_id varchar(255) not null,
	FOREIGN KEY(buyer_id)  REFERENCES purchase_person(purchase_buyer_id),
    debit FLOAT not null,
    credit FLOAT not null,
    balance FLOAT not null,
    date_time DATETIME not NULL
);