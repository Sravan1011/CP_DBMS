Recipe Management System using Flask
Overview
This project is a Recipe Management System built using Flask, a lightweight WSGI web application framework in Python. The system is connected to a MySQL database, providing functionality to explore, add, and view recipes. Users can explore a variety of recipes, add new recipes to the database, and view recipes by specific chefs.

Features
Explore Recipes: Users can browse through a collection of recipes stored in the database.
Add Recipes: Users have the ability to contribute new recipes to the system by submitting them through a form.
View Recipes by Chef: Users can view recipes specifically created by a particular chef, allowing for easy access to a chef's repertoire.
Technical Details
Technologies Used
Flask: Flask is a micro web framework written in Python. It is lightweight and provides tools and libraries to build web applications quickly.
MySQL: MySQL is an open-source relational database management system. It is widely used for storing and managing structured data.
SQLAlchemy: SQLAlchemy is an SQL toolkit and Object-Relational Mapping (ORM) library for Python. It provides a high-level abstraction for interacting with databases.
HTML/CSS: HTML (HyperText Markup Language) is used for creating the structure of web pages, while CSS (Cascading Style Sheets) is used for styling the appearance of these pages.
Jinja2: Jinja2 is a template engine for Python. It allows embedding Python code within HTML templates to generate dynamic content.
Database Schema
The database schema consists of the following tables:

Recipes: Stores information about each recipe, including its title, ingredients, instructions, and the chef who created it.
Chefs: Contains details about each chef, such as their name and a unique identifier.
Flask Routes
The Flask application consists of several routes:

GET /recipes: Displays a list of all available recipes.
GET /recipes/<recipe_id>: Displays details of a specific recipe identified by its ID.
GET /chefs: Lists all chefs present in the database.
GET /chefs/<chef_id>: Displays recipes specific to a particular chef identified by their ID.
POST /add_recipe: Allows users to submit a new recipe to the system.
Installation
To run this application locally, follow these steps:

Clone the repository to your local machine.
Install the required dependencies by running pip install -r requirements.txt.
Set up a MySQL database and update the database configuration in config.py.
Run the Flask application using python app.py.
Access the application through your web browser at http://localhost:5000.
Contributions
Contributions to this project are welcome. If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

License
