import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector

# Function to establish MySQL connection
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="user",  # Change as per your setup
            password="yourpassword",
            database="library_db"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error connecting to database: {err}")
        return None

# Initialize MySQL Database
def init_db():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                                book_name VARCHAR(255),
                                book_id VARCHAR(255) PRIMARY KEY,
                                author VARCHAR(255),
                                status VARCHAR(255),
                                card_id VARCHAR(255))''')
            conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error initializing database: {err}")
        finally:
            conn.close()

# Function to add record to the database
def add_record():
    book_name = book_name_entry.get()
    book_id = book_id_entry.get()
    author_name = author_name_entry.get()
    status = status_combobox.get()

    if not (book_name and book_id and author_name):
        messagebox.showerror("Input Error", "All fields must be filled out.")
        return

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO books (book_name, book_id, author, status, card_id)
                              VALUES (%s, %s, %s, %s, %s)''', 
                              (book_name, book_id, author_name, status, ""))
            conn.commit()
            update_table()
            clear_fields()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error inserting record: {err}")
        finally:
            conn.close()

# Function to update the book table
def update_table():
    for row in book_table.get_children():
        book_table.delete(row)

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM books')
            records = cursor.fetchall()
            for record in records:
                book_table.insert("", "end", values=record)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching records: {err}")
        finally:
            conn.close()

# Function to delete a book record
def delete_book_record():
    selected_item = book_table.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "No record selected.")
        return

    book_id = book_table.item(selected_item)['values'][1]
    if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the book with ID {book_id}?"):
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM books WHERE book_id = %s', (book_id,))
                conn.commit()
                update_table()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error deleting record: {err}")
            finally:
                conn.close()

# Function to delete all book records
def delete_full_inventory():
    if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete all book records?"):
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM books')
                conn.commit()
                update_table()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error deleting all records: {err}")
            finally:
                conn.close()

# Function to clear input fields
def clear_fields():
    book_name_entry.delete(0, tk.END)
    book_id_entry.delete(0, tk.END)
    author_name_entry.delete(0, tk.END)
    status_combobox.set("Available")

# Initialize main window
root = tk.Tk()
root.title("Library Management System")
root.geometry("900x600")
root.configure(bg="skyblue")

# Title Label
title_label = tk.Label(root, text="LIBRARY MANAGEMENT SYSTEM", font=("Arial", 18, "bold"), bg="skyblue")
title_label.pack(pady=10)

# Left Panel for Book Entry
left_frame = tk.Frame(root, bg="skyblue")
left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)

# Book Name Entry
tk.Label(left_frame, text="Book Name", bg="skyblue", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
book_name_entry = tk.Entry(left_frame, font=("Arial", 12))
book_name_entry.grid(row=0, column=1, pady=5, padx=10)

# Book ID Entry
tk.Label(left_frame, text="Book ID", bg="skyblue", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
book_id_entry = tk.Entry(left_frame, font=("Arial", 12))
book_id_entry.grid(row=1, column=1, pady=5, padx=10)

# Author Name Entry
tk.Label(left_frame, text="Author Name", bg="skyblue", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
author_name_entry = tk.Entry(left_frame, font=("Arial", 12))
author_name_entry.grid(row=2, column=1, pady=5, padx=10)

# Status of the Book Combobox
tk.Label(left_frame, text="Status of the Book", bg="skyblue", font=("Arial", 12)).grid(row=3, column=0, sticky="w", pady=5)
status_combobox = ttk.Combobox(left_frame, values=["Available", "Issued"], font=("Arial", 12))
status_combobox.grid(row=3, column=1, pady=5, padx=10)
status_combobox.current(0)

# Buttons for Adding and Clearing Records
add_button = tk.Button(left_frame, text="Add New Record", command=add_record, font=("Arial", 12), bg="lightblue", width=15)
add_button.grid(row=5, column=0, columnspan=2, pady=10)

clear_button = tk.Button(left_frame, text="Clear Fields", command=clear_fields, font=("Arial", 12), bg="lightblue", width=15)
clear_button.grid(row=6, column=0, columnspan=2, pady=5)

# Book Inventory Table
right_frame = tk.Frame(root, bg="skyblue")
right_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)

table_title = tk.Label(right_frame, text="BOOK INVENTORY", font=("Arial", 14, "bold"), bg="skyblue")
table_title.pack()

columns = ("Book Name", "Book ID", "Author", "Status of the Book", "Card ID of the Issuer")
book_table = ttk.Treeview(right_frame, columns=columns, show="headings", height=15)
for col in columns:
    book_table.heading(col, text=col)
    book_table.column(col, width=150, anchor="center")

book_table.pack(pady=10, fill=tk.BOTH, expand=True)

# Initialize the database and update the table
init_db()
update_table()

# Run the application
root.mainloop()
