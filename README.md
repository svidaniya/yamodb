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
from yamodb import YamoDB


# --------------------------
# YamoDB Setup
# --------------------------
YamoDB.secret = "mysecretkey"           # Set the secret key for encryption
YamoDB.delete_old_db = True             # Enable deletion of old databases on startup
YamoDB.connect()                        # Connect to the YamoDB instance

# --------------------------
# YAML Schema Definition
# --------------------------
yaml_db = """
    user:
      name:
        type: string         # Define 'name' as a string
        primary_key: true    # 'name' is the primary key for the user table
        not_null: true       # 'name' cannot be null
      password:
        type: encrypted      # 'password' will be encrypted
        not_null: true       # 'password' cannot be null
      money:
        type: float          # 'money' is a floating point number
      birthdate:
        type: date           # 'birthdate' is a date field

    book:
      title:
        type: string 
        primary_key: true    # 'title' is the primary key for the book table
      owner:
        reference: user.name  # 'owner' references the 'name' field in the 'user' table
        on_delete: cascade    # Options: cascade, set_null, restrict, no_action
"""

# --------------------------
# Generate Schema and Insert Data
# --------------------------
YamoDB.generate_from(yaml_db)  # Generate the database schema from the YAML definition

# Insert a new user into the 'user' table
YamoDB.insert("user", {
    'name': 'John Doe',
    'password': YamoDB.encrypt('password123'),  # Encrypt the user's password
    'money': YamoDB.number_placeholder(),         # Placeholder for 'money' (will be updated later)
    'birthdate': YamoDB.time().today().string()     # Use today's date for birthdate
})

# --------------------------
# Select and Decrypt User Data
# --------------------------
result_user = YamoDB.select("user").where({'name': 'John Doe'}).decrypt('password')
result_user.first().print()  # Print the first user result (shows 'John Doe' with decrypted password)

# --------------------------
# Insert Books Associated with the User
# --------------------------
YamoDB.insert("book", {'title': 'The Great Gatsby', 'owner': 'John Doe'})
YamoDB.insert("book", {'title': 'To Kill a Mockingbird', 'owner': 'John Doe'})

# --------------------------
# Query Books Owned by 'John Doe'
# --------------------------
result_books = YamoDB.select("book").where({'owner': 'John Doe'})
result_books.print()  # Print the list of books for 'John Doe'

# --------------------------
# Update the User's 'money' Field
# --------------------------
result_user.update({'money': 100.0}).print()  # Update 'money' for 'John Doe' to 100.0 and print the updated user

# --------------------------
# Count the Number of Books Owned by 'John Doe'
# --------------------------
book_count = result_books.count()
book_count.print()  # Print the count of books

# --------------------------
# Sort Books by Title in Descending Order
# --------------------------
sorted_books = result_books.order_by('title', desc=True)
sorted_books.print()  # Print books sorted by title in descending order

# --------------------------
# Show the First Book in the Result
# --------------------------
first_book = result_books.first()
first_book.print()  # Print the first book in the result set

# --------------------------
# Group Books by Owner
# --------------------------
grouped_books = result_books.group_by('owner')
grouped_books.print()  # Print the books grouped by owner

# --------------------------
# Limit the Results to Just 1 Book
# --------------------------
limited_books = result_books.limit(1)
limited_books.print()  # Print only the first book from the result set

# --------------------------
# Demonstrate a Simulated Update (Without Committing)
# --------------------------
# This update simulates the change in memory only (commit=False)
result_user.update({'money': 200.0}, commit=False).print()

# --------------------------
# Delete the User and Verify Cascading Deletion on Books
# --------------------------
YamoDB.select("user").where({'name': 'John Doe'}).delete()  # Delete 'John Doe' from the user table
YamoDB.select("book").where({'owner': 'John Doe'}).print()    # Should print an empty list due to cascading delete

# --------------------------
# Close the Database Connection
# --------------------------
YamoDB.close()  # Close the connection to YamoDB

```

### How This Example Works

* **Schema Definition:** `yaml_db` defines the database structure using YAML, including relationships (`book.owner` references `user.name`).
* **Data Insertion:** Adds a user with encrypted password and placeholder money. Inserts a book linked to the user.
* **Queries:** Demonstrates querying, decrypting sensitive data, and cascading deletions.
* **Cascading Deletion:** Deleting a user removes their associated books automatically due to the `on_delete: cascade` rule.
* **Encryption:** Passwords are securely encrypted using `YamoDB.encrypt()`.

YamoDB simplifies database operations while ensuring robust features like encryption and cascading deletions, making it ideal for lightweight applications.
