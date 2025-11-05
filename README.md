# Client Query Management System

This project is a web-based application built using Python, Streamlit, and MySQL.
It allows clients to submit their queries and the support team to manage them efficiently.

## Features

* Separate login for Clients and Support Team
* Clients can register, log in, and raise new queries
* Support team can view all, open, and closed queries
* Support team can close queries after resolving them
* Passwords are securely stored using hashing
* Simple and user-friendly interface
* Connected with MySQL database

## Technologies Used

* Python
* Streamlit
* MySQL
* SQLAlchemy
* Pandas

## Setup Instructions

1. Clone the repository
2. Install required packages   
  " pip install streamlit sqlalchemy pandas mysql-connector-python "
3. Create a MySQL database named "client_queries_db"
4. Update MySQL username and password inside "db_utils.py"
5. Run the application
  
  " streamlit run app.py"

## Default Support Team Login

Email: support@example.com
Password: Support@123

## Optional

You can import query data from Excel into MySQL using:
"python import_excel_to_mysql.py"


## Author
V. Purvajja
BE( Computer Science and Design )

