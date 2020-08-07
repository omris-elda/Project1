# Project1
Stock counting app

Base requirements:

For this project we were tasked with creating an app with basic CRUD (create, read, update, delete) functionality, using a variety of different methods and tools to ensure that the development, testing, and deployment all went as smoothly as possible.

Some of the tools and systems that we used were:
Python to write the back-end of the application
GCP (for both the Virtual Machine and for the database)
A Jira board
A database containing at least one relationship
Basic HTML to display our app on web pages
Pytest to thorougly test our application
Jenkins to automate the testing and deployment of our app
Flask to help integrate our HTML and Python code seamlessly
A version control system (in this case GitHub), which can also be used to assist in the automated testing and deployment.
Selenium for integration testing


My app
For this project I've decided to create a stock counting system, which contains a variety of different features.
I am able to create new users, suppliers, and products, satisfying the create criteria.
I am able to view the users, suppliers, and products individually, as well as an overview of all the products, satisfying the read criteria.
I am able to edit users, suppliers, and products, satisfying the update criteria.
I am able to delete suppliers and products, satisfying the delete criteria.

For my create functionalities, I'm able to create a variety of different types of database fields.
In my User table, I can create and store:
ID
Username
Email
Password hash

In my Supplier table, I can create and store:
SupplierID
Supplier Name
Supplier Description

In my Stock table, I can create and store:
Product ID
Product Name - the name of the product
Product Price - how much the product costs
Supplier - the supplier that supplies the product
Current Stock - how much of that product is currently in stock

When a user is logged in, they're also allowed to edit several fields, including:
On their account, they can edit their username and email.
For stock, they can edit individual products.
For 
