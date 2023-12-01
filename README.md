# To-Do List Application

## Author
- Vitthal Humbe

## Overview
This Python application is a simple To-Do List using the Tkinter library for the graphical user interface and SQLite for database storage. Users can log in, add, and delete tasks, and their to-do items persist across sessions.

## Features
- **Login and Signup**: Users can log in with an existing account or create a new one. The login credentials are verified against a MySQL database.
  
- **To-Do List Management**: Users can add tasks to their to-do list and mark them as completed. They can also delete selected tasks.

- **Database Integration**: The application uses SQLite to store user information and to-do items, ensuring data persistence between sessions.

## Usage
1. **Login/Signup**: When the application is launched, users are prompted to either log in or sign up.
   
2. **Add To-Do Items**: After logging in, users can add tasks to their to-do list by typing them into the input field and clicking "Add Todo."
   
3. **Delete To-Do Items**: Users can select tasks using checkboxes and click "Delete Selected" to remove them from the list.

4. **Database Storage**: To-do items are stored in an SQLite database, ensuring that they are retained even if the application is closed and reopened.

## Dependencies
- Python 3
- Tkinter library
- SQLite
- MySQL Connector (for login authentication)

## How to Run
1. Install the required dependencies.
   
2. Run the application by executing the main script:
   ```bash
   python main.py
