def admin_login(cursor):
    user = input("Enter admin username: ")
    pwd = input("Enter password: ")
    cursor.execute("SELECT * FROM admins WHERE username=%s AND password=%s", (user, pwd))
    admin = cursor.fetchone()
    if admin:
        print("Admin login successful ✅")
        return True
    else:
        print("Invalid admin credentials ❌")
        return False

def add_menu_item(db,cursor):
    name = input("Item name: ")
    cat = input("Category: ")
    price = float(input("Selling price: "))
    cost = float(input("Cost price: "))
    cursor.execute("INSERT INTO menu_items (name, category, price, cost_price) VALUES (%s,%s,%s,%s)",
                   (name, cat, price, cost))
    db.commit()
    print("Item added successfully ✅")

def delete_menu_item(db,cursor):
    item_id = int(input("Enter item ID to delete: "))
    cursor.execute("DELETE FROM menu_items WHERE id=%s", (item_id,))
    db.commit()
    print("Item deleted ❌")

def modify_menu_item(db,cursor):
    item_id = int(input("Enter item ID to modify: "))
    name = input("New name: ")
    cat = input("New category: ")
    price = float(input("New price: "))
    cost = float(input("New cost price: "))
    cursor.execute("UPDATE menu_items SET name=%s, category=%s, price=%s, cost_price=%s WHERE id=%s",
                   (name, cat, price, cost, item_id))
    db.commit()
    print("Item updated ✅")

def view_menu_items(cursor):
    cursor.execute("SELECT * FROM menu_items")
    rows = cursor.fetchall()
    print("\n----- MENU -----")
    for r in rows:
        print(f"{r['id']}. {r['name']} ({r['category']}) - ₹{r['price']}")
    print("-------------------")

def view_orders(cursor):
    cursor.execute("SELECT * FROM orders ORDER BY created_at DESC")
    rows = cursor.fetchall()
    for o in rows:
        print(f"Order {o['id']} | {o['user_name']} | ₹{o['total_amount']} | Profit: ₹{o['profit']} | {o['created_at']}")

def day_wise_profit(cursor):
    cursor.execute("""
        SELECT DATE(created_at) as day, SUM(total_amount) as revenue, SUM(total_cost) as cost, SUM(profit) as profit
        FROM orders GROUP BY DATE(created_at) ORDER BY day DESC
    """)
    rows = cursor.fetchall()
    print("\n--- Day Wise Profit ---")
    for r in rows:
        print(f"{r['day']} | Revenue: ₹{r['revenue']} | Cost: ₹{r['cost']} | Profit: ₹{r['profit']}")
    print("------------------------")