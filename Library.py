import mysql.connector


# Function to establish a connection to the database
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",  # Your MySQL server host
            user="username",  # Your MySQL user
            password="yourpassword",  # Your MySQL password (empty string is fine if you have no password)
            database="library_db"  # Your database name
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None  # Return None if connection fails

# Function to add a new book to the database
def add_book(title, author, genre, status, card_id=None):
    if not title or not author:
        raise ValueError("Title and Author are required fields.")
    if status not in ["Available", "Issued"]:
        raise ValueError("Status must be 'Available' or 'Issued'.")
    
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, genre, status, card_id) VALUES (%s, %s, %s, %s, %s)",
                       (title, author, genre, status, card_id))
        conn.commit()
        conn.close()
    else:
        print("Failed to connect to the database.")

# Function to get all books from the database
def get_all_books():
    conn = connect_db()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT book_id, title, author, status, card_id FROM books")
        books = cursor.fetchall()
        conn.close()
        return books
    else:
        print("Failed to connect to the database.")
        return []


# Function to search books based on title
def search_books(title=None, author=None, status=None, card_id=None):
    conn = connect_db()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT book_id, title, author, status, card_id FROM books WHERE 1=1"
        params = []
        
        if title:
            query += " AND title LIKE %s"
            params.append(f"%{title}%")
        if author:
            query += " AND author LIKE %s"
            params.append(f"%{author}%")
        if status:
            query += " AND status = %s"
            params.append(status)
        if card_id:
            query += " AND card_id = %s"
            params.append(card_id)
        
        cursor.execute(query, tuple(params))
        books = cursor.fetchall()
        conn.close()
        return books
    else:
        print("Failed to connect to the database.")
        return []

# Function to update book details
def update_book_details(book_id, title, author, genre, status, card_id=None):
    if not title or not author:
        raise ValueError("Title and Author are required fields.")
    if status not in ["Available", "Issued"]:
        raise ValueError("Status must be 'Available' or 'Issued'.")

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""UPDATE books SET title = %s, author = %s, genre = %s, status = %s, card_id = %s 
                          WHERE book_id = %s""", (title, author, genre, status, card_id, book_id))
        conn.commit()
        conn.close()
    else:
        print("Failed to connect to the database.")

# Function to update book status (e.g., Available, Issued)
def update_book_status(book_id, status, card_id=None):
    if status not in ["Available", "Issued"]:
        raise ValueError("Status must be 'Available' or 'Issued'.")

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE books SET status = %s, card_id = %s WHERE book_id = %s", (status, card_id, book_id))
        conn.commit()
        conn.close()
    else:
        print("Failed to connect to the database.")

# Function to delete a book record
def delete_book(book_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
        conn.commit()
        conn.close()
    else:
        print("Failed to connect to the database.")

# Function to delete all books (clear inventory)
def delete_all_books():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books")
        conn.commit()
        conn.close()
    else:
        print("Failed to connect to the database.")
