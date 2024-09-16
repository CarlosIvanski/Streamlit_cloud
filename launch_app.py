import tkinter as tk
from tkinter import messagebox
import streamlit as st
import pandas as pd
import os
import io

# Function to update data
def update_data(index):
    def save_changes():
        table_data[index]['name'] = entry_name.get()
        table_data[index]['email'] = entry_email.get()
        table_data[index]['phone'] = entry_phone.get()
        refresh_table()
        edit_window.destroy()

    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Entry")
    
    tk.Label(edit_window, text="Name:").grid(row=0, column=0)
    entry_name = tk.Entry(edit_window)
    entry_name.insert(0, table_data[index]['name'])
    entry_name.grid(row=0, column=1)
    
    tk.Label(edit_window, text="Email:").grid(row=1, column=0)
    entry_email = tk.Entry(edit_window)
    entry_email.insert(0, table_data[index]['email'])
    entry_email.grid(row=1, column=1)
    
    tk.Label(edit_window, text="Phone:").grid(row=2, column=0)
    entry_phone = tk.Entry(edit_window)
    entry_phone.insert(0, table_data[index]['phone'])
    entry_phone.grid(row=2, column=1)
    
    tk.Button(edit_window, text="Save", command=save_changes).grid(row=3, column=0, columnspan=2)

# Function to delete data
def delete_data(index):
    if messagebox.askyesno("Delete", "Are you sure you want to delete this entry?"):
        del table_data[index]
        refresh_table()

# Function to refresh table display
def refresh_table():
    for widget in table_frame.winfo_children():
        widget.destroy()
    
    # Create header row
    headers = ['ID', 'Name', 'Email', 'Phone', 'Actions']
    for col, header in enumerate(headers):
        label = tk.Label(table_frame, text=header, borderwidth=1, relief="solid", width=15)
        label.grid(row=0, column=col)

    # Create data rows
    for i, entry in enumerate(table_data):
        tk.Label(table_frame, text=entry['id'], borderwidth=1, relief="solid", width=15).grid(row=i+1, column=0)
        tk.Label(table_frame, text=entry['name'], borderwidth=1, relief="solid", width=15).grid(row=i+1, column=1)
        tk.Label(table_frame, text=entry['email'], borderwidth=1, relief="solid", width=15).grid(row=i+1, column=2)
        tk.Label(table_frame, text=entry['phone'], borderwidth=1, relief="solid", width=15).grid(row=i+1, column=3)
        
        tk.Button(table_frame, text="Edit", command=lambda i=i: update_data(i)).grid(row=i+1, column=4)
        tk.Button(table_frame, text="Delete", command=lambda i=i: delete_data(i)).grid(row=i+1, column=5)

# Initial data
table_data = [
    {'id': 1, 'name': 'John Doe', 'email': 'john@example.com', 'phone': '123-456-7890'},
    {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com', 'phone': '098-765-4321'}
]

# Main window
root = tk.Tk()
root.title("Table with Edit/Delete")

# Frame to hold the table
table_frame = tk.Frame(root)
table_frame.pack(padx=10, pady=10)

# Refresh table to display the initial data
refresh_table()

# Start the GUI loop
root.mainloop()
