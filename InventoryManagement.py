"""
Inventory Management System in Python 
Features used (5 of the requested requirements):
1. If-elif-else statements
2. While Loop statements
3. Dictionary data structures
4. Boolean statements
5. File Read/Write operations
"""

import json
import os
import tkinter as tk 
from tkinter import messagebox, simpledialog

# Define constants
MAX_ITEMS = 1000
MIN_QUANTITY = 0
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "010101"
FILE_NAME = "inventory_data.json"  

# Define Item class
class InventoryItem:
    # Initialize method
    def __init__(self, item_id, name, quantity, price, sku):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.sku = sku
    
    # Method to update quantity
    def update_quantity(self, new_quantity):
        if new_quantity >= MIN_QUANTITY:
            self.quantity = new_quantity
            print("Quantity updated successfully!")
        else:
            print(f"Invalid quantity! Must be greater than or equal to {MIN_QUANTITY}")
    
    # Method to update price
    def update_price(self, new_price):
        try:
            new_price = float(new_price)  # Convert input to float
            if new_price >= 0:
                self.price = new_price
                print("Price updated successfully!")
            else:
                print("Invalid price! Price cannot be negative.")
        except ValueError:
            print("Invalid input! Please enter a valid number for the price.")
        
    # Method to add SKU
    def add_sku(self, sku):
        self.sku = sku
        print("SKU added successfully!")
    
    # Method to remove SKU
    def remove_sku(self):
        self.sku = None
        print("SKU removed successfully!")
    
    # Method to display item details
    def display_item(self):
        print("--------------------------")
        print(f"Item ID: {self.item_id}")
        print(f"Name: {self.name}")
        print(f"Quantity: {self.quantity}")
        print(f"Price: {self.price}")
        print(f"SKU: {self.sku}")


    # For JSON serialization
    def to_dict(self):
        return {
            "item_id": self.item_id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
            "sku": self.sku
        }


# Define Inventory class
class Inventory:
    # Initialize method
    def __init__(self):
        self.items = {}  
        self.load_inventory_from_file()
    
    # Method to add item
    def add_item(self, item_id, name, quantity, price, sku):
        if len(self.items) < MAX_ITEMS:
            if item_id in self.items:
                print("Item already exists!")
            else:
                self.items[item_id] = InventoryItem(item_id, name, quantity, price, sku)
                print("Item added successfully!")
                self.save_inventory_to_file()
        else:
            print(f"Inventory is full! Maximum capacity is {MAX_ITEMS} items.")
    
    # Method to remove item
    def remove_item(self, item_id):
        if item_id in self.items:   
            del self.items[item_id]
            print("Item removed successfully!")
            self.save_inventory_to_file()
        else:
            print("Item not found!")
    
    # Method to update item quantity
    def update_item_quantity(self, item_id, new_quantity):
        if item_id in self.items:
            self.items[item_id].update_quantity(new_quantity)
            self.save_inventory_to_file()
        else:
            print("Item not found!")
    
    # Method to update item price
    def update_item_price(self, item_id, new_price):
        if item_id in self.items:
            self.items[item_id].update_price(new_price)
            self.save_inventory_to_file()
        else:
            print("Item not found!")
    
    # Method to add SKU
    def add_sku(self, item_id, sku):
        if item_id in self.items:
            self.items[item_id].add_sku(sku)
            self.save_inventory_to_file()
        else:
            print("Item not found!")
    
    # Method to remove SKU
    def remove_sku(self, item_id):
        if item_id in self.items:
            self.items[item_id].remove_sku()
            self.save_inventory_to_file()
        else:
            print("Item not found!")
    
    # Method to search for an item
    def search_item(self, item_id):
        if item_id in self.items:
            print("Item Found:")
            self.items[item_id].display_item()
        else:
            print("Item not found!")
    
    # Method to display all inventory
    def display_inventory(self):
        if not self.items:
            print("Inventory is empty!")
        else:
            for item_id in self.items:
                self.items[item_id].display_item()
    
    # Method to calculate total inventory value
    def calculate_total_value(self):
        total_value = 0
        for item_id in self.items:
            total_value += self.items[item_id].quantity * self.items[item_id].price
        print(f"Total Inventory Value: ${total_value}")
        return total_value
    
    # Method to generate stock alert
    def generate_stock_alert(self, threshold):
        print("Stock Alert Report:")
        print("--------------------------")
        for item_id in self.items:
            if self.items[item_id].quantity < threshold:
                print(f"Stock Alert: Low stock for {self.items[item_id].name} - Current Quantity: {self.items[item_id].quantity}")
    
    # Method to save inventory to file
    def save_inventory_to_file(self):
        try:
            inventory_data = {}
            for item_id, item in self.items.items():
                inventory_data[item_id] = item.to_dict()
            
            with open(FILE_NAME, 'w') as file:
                json.dump(inventory_data, file, indent=4)
            # print("Inventory saved to file.")
        except Exception as e:
            print(f"Error saving inventory: {e}")
    
    # Method to load inventory from file
    def load_inventory_from_file(self):
        if not os.path.exists(FILE_NAME):
            print("No inventory file found. Starting with empty inventory.")
            return
        
        try:
            with open(FILE_NAME, 'r') as file:
                inventory_data = json.load(file)
            
            self.items = {}
            for item_id, item_data in inventory_data.items():
                self.items[item_id] = InventoryItem(
                    item_data["item_id"],
                    item_data["name"],
                    item_data["quantity"],
                    item_data["price"],
                    item_data["sku"]
                )
            print("Inventory loaded from file.")
        except Exception as e:
            print(f"Error loading inventory: {e}")


# Define Authentication System
class AuthenticationSystem:
    # Method to authenticate user
    def authenticate(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            print("Login Successful")
            return True
        else:
            print("Username or password incorrect. Unauthorized user please try again.")
            return False


# Main System class
class InventoryManagementSystem:
    # Initialize method
    def __init__(self):
        self.auth_system = AuthenticationSystem()
        self.inventory = Inventory()
    
    # Method to run the system
    def run(self):
        # Display welcome message
        print("Welcome to the Inventory Management System")
        # Authenticate user
        while True:
            authenticated = self.auth_system.authenticate()
            if authenticated:
                break
        # Main menu loop
        self.display_main_menu()
    
    # Method to display main menu
    def display_main_menu(self):
        while True:
            # Display menu options
            print("\nWhat would you like to do?")
            print("1. Add Item")
            print("2. Remove Item")
            print("3. Update Quantity")
            print("4. Update Price")
            print("5. Search Item")
            print("6. Add SKU Code")
            print("7. Remove SKU Code")
            print("8. View Inventory")
            print("9. Calculate Total Inventory")
            print("10. Generate a Stock Alert")
            print("11. Exit")
            # Get user choice
            try:
                user_choice = int(input("Enter your choice: "))
                # Process user choice
                if user_choice == 1:
                    self.add_item_menu()
                elif user_choice == 2:
                    self.remove_item_menu()
                elif user_choice == 3:
                    self.update_quantity_menu()
                elif user_choice == 4:
                    self.update_price_menu()
                elif user_choice == 5:
                    self.search_item_menu()
                elif user_choice == 6:
                    self.add_sku_menu()
                elif user_choice == 7:
                    self.remove_sku_menu()
                elif user_choice == 8:
                    self.inventory.display_inventory()
                elif user_choice == 9:
                    self.inventory.calculate_total_value()
                elif user_choice == 10:
                    self.generate_alert_menu()
                elif user_choice == 11:
                    print("Ending system... GOODBYE!")
                    return
                else:
                    print("Invalid choice. Please choose an option between 1 and 11.")
            except ValueError:
                print("Please enter a number.")
    
    # Menu methods for each operation
    def add_item_menu(self):
        item_id = input("Enter Item ID: ")
        name = input("Enter Item Name: ")
        try:
            quantity = int(input("Enter Quantity: "))
            price = float(input("Enter Price: "))
            sku = input("Enter SKU: ")
            self.inventory.add_item(item_id, name, quantity, price, sku)
        except ValueError:
            print("Invalid input. Quantity must be an integer and Price must be a number.")
    
    def remove_item_menu(self):
        item_id = input("Enter Item ID to remove: ")
        self.inventory.remove_item(item_id)
    
    def update_quantity_menu(self):
        item_id = input("Enter Item ID: ")
        try:
            new_quantity = int(input("Enter new quantity: "))
            self.inventory.update_item_quantity(item_id, new_quantity)
        except ValueError:
            print("Invalid input. Quantity must be an integer.")
    
    def update_price_menu(self):
        item_id = input("Enter Item ID: ")
        try:
            new_price = float(input("Enter new price: "))
            self.inventory.update_item_price(item_id, new_price)
        except ValueError:
            print("Invalid input. Price must be a number.")
    
    def search_item_menu(self):
        item_id = input("Enter Item ID to search: ")
        self.inventory.search_item(item_id)
    
    def add_sku_menu(self):
        item_id = input("Enter Item ID: ")
        sku = input("Enter SKU code: ")
        self.inventory.add_sku(item_id, sku)
    
    def remove_sku_menu(self):
        item_id = input("Enter Item ID: ")
        self.inventory.remove_sku(item_id)
    
    def generate_alert_menu(self):
        try:
            threshold = 15
            self.inventory.generate_stock_alert(threshold)
        except ValueError:
            print("Invalid input. Threshold must be an integer.")


# Main program entry point
if __name__ == "__main__":
    system = InventoryManagementSystem()
    system.run()


#We need to create a visual interface now!!


