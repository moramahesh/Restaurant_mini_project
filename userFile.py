def user_login():
    name = input("Enter your name: ")
    mobile = input("Enter your mobile: ")
    print(f"Welcome {name}!")
    return {"name": name, "mobile": mobile}

def user_view_menu(cursor):
    cursor.execute("SELECT * FROM menu_items")
    rows = cursor.fetchall()
    print("\n--- MENU ---")
    for r in rows:
        print(f"{r['id']}. {r['name']} ({r['category']}) - ₹{r['price']}")
    return rows

def user_cart_process(user,db,cursor):
    cart = {}
    while True:
        rows = user_view_menu(cursor)
        choice = input("Enter item ID to add: ")
        if choice.lower() == 'done':
            break
        qty = int(input("Enter quantity: "))
        cursor.execute("SELECT * FROM menu_items WHERE id=%s", (choice,))
        item = cursor.fetchone()
        if item:
            cart[choice] = {"id": item['id'], "name": item['name'], "qty": qty,
                            "price": float(item['price']), "cost": float(item['cost_price'])}
            print(f"Added {qty} x {item['name']} to cart ✅")

    if not cart:
        print("Cart is empty ❌")
        return

    # Show bill
    total = sum(v['qty']*v['price'] for v in cart.values())
    total_cost = sum(v['qty']*v['cost'] for v in cart.values())
    profit = total - total_cost

    print("\n--- BILL ---")
    for v in cart.values():
        print(f"{v['name']} x {v['qty']} = ₹{v['qty']*v['price']}")
    print(f"Total: ₹{total}, Profit: ₹{profit}")
    print("-------------")

    # Save order
    cursor.execute("INSERT INTO orders (user_name, user_mobile, total_amount, total_cost, profit) VALUES (%s,%s,%s,%s,%s)",
                   (user['name'], user['mobile'], total, total_cost, profit))
    order_id = cursor.lastrowid

    for v in cart.values():
        cursor.execute("INSERT INTO order_items (order_id, menu_item_id, name, qty, unit_price, line_total) VALUES (%s,%s,%s,%s,%s,%s)",
                       (order_id, v['id'], v['name'], v['qty'], v['price'], v['qty']*v['price']))
    db.commit()
    print("Order placed successfully ✅")