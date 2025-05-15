Here's a complete `seed.py` script that sets up a MySQL database named **`ALX_prodev`**, creates a **`user_data`** table, and populates it using a **`user_data.csv`** file. This version uses `mysql-connector-python` and includes all the required function prototypes.

---

### **Requirements:**

1. MySQL running locally or remotely.
2. Python installed with:

   ```bash
   pip install mysql-connector-python pandas
   ```
3. A CSV file named `user_data.csv` in the same directory.

---

### \*\*`seed.py` Script:

```python
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import uuid

def connect_db():
    """Connect to MySQL server (not to a specific database)."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password_here'
        )
        print("Connected to MySQL server")
        return connection
    except mysql.connector.Error as err:
        print(f"Connection error: {err}")
        exit(1)

def create_database(connection):
    """Create ALX_prodev database if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev is ready")
    except mysql.connector.Error as err:
        print(f"Failed to create database: {err}")
        exit(1)
    cursor.close()

def connect_to_prodev():
    """Connect directly to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password_here',
            database='ALX_prodev'
        )
        print("Connected to ALX_prodev database")
        return connection
    except mysql.connector.Error as err:
        print(f"Connection error: {err}")
        exit(1)

def create_table(connection):
    """Create user_data table with appropriate schema."""
    cursor = connection.cursor()
    create_stmt = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(3,0) NOT NULL,
        INDEX(user_id)
    )
    """
    try:
        cursor.execute(create_stmt)
        print("user_data table is ready")
    except mysql.connector.Error as err:
        print(f"Failed to create table: {err}")
    finally:
        cursor.close()

def insert_data(connection, data):
    """Insert data into user_data table, ignoring duplicates."""
    cursor = connection.cursor()
    insert_stmt = """
    INSERT INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE name = VALUES(name), email = VALUES(email), age = VALUES(age)
    """
    for _, row in data.iterrows():
        uid = str(uuid.uuid4())
        values = (uid, row['name'], row['email'], row['age'])
        try:
            cursor.execute(insert_stmt, values)
        except mysql.connector.Error as err:
            print(f"Failed to insert: {err}")
    connection.commit()
    cursor.close()
    print("Data inserted successfully")

if __name__ == '__main__':
    db_conn = connect_db()
    create_database(db_conn)
    db_conn.close()

    prodev_conn = connect_to_prodev()
    create_table(prodev_conn)

    # Load CSV data
    try:
        data = pd.read_csv("user_data.csv")
        insert_data(prodev_conn, data)
    except FileNotFoundError:
        print("user_data.csv not found")
    finally:
        prodev_conn.close()
```

---



---

