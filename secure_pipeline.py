
import sqlite3
import os

os.makedirs("data", exist_ok=True)

conn = sqlite3.connect("data/sales.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone TEXT,
    sales_amount REAL
)
""")

customers = [
    (101, "Arun", "arun@gmail.com", "9876543210", 5000),
    (102, "Priya", "priya@gmail.com", "9876543211", 7500),
    (103, "Kumar", "kumar@gmail.com", "9876543212", 6200),
    (104, "Divya", "divya@gmail.com", "9876543213", 8900),
    (105, "Rahul", "rahul@gmail.com", "9876543214", 4500)
]

cursor.executemany("""
INSERT OR REPLACE INTO customers
VALUES (?, ?, ?, ?, ?)
""", customers)

conn.commit()


# Secure parameterized query
def secure_query(customer_id):
    query = """
    SELECT customer_id, name, email, phone, sales_amount
    FROM customers
    WHERE customer_id = ?
    """
    cursor.execute(query, (customer_id,))
    return cursor.fetchall()


# Mask PII data
def mask_data(records):
    masked_records = []

    for row in records:
        customer_id, name, email, phone, amount = row

        masked_name = name[0] + "****"
        masked_email = email[0] + "****@" + email.split("@")[1]
        masked_phone = "XXXXXX" + phone[-4:]

        masked_records.append((
            customer_id,
            masked_name,
            masked_email,
            masked_phone,
            amount
        ))

    return masked_records


print("\nORIGINAL CUSTOMER DATA")
original_data = secure_query(101)

for record in original_data:
    print(record)

print("\nMASKED CUSTOMER DATA")
masked_data = mask_data(original_data)

for record in masked_data:
    print(record)

print("\nSQL INJECTION TEST")
malicious_input = "' OR '1'='1"
result = secure_query(malicious_input)

print("Malicious input:", malicious_input)
print("Records returned:", len(result))

if len(result) == 0:
    print("SQL Injection prevented successfully!")

conn.close()
