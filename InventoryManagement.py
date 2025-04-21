"""
# Program: Inventory Management System 

# Written by: Noemi Abreu, Aryan Ranade 

# Date: 04/22/2025 

# Description: This program helps users (business owners or warehouse managers) 

# manage inventory items by adding, removing, updating, and tracking 

# products. It includes authentication, data persistence, and a GUI 

# for interaction. 

# Challenges:   Designing the visual interface with Figma and tkinter. 

# Time Spent:    Estimated total 25+ hours (team effort) 

# Features Used: 

# 1. If-elif-else statements 

# 2. While loops 

# 3. Boolean logic 

# 4. Dictionaries 

# 5. File read/write operations (JSON) 

# Example Inputs and Expected Outputs: 

# User logs in with admin / 010101 → "Login Successful" 

# Adds item with ID 1001, quantity 5, price $10 → "Item added successfully!" 

# Tries removing nonexistent item → "Item not found!" 
"""

import json
import os
import tkinter as tk
from tkinter import ttk

base_dir = os.path.dirname(__file__)

# Define constants
FILE_NAME = os.path.join(base_dir, 'inventory_data.json')
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "010101"

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("800x500")
        self.root.resizable(True, True)
        
        # Initialize inventory
        self.inventory = {}
        self.load_inventory()
        
        # Set up the main container
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Login first
        self.show_login()
        
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")


    def load_inventory(self):
        """Load inventory data from file"""
        if os.path.exists(FILE_NAME):
            try:
                with open(FILE_NAME, 'r') as file:
                    self.inventory = json.load(file)
            except Exception as e:
                self.status_var.set(f"Error: Failed to load inventory: {str(e)}")
        else:
            # Create empty inventory
            self.inventory = {}
    
    def save_inventory(self):
        """Save inventory data to file"""
        try:
            with open(FILE_NAME, 'w') as file:
                json.dump(self.inventory, file, indent=4)
            self.status_var.set("Inventory saved successfully")
        except Exception as e:
            self.status_var.set(f"Error: Failed to save inventory: {str(e)}")
    
    def show_login(self):
        """Display login window"""
        # Clear frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create login form
        login_frame = tk.Frame(self.main_frame)
        login_frame.pack(expand=True)
        
        # Title
        title_label = tk.Label(login_frame, text="Inventory Management System", font=("Poppins", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Username
        username_label = tk.Label(login_frame, text="Username:", font=("Poppins", 12))
        username_label.grid(row=1, column=0, sticky="e", padx=5, pady=10)
        self.username_entry = tk.Entry(login_frame, font=("Poppins", 12))
        self.username_entry.grid(row=1, column=1, padx=5, pady=10)
        
        # Password
        password_label = tk.Label(login_frame, text="Password:", font=("Poppins", 12))
        password_label.grid(row=2, column=0, sticky="e", padx=5, pady=10)
        self.password_entry = tk.Entry(login_frame, show="*", font=("Poppins", 12))
        self.password_entry.grid(row=2, column=1, padx=5, pady=10)
        
        # Status label for login errors
        self.login_status = tk.Label(login_frame, text="", fg="red", font=("Poppins", 10))
        self.login_status.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Login button
        login_button = tk.Button(login_frame, text="Login", command=self.authenticate, 
                               font=("Poppins", 12), width=10)
        login_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Bind Enter key
        self.password_entry.bind("<Return>", lambda event: self.authenticate())
    
    def authenticate(self):
        """Verify login credentials"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            self.show_main_interface()
        else:
            self.login_status.config(text="Invalid username or password")
    
    def show_main_interface(self):
        """Display the main interface after login"""
        # Clear frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create main interface
        # Top button panel
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Create buttons with consistent syling
        button_style = {"font": ("Poppins", 12), "width": 12, "height":1,}
        
        add_btn = tk.Button(button_frame, text="Add Item", command=self.add_item_window, **button_style)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        remove_btn = tk.Button(button_frame, text="Remove Item", command=self.remove_item, **button_style)
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        update_qty_btn = tk.Button(button_frame, text="Update Quantity", command=self.update_quantity_window, **button_style)
        update_qty_btn.pack(side=tk.LEFT, padx=5)
        
        update_price_btn = tk.Button(button_frame, text="Update Price", command=self.update_price_window, **button_style)
        update_price_btn.pack(side=tk.LEFT, padx=5)
        
        calc_btn = tk.Button(button_frame, text="Total Value", command=self.calculate_total, **button_style)
        calc_btn.pack(side=tk.LEFT, padx=5)
        
        exit_btn = tk.Button(button_frame, text="Exit", command=self.root.quit, **button_style)
        exit_btn.pack(side=tk.LEFT, padx=5)
        
        # Treeview for inventory
        tree_frame = tk.Frame(self.main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create treeview
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        # Define columns
        self.tree['columns'] = ('name', 'quantity', 'price', 'sku')
        
        # Format columns
        self.tree.column('#0', width=80, minwidth=80)  # ID column
        self.tree.column('name', width=200, minwidth=150)
        self.tree.column('quantity', width=100, minwidth=80)
        self.tree.column('price', width=100, minwidth=80)
        self.tree.column('sku', width=120, minwidth=80)
        
        # Create headings
        self.tree.heading('#0', text='Item ID')
        self.tree.heading('name', text='Name')
        self.tree.heading('quantity', text='Quantity')
        self.tree.heading('price', text='Price')
        self.tree.heading('sku', text='SKU')
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bottom status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.main_frame, textvariable=self.status_var, 
                             bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load inventory data into treeview
        self.refresh_inventory()
    
    def refresh_inventory(self):
        """Refresh the inventory display"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load inventory items
        for item_id, item_data in self.inventory.items():
            self.tree.insert('', tk.END, text=item_id, values=(
                item_data['name'],
                item_data['quantity'],
                f"${item_data['price']:.2f}",
                item_data['sku'] if item_data['sku'] else ""
            ))
        
        self.status_var.set(f"Inventory loaded - {len(self.inventory)} items")
    
    def add_item_window(self):
        """Open a window to add a new item"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Item")
        add_window.geometry("300x350")
        add_window.transient(self.root)
        add_window.grab_set()
        
        # Create form
        form_frame = tk.Frame(add_window, padx=10, pady=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Item ID
        tk.Label(form_frame, text="Item ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        id_entry = tk.Entry(form_frame)
        id_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Name
        tk.Label(form_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        name_entry = tk.Entry(form_frame)
        name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Quantity
        tk.Label(form_frame, text="Quantity:").grid(row=2, column=0, sticky=tk.W, pady=5)
        qty_entry = tk.Entry(form_frame)
        qty_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        qty_entry.insert(0, "0")
        
        # Price
        tk.Label(form_frame, text="Price:").grid(row=3, column=0, sticky=tk.W, pady=5)
        price_entry = tk.Entry(form_frame)
        price_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        price_entry.insert(0, "0.00")
        
        # SKU
        tk.Label(form_frame, text="SKU:").grid(row=4, column=0, sticky=tk.W, pady=5)
        sku_entry = tk.Entry(form_frame)
        sku_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Status label for messages/errors
        status_label = tk.Label(form_frame, text="", fg="red")
        status_label.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Submit button
        def add_item_submit():
            try:
                item_id = id_entry.get().strip()
                name = name_entry.get().strip()
                
                # Validate required fields
                if not item_id or not name:
                    status_label.config(text="Item ID and Name are required")
                    return
                    
                if item_id in self.inventory:
                    status_label.config(text="Item ID already exists")
                    return
                
                # Validate numeric fields
                try:
                    quantity = int(qty_entry.get())
                    price = float(price_entry.get())
                    
                    if quantity < 0:
                        status_label.config(text="Quantity cannot be negative")
                        return
                        
                    if price < 0:
                        status_label.config(text="Price cannot be negative")
                        return
                except ValueError:
                    status_label.config(text="Invalid quantity or price")
                    return
                
                sku = sku_entry.get().strip()
                
                # Add to inventory
                self.inventory[item_id] = {
                    "item_id": item_id,
                    "name": name,
                    "quantity": quantity,
                    "price": price,
                    "sku": sku
                }
                
                # Save and refresh
                self.save_inventory()
                self.refresh_inventory()
                
                # Close window
                add_window.destroy()
                self.status_var.set("Item added successfully")
                
            except Exception as e:
                status_label.config(text=f"Error: {str(e)}")
        
        submit_btn = tk.Button(form_frame, text="Add Item", command=add_item_submit)
        submit_btn.grid(row=6, column=0, columnspan=2, pady=15)
        
        # Cancel button
        cancel_btn = tk.Button(form_frame, text="Cancel", command=add_window.destroy)
        cancel_btn.grid(row=7, column=0, columnspan=2, pady=5)
    
    def get_selected_item(self):
        """Get the selected item ID or None"""
        selection = self.tree.selection()
        if not selection:
            self.status_var.set("Warning: Please select an item first")
            return None
        
        return self.tree.item(selection[0], 'text')
    
    def remove_item(self):
        """Remove the selected item"""
        item_id = self.get_selected_item()
        if not item_id:
            return
        
        # Create a confirmation dialog 
        confirm_window = tk.Toplevel(self.root)
        confirm_window.title("Confirm Removal")
        confirm_window.geometry("300x150")
        confirm_window.transient(self.root)
        confirm_window.grab_set()
        
        # Dialog content
        tk.Label(confirm_window, text=f"Are you sure you want to remove item {item_id}?", 
                 wraplength=250).pack(pady=20)
        
        # Buttons frame
        btn_frame = tk.Frame(confirm_window)
        btn_frame.pack(pady=10)
        
        # Yes button
        def confirm_yes():
            if item_id in self.inventory:
                del self.inventory[item_id]
                self.save_inventory()
                self.refresh_inventory()
                self.status_var.set("Item removed successfully")
            confirm_window.destroy()
        
        yes_btn = tk.Button(btn_frame, text="Yes", command=confirm_yes, width=10)
        yes_btn.pack(side=tk.LEFT, padx=10)
        
        # No button
        no_btn = tk.Button(btn_frame, text="No", command=confirm_window.destroy, width=10)
        no_btn.pack(side=tk.LEFT, padx=10)
    
    def update_quantity_window(self):
        """Open window to update quantity"""
        item_id = self.get_selected_item()
        if not item_id:
            return
        
        # Get current quantity
        current_qty = self.inventory[item_id]["quantity"]
        
        # Create dialog
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Quantity")
        update_window.geometry("300x200")
        update_window.transient(self.root)
        update_window.grab_set()
        
        # Form
        tk.Label(update_window, text=f"Item: {self.inventory[item_id]['name']}").pack(pady=10)
        tk.Label(update_window, text=f"Current Quantity: {current_qty}").pack()
        
        # New quantity
        frame = tk.Frame(update_window)
        frame.pack(pady=10)
        tk.Label(frame, text="New Quantity:").pack(side=tk.LEFT)
        qty_entry = tk.Entry(frame, width=10)
        qty_entry.pack(side=tk.LEFT, padx=5)
        qty_entry.insert(0, str(current_qty))
        
        # Status label
        status_label = tk.Label(update_window, text="", fg="red")
        status_label.pack(pady=5)
        
        # Buttons frame
        btn_frame = tk.Frame(update_window)
        btn_frame.pack(pady=10)
        
        # Submit button
        def update_qty_submit():
            try:
                new_qty = int(qty_entry.get())
                if new_qty < 0:
                    status_label.config(text="Quantity cannot be negative")
                    return
                
                # Update inventory
                self.inventory[item_id]["quantity"] = new_qty
                self.save_inventory()
                self.refresh_inventory()
                
                # Close window
                update_window.destroy()
                self.status_var.set("Quantity updated successfully")
                
            except ValueError:
                status_label.config(text="Please enter a valid number")
        
        update_btn = tk.Button(btn_frame, text="Update", command=update_qty_submit, width=10)
        update_btn.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_btn = tk.Button(btn_frame, text="Cancel", command=update_window.destroy, width=10)
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def update_price_window(self):
        """Open window to update price"""
        item_id = self.get_selected_item()
        if not item_id:
            return
        
        # Get current price
        current_price = self.inventory[item_id]["price"]
        
        # Create dialog
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Price")
        update_window.geometry("300x200")
        update_window.transient(self.root)
        update_window.grab_set()
        
        # Form
        tk.Label(update_window, text=f"Item: {self.inventory[item_id]['name']}").pack(pady=10)
        tk.Label(update_window, text=f"Current Price: ${current_price:.2f}").pack()
        
        # New price
        frame = tk.Frame(update_window)
        frame.pack(pady=10)
        tk.Label(frame, text="New Price:").pack(side=tk.LEFT)
        price_entry = tk.Entry(frame, width=10)
        price_entry.pack(side=tk.LEFT, padx=5)
        price_entry.insert(0, str(current_price))
        
        # Status label
        status_label = tk.Label(update_window, text="", fg="red")
        status_label.pack(pady=5)
        
        # Buttons frame
        btn_frame = tk.Frame(update_window)
        btn_frame.pack(pady=10)
        
        # Submit button
        def update_price_submit():
            try:
                new_price = float(price_entry.get())
                if new_price < 0:
                    status_label.config(text="Price cannot be negative")
                    return
                
                # Update inventory
                self.inventory[item_id]["price"] = new_price
                self.save_inventory()
                self.refresh_inventory()
                
                # Close window
                update_window.destroy()
                self.status_var.set("Price updated successfully")
                
            except ValueError:
                status_label.config(text="Please enter a valid number")
        
        update_btn = tk.Button(btn_frame, text="Update", command=update_price_submit, width=10)
        update_btn.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_btn = tk.Button(btn_frame, text="Cancel", command=update_window.destroy, width=10)
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def calculate_total(self):
        """Calculate and display total inventory value"""
        total = 0
        for item_id, item_data in self.inventory.items():
            total += item_data["quantity"] * item_data["price"]
        
        # Show total in status bar
        self.status_var.set(f"Total Inventory Value: ${total:.2f}")
     
        total_window = tk.Toplevel(self.root)
        total_window.title("Total Inventory Value")
        total_window.geometry("300x160")
        total_window.transient(self.root)
        total_window.grab_set()
        
        # Show total
        tk.Label(total_window, text="Total Inventory Value", font=("Poppins", 12, "bold")).pack(pady=10)
        tk.Label(total_window, text=f"${total:.2f}", font=("Poppins", 14)).pack(pady=10)
        
        # OK button
        tk.Button(total_window, text="OK", command=total_window.destroy, width=10).pack(pady=10)

# Main function
def main():
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    
