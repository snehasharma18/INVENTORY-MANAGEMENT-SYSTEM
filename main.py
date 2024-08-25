import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import customtkinter as ctk
import customtkinter
import pickle
import logging
import os
import warnings
warnings.filterwarnings("ignore")

# Initialize appearance mode and theme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

class InventoryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.conn = sqlite3.connect('inventory.db')
        self.root.geometry("1900x1000")
        self.mode = "dark"
        self.create_tables()
        self.login_screen()

        # Initialize customtkinter
        self.logged_in_user = None  # To store logged-in user details
        
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        item_name TEXT NOT NULL,
                        min_quantity INTEGER NOT NULL,
                        max_quantity INTEGER NOT NULL,
                        consumed_quantity INTEGER NOT NULL,
                        supplier_emails TEXT NOT NULL)''')
        self.conn.commit()

    def login_screen(self):
        self.clear_screen()
        font_style = ("Helvetica", 50, "bold")
        customtkinter.CTkLabel(self.root, text='INVENTORY MANAGEMENT SYSTEM',font=font_style).grid(row=0, column=5, padx=150, pady=20, sticky='nsew')

        self.login_frame = customtkinter.CTkFrame(master = self.root, width = 1200, height = 1200, border_width = 5, corner_radius = 10)
        self.login_frame.grid(row=1, column=2, columnspan=6,rowspan=4, padx=10, pady=10, sticky='nsew')

        font_style1 = ("Arial",20,"bold")
        customtkinter.CTkLabel(self.login_frame, text="LOGIN",font=font_style1).grid(row=0,column=2,columnspan=2,padx=10,pady=10,sticky="nsew")
        
        customtkinter.CTkLabel(self.login_frame, text="User ID (Email) :").grid(row=3, column=2, padx=10, pady=10, sticky="nsew")
        self.userid_entry = customtkinter.CTkEntry(self.login_frame,width=200)
        self.userid_entry.grid(row=3, column=3, padx=10, pady=10,sticky="nsew")
        
        customtkinter.CTkLabel(self.login_frame, text="Password :").grid(row=4, column=2, padx=10, pady=10, sticky="nsew")
        self.password_entry = customtkinter.CTkEntry(self.login_frame, show="*",width=200)
        self.password_entry.grid(row=4, column=3, padx=10, pady=10,sticky="nsew")
        
        self.remember_var = tk.BooleanVar()
        self.remember_checkbox = customtkinter.CTkCheckBox(self.login_frame, text="Remember Me", variable=self.remember_var)
        self.remember_checkbox.grid(row=5, column=3, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        customtkinter.CTkButton(self.login_frame, text="Login", command=self.login).grid(row=6, column=3, columnspan=2, padx=10, pady=10,sticky="nsew")
        
        theme_button = customtkinter.CTkButton(self.root, text="Change Theme", command=self.change_theme)
        theme_button.grid(row=0, column=7, padx=20, pady=20, sticky='ne')

        self.sign_up_frame = customtkinter.CTkFrame(master = self.root, width = 1200, height = 1200, border_width = 5, corner_radius = 10)
        self.sign_up_frame.grid(row=6,column=5,rowspan=4,columnspan=6,padx=10,pady=10,sticky='nsew')
        
        ctk.CTkLabel(self.sign_up_frame, text='SIGN UP', font=font_style1).grid(row=0, column=0, columnspan=2, padx=10, pady=20)

        ctk.CTkLabel(self.sign_up_frame, text="Name :").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.name_entry = ctk.CTkEntry(self.sign_up_frame,width=200)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(self.sign_up_frame, text="Email :").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.email_entry = ctk.CTkEntry(self.sign_up_frame,width=200)
        self.email_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(self.sign_up_frame, text="Password :").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.sign_up_password_entry = ctk.CTkEntry(self.sign_up_frame, show="*",width=200)
        self.sign_up_password_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(self.sign_up_frame, text="Role :").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.role_combobox = customtkinter.CTkComboBox(self.sign_up_frame, values=["User", "Admin"],width=200)
        self.role_combobox.grid(row=4, column=1, padx=10, pady=10)
        selected_role = self.role_combobox.get()
        
        customtkinter.CTkButton(self.sign_up_frame, text="Sign Up", command=self.sign_up).grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.load_login_details()

    def sign_up(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        role = self.role_combobox.get()

        if not name or not email or not password or not role:
            messagebox.showerror("Sign-Up Failed", "All fields are required")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address")
            return

        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)", (name, email, password, role))
            self.conn.commit()
            messagebox.showinfo("Sign-Up Successful", "Sign-up successful!")
        except sqlite3.Error as err:
            messagebox.showerror("Error", f"Error during sign-up: {err}")
        finally:
            cursor.close()

    def login(self):
        email = self.userid_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Login Failed", "Please enter both email and password")
            return

        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, role FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()

        if user:
            self.logged_in_user = user
            role_message = f"Login successful! You are logged in as {user[2]}."
            messagebox.showinfo("Login Successful", role_message)

            if self.remember_var.get():
                self.save_login_details()
            else:
                self.delete_login_details()

            if user[2] == "Admin":
                self.admin_screen()
            elif user[2] == "User":
                self.user_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    def admin_screen(self):
        #tk.Button(self.root, text="Add New Member", command=self.add_new_member).grid(row=1, column=0, padx=10, pady=10)
        #tk.Button(self.root, text="Delete Member", command=self.delete_member).grid(row=1, column=3, padx=10, pady=10)
        self.clear_screen()

    # Set up the main title label
        font_style = ("Helvetica", 50, "bold")
        customtkinter.CTkLabel(self.root, text='INVENTORY MANAGEMENT SYSTEM', font=font_style).grid(row=0, column=0, columnspan=10, padx=150, pady=20, sticky='nsew')
    
    # Add the theme button
        theme_button = customtkinter.CTkButton(self.root, text="Change Theme", command=self.change_theme)
        theme_button.grid(row=0, column=10, padx=20, pady=20, sticky='ne')

        logout_button = customtkinter.CTkButton(self.root, text="Log Out", command=self.logout)
        logout_button.grid(row=9, column=10, padx=20, pady=20, sticky='se')

    # Define a common size for all frames
        frame_width = 400
        frame_height = 400

    # Add Item Frame
        font_style1 = ("Arial", 20, "bold")
        add_item_frame = customtkinter.CTkFrame(self.root, width=frame_width, height=frame_height, border_width=5, corner_radius=10)
        add_item_frame.grid(row=1, column=0, rowspan=6, columnspan=4, padx=10, pady=10, sticky='nsew')

        customtkinter.CTkLabel(add_item_frame, text="Add Inventory Item", font=font_style1).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        customtkinter.CTkLabel(add_item_frame, text="Item Name:").grid(row=1, column=0, padx=10, pady=10)
        self.item_name_entry = customtkinter.CTkEntry(add_item_frame, width=200)
        self.item_name_entry.grid(row=1, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(add_item_frame, text="Minimum Quantity:").grid(row=2, column=0, padx=10, pady=10)
        self.min_quantity_entry = customtkinter.CTkEntry(add_item_frame, width=200)
        self.min_quantity_entry.grid(row=2, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(add_item_frame, text="Maximum Quantity:").grid(row=3, column=0, padx=10, pady=10)
        self.max_quantity_entry = customtkinter.CTkEntry(add_item_frame, width=200)
        self.max_quantity_entry.grid(row=3, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(add_item_frame, text="Consumed Quantity:").grid(row=4, column=0, padx=10, pady=10)
        self.consumed_quantity_entry = customtkinter.CTkEntry(add_item_frame, width=200)
        self.consumed_quantity_entry.grid(row=4, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(add_item_frame, text="Supplier Emails:").grid(row=5, column=0, padx=10, pady=10)
        self.supplier_emails_entry = customtkinter.CTkEntry(add_item_frame, width=200)
        self.supplier_emails_entry.grid(row=5, column=1, padx=10, pady=10)

        customtkinter.CTkButton(add_item_frame, text="Submit", command=self.submit_inventory_item, fg_color="green").grid(row=6, column=0, columnspan=2, pady=10)
        customtkinter.CTkButton(add_item_frame, text="Cancel", command=self.cancel_submit, fg_color="maroon").grid(row=7, column=0, columnspan=2, pady=10)

    # Update Item Frame
        update_item_frame = customtkinter.CTkFrame(self.root, width=frame_width, height=frame_height, border_width=5, corner_radius=10)
        update_item_frame.grid(row=1, column=4, rowspan=6, columnspan=4, padx=10, pady=10, sticky='nsew')

        customtkinter.CTkLabel(update_item_frame, text="Update Inventory", font=font_style1).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        customtkinter.CTkLabel(update_item_frame, text="Select Item:").grid(row=1, column=0, padx=10, pady=10)
        self.item_combobox = customtkinter.CTkComboBox(update_item_frame, values=self.get_inventory_items())
        self.item_combobox.grid(row=1, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(update_item_frame, text="Quantity Consumed:").grid(row=2, column=0, padx=10, pady=10)
        self.new_quantity_entry = customtkinter.CTkEntry(update_item_frame)
        self.new_quantity_entry.grid(row=2, column=1, padx=10, pady=10)

        customtkinter.CTkButton(update_item_frame, text="Update", command=self.update, fg_color="green").grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        customtkinter.CTkLabel(add_item_frame, text="Minimum Quantity:").grid(row=2, column=0, padx=10, pady=10)
        self.min_quantity_entry = customtkinter.CTkEntry(add_item_frame, width=200)
        self.min_quantity_entry.grid(row=2, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(add_item_frame, text="Maximum Quantity:").grid(row=3, column=0, padx=10, pady=10)
        self.max_quantity_entry = customtkinter.CTkEntry(add_item_frame, width=200)
        self.max_quantity_entry.grid(row=3, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(add_item_frame, text="Consumed Quantity:").grid(row=4, column=0, padx=10, pady=10)
        self.consumed_quantity_entry = customtkinter.CTkEntry(add_item_frame, width=200)
        self.consumed_quantity_entry.grid(row=4, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(add_item_frame, text="Supplier Emails:").grid(row=5, column=0, padx=10, pady=10)
        self.supplier_emails_entry = customtkinter.CTkEntry(add_item_frame, width=200)
        self.supplier_emails_entry.grid(row=5, column=1, padx=10, pady=10)

        customtkinter.CTkButton(add_item_frame, text="Submit", command=self.submit_inventory_item, fg_color="green").grid(row=6, column=0, columnspan=2, pady=10)
        customtkinter.CTkButton(add_item_frame, text="Cancel", command=self.cancel_submit, fg_color="maroon").grid(row=7, column=0, columnspan=2, pady=10)

    # Update Item Frame
        update_item_frame = customtkinter.CTkFrame(self.root, width=frame_width, height=frame_height, border_width=5, corner_radius=10)
        update_item_frame.grid(row=1, column=4, rowspan=6, columnspan=4, padx=10, pady=10, sticky='nsew')

        customtkinter.CTkLabel(update_item_frame, text="Update Inventory", font=font_style1).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        customtkinter.CTkLabel(update_item_frame, text="Select Item:").grid(row=1, column=0, padx=10, pady=10)
        self.item_combobox = customtkinter.CTkComboBox(update_item_frame, values=self.get_inventory_items())
        self.item_combobox.grid(row=1, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(update_item_frame, text="Quantity Consumed:").grid(row=2, column=0, padx=10, pady=10)
        self.new_quantity_entry = customtkinter.CTkEntry(update_item_frame)
        self.new_quantity_entry.grid(row=2, column=1, padx=10, pady=10)

        customtkinter.CTkButton(update_item_frame, text="Update", command=self.update, fg_color="green").grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        customtkinter.CTkButton(update_item_frame, text="Cancel", command=self.cancel_update, fg_color="maroon").grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # Delete Item Frame
        delete_item_frame = customtkinter.CTkFrame(self.root, width=frame_width, height=frame_height, border_width=5, corner_radius=10)
        delete_item_frame.grid(row=1, column=8, rowspan=6, columnspan=4, padx=10, pady=10, sticky='nsew')

        customtkinter.CTkLabel(delete_item_frame, text="Delete Inventory Item", font=font_style1).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        customtkinter.CTkLabel(delete_item_frame, text="Select Item:").grid(row=1, column=0, padx=10, pady=10)

        self.inventory_var = tk.StringVar()
        items = self.get_inventory_items()
        self.inventory_combobox = customtkinter.CTkComboBox(delete_item_frame, values=items, variable=self.inventory_var)
        self.inventory_combobox.grid(row=1, column=1, padx=10, pady=10)

        customtkinter.CTkButton(delete_item_frame, text="Delete", command=self.confirm_delete_inventory_item, fg_color="green").grid(row=2, column=0, columnspan=2, pady=10)
        customtkinter.CTkButton(delete_item_frame, text="Cancel", command=self.cancel_delete, fg_color="maroon").grid(row=3, column=0, columnspan=2, pady=10)

    # Table Frame (at the bottom)
        self.table_frame = customtkinter.CTkFrame(self.root, border_width=5, corner_radius=10)
        self.table_frame.grid(row=7, column=0, columnspan=12, padx=10, pady=10, sticky='nsew')
        
    # Table title
        customtkinter.CTkLabel(self.table_frame, text="List of Items", font=font_style1).grid(row=0, column=0, columnspan=5, padx=10, pady=10)

            # Column headers
        headers = ["Item Name", "Min Quantity", "Max Quantity", "Consumed Quantity", "Supplier Emails"]
        for col, header in enumerate(headers):
            customtkinter.CTkLabel(self.table_frame, text=header, font=("Helvetica", 14, "bold")).grid(row=1, column=col, padx=10, pady=5)

    # Populate the table with data
        #for row, item in enumerate(inventory_data, start=2):
            #for col, value in enumerate(item):
                #customtkinter.CTkLabel(table_frame, text=value).grid(row=row, column=col, padx=10, pady=5)

    # Configure the grid to ensure the frames resize properly
        self.root.grid_rowconfigure(7, weight=1)
        self.root.grid_columnconfigure((0, 4, 8), weight=1)
        self.refresh_inventory_list()
 
    def user_screen(self):
        self.clear_screen()

    # Set up the main title label
        font_style = ("Helvetica", 50, "bold")
        customtkinter.CTkLabel(self.root, text='INVENTORY MANAGEMENT SYSTEM', font=font_style).grid(row=0, column=0, columnspan=10, padx=150, pady=20, sticky='nsew')
    
    # Add the theme button
        theme_button = customtkinter.CTkButton(self.root, text="Change Theme", command=self.change_theme)
        theme_button.grid(row=0, column=10, padx=20, pady=20, sticky='ne')

        logout_button = customtkinter.CTkButton(self.root, text="Log Out", command=self.logout)
        logout_button.grid(row=9, column=10, padx=20, pady=20, sticky='se')

    # Define a common size for all frames
        frame_width = 400
        frame_height = 400

    # Add Item Frame
        font_style1 = ("Arial", 20, "bold")
        add_item_frame = customtkinter.CTkFrame(self.root, width=frame_width, height=frame_height, border_width=5, corner_radius=10)
        add_item_frame.grid(row=1, column=0, rowspan=6, columnspan=4, padx=10, pady=10, sticky='nsew')

        customtkinter.CTkLabel(add_item_frame, text="Add Inventory Item", font=font_style1).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        customtkinter.CTkLabel(add_item_frame, text="Item Name:").grid(row=1, column=0, padx=10, pady=10)
        self.item_name_entry = customtkinter.CTkEntry(add_item_frame, width=200)
        self.item_name_entry.grid(row=1, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(add_item_frame, text="Minimum Quantity:").grid(row=2, column=0, padx=10, pady=10)
        self.min_quantity_entry = customtkinter.CTkEntry(add_item_frame, width=200)
        self.min_quantity_entry.grid(row=2, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(add_item_frame, text="Maximum Quantity:").grid(row=3, column=0, padx=10, pady=10)
        self.max_quantity_entry = customtkinter.CTkEntry(add_item_frame, width=200)
        self.max_quantity_entry.grid(row=3, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(add_item_frame, text="Consumed Quantity:").grid(row=4, column=0, padx=10, pady=10)
        self.consumed_quantity_entry = customtkinter.CTkEntry(add_item_frame, width=200)
        self.consumed_quantity_entry.grid(row=4, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(add_item_frame, text="Supplier Emails:").grid(row=5, column=0, padx=10, pady=10)
        self.supplier_emails_entry = customtkinter.CTkEntry(add_item_frame, width=200)
        self.supplier_emails_entry.grid(row=5, column=1, padx=10, pady=10)

        customtkinter.CTkButton(add_item_frame, text="Submit", command=self.submit_inventory_item, fg_color="green").grid(row=6, column=1,columnspan=1, pady=10)
        customtkinter.CTkButton(add_item_frame, text="Cancel", command=self.cancel_submit, fg_color="maroon").grid(row=6, column=2, columnspan=2, pady=10)

    # Update Item Frame
        update_item_frame = customtkinter.CTkFrame(self.root, border_width=5, corner_radius=10)
        update_item_frame.grid(row=1, column=4, rowspan=6, columnspan=4, padx=10, pady=10, sticky='nsew')
        
        # Configure row and column to allow frame expansion
        self.root.grid_rowconfigure(1, weight=1)  # Ensure the row expands
        self.root.grid_columnconfigure(4, weight=1)  # Ensure the column expands

        customtkinter.CTkLabel(update_item_frame, text="Update Inventory", font=font_style1).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        customtkinter.CTkLabel(update_item_frame, text="Select Item:").grid(row=1, column=0, padx=10, pady=10)
        self.item_combobox = customtkinter.CTkComboBox(update_item_frame, values=self.get_inventory_items())
        self.item_combobox.grid(row=1, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(update_item_frame, text="Quantity Consumed:").grid(row=2, column=0, padx=10, pady=10)
        self.new_quantity_entry = customtkinter.CTkEntry(update_item_frame)
        self.new_quantity_entry.grid(row=2, column=1, padx=10, pady=10)

        customtkinter.CTkButton(update_item_frame, text="Update", command=self.update, fg_color="green").grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        customtkinter.CTkButton(update_item_frame, text="Cancel", command=self.cancel_update, fg_color="maroon").grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # Delete Item Frame
        delete_item_frame = customtkinter.CTkFrame(self.root, width=frame_width, height=frame_height, border_width=5, corner_radius=10)
        delete_item_frame.grid(row=1, column=8, rowspan=6, columnspan=4, padx=10, pady=10, sticky='nsew')

        # Configure row and column to allow frame expansion
        self.root.grid_rowconfigure(1, weight=1)  # Ensure the row expands
        self.root.grid_columnconfigure(8, weight=1)  # Ensure the column expands

        customtkinter.CTkLabel(delete_item_frame, text="Delete Inventory Item", font=font_style1).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        customtkinter.CTkLabel(delete_item_frame, text="Select Item:").grid(row=1, column=0, padx=10, pady=10)

        self.inventory_var = tk.StringVar()
        items = self.get_inventory_items()
        self.inventory_combobox = customtkinter.CTkComboBox(delete_item_frame, values=items, variable=self.inventory_var)
        self.inventory_combobox.grid(row=1, column=1, padx=10, pady=10)

        customtkinter.CTkButton(delete_item_frame, text="Delete", command=self.confirm_delete_inventory_item, fg_color="green").grid(row=2, column=0, columnspan=2, pady=10)
        customtkinter.CTkButton(delete_item_frame, text="Cancel", command=self.cancel_delete, fg_color="maroon").grid(row=3, column=0, columnspan=2, pady=10)

    # Table Frame (at the bottom)
        self.table_frame = customtkinter.CTkFrame(self.root, border_width=5, corner_radius=10)
        self.table_frame.grid(row=7, column=0, columnspan=12, padx=10, pady=10, sticky='nsew')

        # Configuring the rows and columns for the grid
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)  # For canvas
        self.table_frame.grid_columnconfigure(11, weight=0) # For scrollbar

        # Creating a canvas to hold the table
        self.canvas = ctk.CTkCanvas(self.table_frame, highlightthickness=2)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Scrollbar
        self.scrollbar = ctk.CTkScrollbar(self.table_frame, orientation="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=11, sticky="ns")

        # Configuring the canvas to work with scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.table_content = ctk.CTkFrame(self.canvas)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Table content

        self.canvas.create_window((0, 0), window=self.table_content, anchor="nw")
        
    # Table title
        customtkinter.CTkLabel(self.table_frame, text="List of Items", font=font_style1).grid(row=0, column=0, columnspan=5, padx=10, pady=10)

    # Column headers
        headers = ["Item Name", "Min Quantity", "Max Quantity", "Consumed Quantity", "Supplier Emails"]
        for col, header in enumerate(headers):
            customtkinter.CTkLabel(self.table_content, text=header, font=("Helvetica", 14, "bold")).grid(row=1, column=col, padx=10, pady=5)

    # Populate the table with data
        #for row, item in enumerate(inventory_data, start=2):
            #for col, value in enumerate(item):
                #customtkinter.CTkLabel(table_frame, text=value).grid(row=row, column=col, padx=10, pady=5)

    # Configure the grid to ensure the frames resize properly
        self.root.grid_rowconfigure(7, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.refresh_inventory_list()
                
    def delete_member(self):
        member_id = simpledialog.askinteger("Delete Member", "Enter Member ID:")
        if member_id is not None:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM users WHERE id = ?", (member_id,))
            result = cursor.fetchone()
        
            if result:
                member_name = result[0]
                confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the member with ID {member_id} and Name {member_name}?")
                if confirm:
                    cursor.execute("DELETE FROM users WHERE id = ?", (member_id,))
                    self.conn.commit()
                    if cursor.rowcount > 0:
                        messagebox.showinfo("Success", "Member deleted successfully")
                    else:
                        messagebox.showerror("Error", "Member ID not found")
                else:
                    messagebox.showinfo("Cancelled", "Member deletion cancelled")
            else:
                messagebox.showerror("Error", "Member ID not found")
              
    def submit_new_member(self):
        name = self.name_entry.get().lower()
        email = self.email_entry.get().lower()
        password = self.password_entry.get()
        role = self.role_var.get().lower()

        if not name or not email or not password or not role:
            messagebox.showerror("Input Error", "All fields are required")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address")
            return

        cursor = self.conn.cursor()

        # Check for duplicate email
        cursor.execute("SELECT COUNT(*) FROM users WHERE email = ?", (email,))
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Duplicate Entry", "A member with this email already exists")
            return

        cursor.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                       (name, email, password, role))
        self.conn.commit()
        messagebox.showinfo("Success", "New member added successfully")

    def submit_inventory_item(self):
        item_name = self.item_name_entry.get()
        min_quantity = int(self.min_quantity_entry.get())
        max_quantity = int(self.max_quantity_entry.get())
        consumed_quantity = int(self.consumed_quantity_entry.get())
        supplier_emails = self.supplier_emails_entry.get()

        if not item_name or min_quantity < 0 or max_quantity < 0 or consumed_quantity < 0 or not supplier_emails:
            messagebox.showerror("Error", "All fields are required and quantities must be non-negative")
            return

        remaining_quantity = max_quantity - consumed_quantity

        cursor = self.conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM inventory WHERE item_name = ?", (item_name,))
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Duplicate Entry", "An item with this name already exists")
            return

        cursor.execute("INSERT INTO inventory (item_name, min_quantity, max_quantity, consumed_quantity, supplier_emails) VALUES (?, ?, ?, ?, ?)",
                   (item_name, min_quantity, max_quantity, consumed_quantity, supplier_emails))
        self.conn.commit()

        if remaining_quantity <= min_quantity:
            self.send_email_notification(supplier_emails, item_name, remaining_quantity)

        messagebox.showinfo("Success", "Inventory item added successfully")
        self.refresh_inventory_list()  # Refresh the list after adding the item
        
    def update(self):
        selected_item = self.item_combobox.get()
        quantity_consumed = self.new_quantity_entry.get()

        if not selected_item or not quantity_consumed.isdigit() or int(quantity_consumed) < 0:
            messagebox.showerror("Input Error", "Please select a valid item and enter a valid quantity")
            return

        quantity_consumed = int(quantity_consumed)
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, consumed_quantity, min_quantity, max_quantity, supplier_emails FROM inventory WHERE item_name = ?", (selected_item,))
        item = cursor.fetchone()

        if not item:
            messagebox.showerror("Error", "Item not found")
            return

        item_id, consumed_quantity, min_quantity, max_quantity, supplier_emails = item
        new_consumed_quantity = consumed_quantity + quantity_consumed
        remaining_quantity = max_quantity - new_consumed_quantity

        cursor.execute("UPDATE inventory SET consumed_quantity = ? WHERE id = ?", (new_consumed_quantity, item_id))
        self.conn.commit()

        if remaining_quantity <= min_quantity:
            self.send_email_notification(supplier_emails, selected_item, remaining_quantity)

        messagebox.showinfo("Success", f"Item updated successfully! Remaining Quantity: {remaining_quantity}")
        self.refresh_inventory_list()    

    def confirm_delete_inventory_item(self):
        selected_item = self.inventory_var.get()
        if not selected_item:
            messagebox.showerror("Error", "Please select an item")
            return

        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT id FROM inventory WHERE item_name = ?", (selected_item,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Error", "Selected item not found")
                return
                
            item_id = result[0]
            
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the inventory item '{selected_item}'?")
            if confirm:
                cursor.execute("DELETE FROM inventory WHERE item_name = ?", (selected_item,))
                self.conn.commit()
                
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", f"Inventory item '{selected_item}' deleted successfully")
                else:
                    messagebox.showerror("Error", "Failed to delete inventory item")
            else:
                messagebox.showinfo("Cancelled", "Item deletion cancelled")
                
        except sqlite3.Error as e:
            self.conn.rollback()  # Rollback in case of error
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
        finally:
            cursor.close()
            self.refresh_inventory_list()

    def get_inventory_items(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT item_name FROM inventory")
        items = cursor.fetchall()
        return [item[0] for item in items]

    def refresh_inventory_list(self):
        updated_item = self.get_inventory_items()
        self.inventory_combobox.configure(values=updated_item)
        self.item_combobox.configure(values=updated_item)
        self.item_combobox.set('')
        self.inventory_var.set('')
        cursor = self.conn.cursor()
        try:
            # Fetch the inventory data
            cursor.execute("SELECT item_name, min_quantity, max_quantity, consumed_quantity, supplier_emails FROM inventory")
            rows = cursor.fetchall()
    
            # Clear existing labels in the table frame
            for widget in self.table_frame.winfo_children():
                if isinstance(widget, customtkinter.CTkLabel):
                    widget.destroy()
    
            # Recreate column headers
            headers = ["Item Name", "Min Quantity", "Max Quantity", "Consumed Quantity", "Supplier Emails"]
            for col, header in enumerate(headers):
                customtkinter.CTkLabel(self.table_content, text=header, font=("Helvetica", 14, "bold")).grid(row=1, column=col, padx=10, pady=5)
    
            # Populate the table with new data
            for row, item in enumerate(rows, start=2):
                for col, value in enumerate(item):
                    customtkinter.CTkLabel(self.table_content, text=value).grid(row=row, column=col, padx=10, pady=5)
            self.table_content.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
        except sqlite3.Error as err:
            messagebox.showerror("Error", f"Error fetching data from database: {err}")
        finally:
            cursor.close()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def send_email_notification(self, supplier_emails, item_name, remaining_quantity):
        subject = f"Restock Notification for {item_name}"
        body = f"The remaining quantity of {item_name} has reached the minimum level ({remaining_quantity}). Please restock the item as soon as possible."

        supplier_email_list = supplier_emails.split(',')  # Split the supplier emails if there are multiple

        for email in supplier_email_list:
            self.send_email(email.strip(), subject, body)

    def send_email(self, to_email, subject, body):
        from_email = "snehasharma18072001@gmail.com"
        password = "hmfjjcpncttlzyps"
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(from_email, password)
                text = msg.as_string()
        
                server.sendmail(from_email, to_email, text)
                print("Email sent successfully")
        except:
            print("Error: unable to send email")

    def load_login_details(self):
        if os.path.exists("login_details.pkl"):
            with open("login_details.pkl", "rb") as file:
                login_details = pickle.load(file)
                self.userid_entry.insert(0, login_details.get("email", ""))
                self.password_entry.insert(0, login_details.get("password", ""))
                self.remember_var.set(True)

    def save_login_details(self):
        if self.remember_var.get():
            login_details = {
                "email": self.userid_entry.get(),
                "password": self.password_entry.get()
            }
            with open("login_details.pkl", "wb") as file:
                pickle.dump(login_details, file)
        else:
            if os.path.exists("login_details.pkl"):
                os.remove("login_details.pkl")
                
    def logout(self):
        #self.logged_in_user = None
        self.clear_screen()
        self.login_screen()

    def cancel_submit(self):
        if self.logged_in_user[2] == "Admin":
            self.admin_screen()
        elif self.logged_in_user[2] == "User":
            self.user_screen()

    def cancel_delete(self):
        if self.logged_in_user[2] == "Admin":
            self.admin_screen()
        elif self.logged_in_user[2] == "User":
            self.user_screen()


    def cancel_update(self):
        if self.logged_in_user[2] == "Admin":
            self.admin_screen()
        elif self.logged_in_user[2] == "User":
            self.user_screen()

    def delete_login_details(self):
        try:
            os.remove("login_details.txt")  # Assuming you saved login details in a file
            messagebox.showinfo("Info", "Login details deleted")
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No login details found to delete")

    def change_theme(self):
        if self.mode == "dark":
            self.mode = "light"
            customtkinter.set_appearance_mode("light")
        else:
            self.mode = "dark"
            customtkinter.set_appearance_mode("dark")

if __name__ == "__main__":
    root = customtkinter.CTk()
    app = InventoryManagementSystem(root)
    root.mainloop()
