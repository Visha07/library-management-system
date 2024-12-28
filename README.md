# Library Management System

This is a simple Library Management System built using Python, MySQL, and `mysql.connector` library. It allows for the management of books in a library database. The system supports adding, searching, updating, and deleting books. It also handles the status of the books (e.g., Available, Issued).

## Features

- **Add a Book**: Add new books to the library with details like title, author, genre, and status.
- **Search Books**: Search books by title, author, status, and card ID.
- **Update Book Details**: Update the details of existing books.
- **Update Book Status**: Change the status of a book (e.g., from "Available" to "Issued").
- **Delete a Book**: Remove a book from the library database.
- **Delete All Books**: Clear the entire inventory of books.

## Requirements

- **Python** (>= 3.6)
- **MySQL Database**: A MySQL database with a table `books` to store the books' information.
- **mysql.connector**: A Python package to interact with the MySQL database.

### Python Libraries

You can install the required libraries using `pip`:

```bash
pip install mysql-connector-python
