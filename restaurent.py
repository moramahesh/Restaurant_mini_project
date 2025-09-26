import mysql.connector
from datetime import datetime
from decimal import Decimal
from adminFile import *
from userFile import *

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",       # put your MySQL root password
    database="restaurant_db"
)
cursor = db.cursor(dictionary=True)


def main():
    while True:
        print("\n=== Restaurant Management ===")
        print("1. Admin Login")
        print("2. User Login")
        print("0. Exit")
        ch = input("Enter choice: ")

        if ch == '1':
            if admin_login(cursor):
                while True:
                    print("\n--- Admin Menu ---")
                    print("1. Add Menu Item")
                    print("2. Delete Menu Item")
                    print("3. Modify Menu Item")
                    print("4. View Menu")
                    print("5. View Orders")
                    print("6. Day-wise Profit")
                    print("0. Logout")
                    c = input("Enter choice: ")
                    if c == '1': add_menu_item(db,cursor)
                    elif c == '2': delete_menu_item(db,cursor)
                    elif c == '3': modify_menu_item(db,cursor)
                    elif c == '4': view_menu_items(cursor)
                    elif c == '5': view_orders(cursor)
                    elif c == '6': day_wise_profit(cursor)
                    elif c == '0': break

        elif ch == '2':
            user = user_login()
            user_cart_process(user,db,cursor)

        elif ch == '0':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()