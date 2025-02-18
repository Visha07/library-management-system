import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import mysql.connector
def conn(){
    mysql.connector.connect(
            host="localhost",  # Your MySQL host (use 'localhost' if running locally)
            user="user",       # Your MySQL username
            password="yourpassword",       # Your MySQL password
            database="library_db"  # Name of your MySQL database
        )
}
# Initialize MySQL Database
def init_db():
    try:
        conn
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                            book_name VARCHAR(255),
                            book_id VARCHAR(255) PRIMARY KEY,
                            author VARCHAR(255),
                            status VARCHAR(255),
                            card_id VARCHAR(255))''')
        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error initializing database: {err}")

# Function to add record to the database
def add_record():
    book_name = book_name_entry.get()
    book_id = book_id_entry.get()
    author_name = author_name_entry.get()
    status = status_combobox.get()
   

    if not (book_name and book_id and author_name):
        messagebox.showerror("Input Error", "All fields must be filled out.")
        return

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="user",
            password="password",
            database="library_db"
        )
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO books (book_name, book_id, author, status, card_id)
                          VALUES (%s, %s, %s, %s, %s)''', (book_name, book_id, author_name, status, ""))
        conn.commit()
        conn.close()
        update_table()
        clear_fields()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error inserting record: {err}")

# Function to update the table from the database
# Function to update the book table
# Function to update the book table
def update_table():
    for row in book_table.get_children():
        book_table.delete(row)

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="visha",
            password="Arpan@1234",
            database="library_db"
        )
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books')
        records = cursor.fetchall()
        for record in records:
            book_table.insert("", "end", values=record)  # Display book details including Card ID
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching records: {err}")

# Function to delete a book record
def delete_book_record():
    selected_item = book_table.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "No record selected.")
        return

    book_id = book_table.item(selected_item)['values'][1]
    if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the book with ID {book_id}?"):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="visha",
                password="Arpan@1234",
                database="library_db"
            )
            cursor = conn.cursor()
            cursor.execute('DELETE FROM books WHERE book_id = %s', (book_id,))
            conn.commit()
            conn.close()
            update_table()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error deleting record: {err}")

# Function to delete all book records
def delete_full_inventory():
    if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete all book records?"):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="visha",
                password="Arpan@1234",
                database="library_db"
            )
            cursor = conn.cursor()
            cursor.execute('DELETE FROM books')
            conn.commit()
            conn.close()
            update_table()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error deleting all records: {err}")

# Function to update book details
def update_book_details():
    selected_item = book_table.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "No record selected.")
        return

    # Get the Book ID from the selected row (column index 1 contains the "Book ID")
    book_id = book_table.item(selected_item)['values'][1]

    # Get updated values from the input fields
    updated_book_name = book_name_entry.get()
    updated_author_name = author_name_entry.get()
    updated_status = status_combobox.get()
    

    # Make sure at least one field is updated
    if not (updated_book_name or updated_author_name or updated_status):
        messagebox.showerror("Input Error", "At least one field must be updated.")
        return

    # Create a connection to the MySQL database
    conn = mysql.connector.connect(
        host='localhost',
        user='visha',
        password='Arpan@1234',  # Replace with your MySQL password
        database='library_db'
    )
    cursor = conn.cursor()

    try:
        # Create the update query with dynamic values
        query = "UPDATE books SET "
        updates = []

        # Only add fields to the query if they were changed
        if updated_book_name:
            updates.append(f"book_name = '{updated_book_name}'")
        if updated_author_name:
            updates.append(f"author = '{updated_author_name}'")
        if updated_status:
            updates.append(f"status = '{updated_status}'")

        # Join the updates into the final query
        query += ", ".join(updates) + f" WHERE book_id = '{book_id}'"

        # Execute the update query
        cursor.execute(query)

        # Commit the changes to the database
        conn.commit()

        # Check if any rows were updated
        if cursor.rowcount > 0:
            messagebox.showinfo("Success", "Book details updated successfully.")
        else:
            messagebox.showerror("Error", "Book not found or no changes made.")
        
        # Update the table and clear the fields
        update_table()
        clear_fields()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Function to toggle book status between Available and Issued
# Function to change book status and assign Card ID of the issuer
def change_issue_availability():
    selected_item = book_table.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "No record selected.")
        return

    book_id = book_table.item(selected_item)['values'][1]
    current_status = book_table.item(selected_item)['values'][3]

    if current_status == "Available":
        # If the book is available, change to Issued
        card_id = simpledialog.askstring("Card ID", "Enter the Card ID of the borrower:")
        if card_id:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="visha",
                    password="Arpan@1234",
                    database="library_db"
                )
                cursor = conn.cursor()
                cursor.execute('UPDATE books SET status = %s, card_id = %s WHERE book_id = %s',
                               ("Issued", card_id, book_id))
                conn.commit()
                conn.close()
                update_table()
                messagebox.showinfo("Success", "Book status updated to Issued and Card ID assigned.")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error updating book: {err}")
    else:
        # If the book is issued, change to Available
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="visha",
                password="Arpan@1234",
                database="library_db"
            )
            cursor = conn.cursor()
            cursor.execute('UPDATE books SET status = %s, card_id = %s WHERE book_id = %s',
                           ("Available", "", book_id))  # Clear the card ID when returning the book
            conn.commit()
            conn.close()
            update_table()
            messagebox.showinfo("Success", "Book status updated to Available and Card ID cleared.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error updating book: {err}")

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

# Right Panel for Book Inventory Table and Control Buttons
right_frame = tk.Frame(root, bg="skyblue")
right_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)

# Table Title
table_title = tk.Label(right_frame, text="BOOK INVENTORY", font=("Arial", 14, "bold"), bg="skyblue")
table_title.pack()

# Book Inventory Table
columns = ("Book Name", "Book ID", "Author", "Status of the Book", "Card ID of the Issuer")
book_table = ttk.Treeview(right_frame, columns=columns, show="headings", height=15)
for col in columns:
    book_table.heading(col, text=col)
    book_table.column(col, width=150, anchor="center")

book_table.pack(pady=10, fill=tk.BOTH, expand=True)

# Control Buttons
button_frame = tk.Frame(right_frame, bg="skyblue")
button_frame.pack(pady=10)

delete_button = tk.Button(button_frame, text="Delete Book Record", command=delete_book_record, font=("Arial", 10), bg="lightcoral", width=20)
delete_button.grid(row=0, column=0, padx=5)

delete_all_button = tk.Button(button_frame, text="Delete Full Inventory", command=delete_full_inventory, font=("Arial", 10), bg="lightcoral", width=20)
delete_all_button.grid(row=0, column=1, padx=5)

update_button = tk.Button(button_frame, text="Update Book Details", command=update_book_details, font=("Arial", 10), bg="lightgreen", width=20)
update_button.grid(row=0, column=2, padx=5)

change_status_button = tk.Button(button_frame, text="Change Issue Availability", command=change_issue_availability, font=("Arial", 10), bg="lightblue", width=20)
change_status_button.grid(row=0, column=3, padx=5)

# Initialize the database and update the table
init_db()
update_table()

# Run the application
root.mainloop()
