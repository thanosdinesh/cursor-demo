# generate_data.py
# Run: pip install faker
from faker import Faker
import csv
import random
from datetime import datetime, timedelta

fake = Faker()
random.seed(0)

NUM_CUSTOMERS = 30
NUM_PRODUCTS = 50
NUM_ORDERS = 100

# 1) customers.csv
customers = []
for cid in range(1, NUM_CUSTOMERS + 1):
    customers.append({
        "customer_id": cid,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "join_date": fake.date_between(start_date='-2y', end_date='today').isoformat()
    })

with open("customers.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=customers[0].keys())
    writer.writeheader()
    writer.writerows(customers)

# 2) products.csv
products = []
for pid in range(1, NUM_PRODUCTS + 1):
    products.append({
        "product_id": pid,
        "product_name": fake.word().capitalize() + " " + fake.word().capitalize(),
        "category": random.choice(["Electronics","Books","Home","Fashion","Sports","Toys"]),
        "price": round(random.uniform(5, 500), 2),
        "stock": random.randint(0, 200)
    })

with open("products.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=products[0].keys())
    writer.writeheader()
    writer.writerows(products)

# 3) orders.csv
orders = []
order_id = 1
for _ in range(NUM_ORDERS):
    cid = random.randint(1, NUM_CUSTOMERS)
    order_date = fake.date_between(start_date='-365d', end_date='today')
    orders.append({
        "order_id": order_id,
        "customer_id": cid,
        "order_date": order_date.isoformat(),
        "status": random.choice(["placed","shipped","delivered","cancelled"])
    })
    order_id += 1

with open("orders.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=orders[0].keys())
    writer.writeheader()
    writer.writerows(orders)

# 4) order_items.csv
order_items = []
oi_id = 1
for o in orders:
    num_items = random.randint(1, 4)
    chosen_products = random.sample(products, k=num_items)
    for p in chosen_products:
        qty = random.randint(1, 5)
        order_items.append({
            "order_item_id": oi_id,
            "order_id": o["order_id"],
            "product_id": p["product_id"],
            "quantity": qty,
            "unit_price": p["price"]
        })
        oi_id += 1

with open("order_items.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=order_items[0].keys())
    writer.writeheader()
    writer.writerows(order_items)

# 5) payments.csv
payments = []
pid_counter = 1
for o in orders:
    amount = 0.0
    for oi in [it for it in order_items if it["order_id"] == o["order_id"]]:
        amount += oi["quantity"] * oi["unit_price"]
    payments.append({
        "payment_id": pid_counter,
        "order_id": o["order_id"],
        "paid_amount": round(amount, 2),
        "payment_date": (datetime.fromisoformat(o["order_date"]) + timedelta(days=random.randint(0,5))).date().isoformat(),
        "payment_method": random.choice(["card","paypal","netbanking"])
    })
    pid_counter += 1

with open("payments.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=payments[0].keys())
    writer.writeheader()
    writer.writerows(payments)

print("Generated: customers.csv, products.csv, orders.csv, order_items.csv, payments.csv")
