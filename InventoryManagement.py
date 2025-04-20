"""
# Program: Inventory Management System 

# Written by: Noemi Abreu, Aryan Ranade 

# Date: [April 22, 2025] 

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

# Define constants
MAX_ITEMS = 1000
MIN_QUANTITY = 0
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "010101"
FILE_NAME = "inventory_data.json"

# Global inventory variable
inventory = {}

# File operations functions
def save_inventory_to_file():
    try:
        with open(FILE_NAME, 'w') as file:
            json.dump(inventory, file, indent=4)
    except Exception as e:
        print(f"Error saving inventory: {e}")

def load_inventory_from_file():
    global inventory
    if not os.path.exists(FILE_NAME):
        print("No inventory file found. Starting with empty inventory.")
        return
    
    try:
        with open(FILE_NAME, 'r') as file:
            inventory = json.load(file)
        print("Inventory loaded from file.")
    except Exception as e:
        print(f"Error loading inventory: {e}")

# Inventory management functions
def add_item(item_id, name, quantity, price, sku):
    if len(inventory) < MAX_ITEMS:
        if item_id in inventory:
            print("Item already exists!")
        else:
            inventory[item_id] = {
                "item_id": item_id,
                "name": name,
                "quantity": quantity,
                "price": price,
                "sku": sku
            }
            print("Item added successfully!")
            save_inventory_to_file()
    else:
        print(f"Inventory is full! Maximum capacity is {MAX_ITEMS} items.")

def remove_item(item_id):
    if item_id in inventory:
        del inventory[item_id]
        print("Item removed successfully!")
        save_inventory_to_file()
    else:
        print("Item not found!")

def update_quantity(item_id, new_quantity):
    if item_id in inventory:
        if new_quantity >= MIN_QUANTITY:
            inventory[item_id]["quantity"] = new_quantity
            print("Quantity updated successfully!")
            save_inventory_to_file()
        else:
            print(f"Invalid quantity! Must be greater than or equal to {MIN_QUANTITY}")
    else:
        print("Item not found!")

def update_price(item_id, new_price):
    if item_id in inventory:
        try:
            new_price = float(new_price)
            if new_price >= 0:
                inventory[item_id]["price"] = new_price
                print("Price updated successfully!")
                save_inventory_to_file()
            else:
                print("Invalid price! Price cannot be negative.")
        except ValueError:
            print("Invalid input! Please enter a valid number for the price.")
    else:
        print("Item not found!")

def add_sku(item_id, sku):
    if item_id in inventory:
        inventory[item_id]["sku"] = sku
        print("SKU added successfully!")
        save_inventory_to_file()
    else:
        print("Item not found!")

def remove_sku(item_id):
    if item_id in inventory:
        inventory[item_id]["sku"] = None
        print("SKU removed successfully!")
        save_inventory_to_file()
    else:
        print("Item not found!")

def search_item(item_id):
    if item_id in inventory:
        print("Item Found:")
        display_item(item_id)
    else:
        print("Item not found!")

def display_item(item_id):
    item = inventory[item_id]
    print("--------------------------")
    print(f"Item ID: {item['item_id']}")
    print(f"Name: {item['name']}")
    print(f"Quantity: {item['quantity']}")
    print(f"Price: {item['price']}")
    print(f"SKU: {item['sku']}")

def display_inventory():
    if not inventory:
        print("Inventory is empty!")
    else:
        for item_id in inventory:
            display_item(item_id)

def calculate_total_value():
    total_value = 0
    for item_id in inventory:
        total_value += inventory[item_id]["quantity"] * inventory[item_id]["price"]
    print(f"Total Inventory Value: ${total_value}")
    return total_value

def generate_stock_alert(threshold):
    print("Stock Alert Report:")
    print("--------------------------")
    for item_id in inventory:
        if inventory[item_id]["quantity"] < threshold:
            print(f"Stock Alert: Low stock for {inventory[item_id]['name']} - Current Quantity: {inventory[item_id]['quantity']}")

# Authentication function
def authenticate():
    username = input("Enter username: ")
    password = input("Enter password: ")
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("Login Successful")
        return True
    else:
        print("Username or password incorrect. Unauthorized user please try again.")
        return False

# Menu functions
def add_item_menu():
    item_id = input("Enter Item ID: ")
    name = input("Enter Item Name: ")
    try:
        quantity = int(input("Enter Quantity: "))
        price = float(input("Enter Price: "))
        sku = input("Enter SKU: ")
        add_item(item_id, name, quantity, price, sku)
    except ValueError:
        print("Invalid input. Quantity must be an integer and Price must be a number.")

def remove_item_menu():
    item_id = input("Enter Item ID to remove: ")
    remove_item(item_id)

def update_quantity_menu():
    item_id = input("Enter Item ID: ")
    try:
        new_quantity = int(input("Enter new quantity: "))
        update_quantity(item_id, new_quantity)
    except ValueError:
        print("Invalid input. Quantity must be an integer.")

def update_price_menu():
    item_id = input("Enter Item ID: ")
    try:
        new_price = float(input("Enter new price: "))
        update_price(item_id, new_price)
    except ValueError:
        print("Invalid input. Price must be a number.")

def search_item_menu():
    item_id = input("Enter Item ID to search: ")
    search_item(item_id)

def add_sku_menu():
    item_id = input("Enter Item ID: ")
    sku = input("Enter SKU code: ")
    add_sku(item_id, sku)

def remove_sku_menu():
    item_id = input("Enter Item ID: ")
    remove_sku(item_id)

def generate_alert_menu():
    try:
        threshold = 15
        generate_stock_alert(threshold)
    except ValueError:
        print("Invalid input. Threshold must be an integer.")

def display_main_menu():
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
                add_item_menu()
            elif user_choice == 2:
                remove_item_menu()
            elif user_choice == 3:
                update_quantity_menu()
            elif user_choice == 4:
                update_price_menu()
            elif user_choice == 5:
                search_item_menu()
            elif user_choice == 6:
                add_sku_menu()
            elif user_choice == 7:
                remove_sku_menu()
            elif user_choice == 8:
                display_inventory()
            elif user_choice == 9:
                calculate_total_value()
            elif user_choice == 10:
                generate_alert_menu()
            elif user_choice == 11:
                print("Ending system... GOODBYE!")
                return
            else:
                print("Invalid choice. Please choose an option between 1 and 11.")
        except ValueError:
            print("Please enter a number.")

# Main function
def main():
    # Display welcome message
    print("Welcome to the Inventory Management System")
    
    # Load inventory data
    load_inventory_from_file()
    
    # Authenticate user
    while True:
        authenticated = authenticate()
        if authenticated:
            break
    
    # Display main menu
    display_main_menu()

# Run the program
if __name__ == "__main__":
    main()
