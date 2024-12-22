YamoDB
====

**YamoDB** is a powerful and lightweight library designed for data and database manipulation. It enables you to easily create and manage complex databases using YAML files, offering a simple yet efficient way to handle structured data. Whether you're working on small projects or need advanced data management capabilities, YamoDB provides an easy and straightforward approach to store, retrieve, and manipulate data without the need for heavyweight database systems.

---

🚀 Key Features
---------------

### 📦 Data Management with YAML

* Easily create and manage databases using YAML files.
* Supports complex database structures with relationships, constraints, and data types.
* Ideal for small to medium-sized projects where heavyweight databases are unnecessary.

### 🔍 Advanced Data Manipulation

* Perform queries like filtering, sorting, and modifying records with ease.
* Includes intuitive methods for data insertion, selection, updates, and deletion.

### 🔐 Built-in Encryption

* Protect sensitive data with native encryption methods like `encrypt()`.
* Example: `YamoDB.insert('user', {'password': YamoDB.encrypt('mypassword')})`.

### ⏳ Modern Date and Time Handling

* Effortless date and time manipulation.
* Example: `YamTimes.today().string()` to get the current date.

---

📖 Example Usage
----------------

```python
from yamodb import YamoDB, YamTimes

# Setting up YamoDB
YamoDB.secret = "mysecretkey"
YamoDB.delete_old_db = True
YamoDB.connect()

# YAML schema definition
yaml_db = """
user:
    name:
        type: string
        primary_key: true
        not_null : true
    password:
        type: encrypted
        not_null: true
    money:
        type: float
    birthdate:
        type: date

book:
    title:
        type: string
        primary_key: true
    owner:
        reference: user.name
        on_delete: cascade
"""

# Generate schema and insert data
YamoDB.generate_from(yaml_db)
YamoDB.insert("user", {
    'name': 'John Doe',
    'password': YamoDB.encrypt('password123'),
    'money': YamoDB.number_placeholder(),
    'birthdate': YamTimes.today().string()
})

# Select and decrypt user data
YamoDB.select("user").where({'name': 'John Doe'}).decrypt('password').first().print()

# Insert a book associated with the user
YamoDB.insert("book", {'title': 'The Great Gatsby', 'owner': 'John Doe'})

# Retrieve books owned by the user
YamoDB.select("book").where({'owner': 'John Doe'}).print()

# Delete the user and check cascading deletion on books
YamoDB.select("user").where({'name': 'John Doe'}).delete()
YamoDB.select("book").where({'owner': 'John Doe'}).print()

# Close the connection
YamoDB.close()
```

### How This Example Works

* **Schema Definition:** `yaml_db` defines the database structure using YAML, including relationships (`book.owner` references `user.name`).
* **Data Insertion:** Adds a user with encrypted password and placeholder money. Inserts a book linked to the user.
* **Queries:** Demonstrates querying, decrypting sensitive data, and cascading deletions.
* **Cascading Deletion:** Deleting a user removes their associated books automatically due to the `on_delete: cascade` rule.
* **Encryption:** Passwords are securely encrypted using `YamoDB.encrypt()`.

YamoDB simplifies database operations while ensuring robust features like encryption and cascading deletions, making it ideal for lightweight applications.
