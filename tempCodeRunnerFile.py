import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Initialize the book records (For demonstration purposes, in real applications, you may use a database)
book_records = []

def add_record():
    # Get values from the input fields
    book_name = book_name_entry.get()
    book_id = book_id_entry.get()
    author_name = author_name_entry.get()
    status = status_combobox.get()

    if not (book_name and book_id and author_name):
        messagebox.showerror("Input Error", "All fields must be filled out.")
        return

    # Add the new book record to the inventory
    new_record = {
        "Book Name": book_name,
        "Book ID": book_id,
        "Author": author_name,
        "Status of the Book": status,
        "Card ID of the Issuer": ""
    }
    book_records.append(new_record)
    update_table()

    # Clear fields after adding
    clear_fields()

def clear_fields():
    book_name_entry.delete(0, tk.END)
    book_id_entry.delete(0, tk.END)
    author_name_entry.delete(0, tk.END)
    status_combobox.set("Available")

def delete_book_record():
    selected_item = book_table.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "No record selected.")
        return
    
    # Get the Book ID from the selected row (column index 1 contains the "Book ID")
    book_id = book_table.item(selected_item)['values'][1]
    
    # Find and delete the record from the book_records list
    global book_records
    book_records = [record for record in book_records if record["Book ID"] != book_id]
    
    # Update the table to reflect the changes
    update_table()


def delete_full_inventory():
    global book_records
    book_records.clear()
    update_table()

def update_book_details():
    selected_item = book_table.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "No record selected.")
        return

    book_id = book_table.item(selected_item)['values'][1]
    updated_book_name = book_name_entry.get()
    updated_author_name = author_name_entry.get()
    updated_status = status_combobox.get()

    for record in book_records:
        if record["Book ID"] == book_id:
            record["Book Name"] = updated_book_name if updated_book_name else record["Book Name"]
            record["Author"] = updated_author_name if updated_author_name else record["Author"]
            record["Status of the Book"] = updated_status if updated_status else record["Status of the Book"]
    
    update_table()
    clear_fields()

def change_issue_availability():
    selected_item = book_table.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "No record selected.")
        return

    book_id = book_table.item(selected_item)['values'][1]
    for record in book_records:
        if record["Book ID"] == book_id:
            # Toggle the status between Available and Issued
            record["Status of the Book"] = "Issued" if record["Status of the Book"] == "Available" else "Available"
    
    update_table()

def update_table():
    # Clear the existing table entries
    for row in book_table.get_children():
        book_table.delete(row)

    # Insert updated records into the table
    for record in book_records:
        book_table.insert("", "end", values=(record["Book Name"], record["Book ID"], record["Author"], record["Status of the Book"], record["Card ID of the Issuer"]))

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
add_button.grid(row=4, column=0, columnspan=2, pady=10)

clear_button = tk.Button(left_frame, text="Clear Fields", command=clear_fields, font=("Arial", 12), bg="lightblue", width=15)
clear_button.grid(row=5, column=0, columnspan=2, pady=5)

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

# Run the application
root.mainloop()
