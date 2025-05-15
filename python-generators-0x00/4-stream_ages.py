Here's how you can implement the `stream_user_ages()` generator to yield user ages **one by one** from a MySQL database, and calculate the **average age** without loading the entire dataset into memory:

---

### **Requirements Met:**

* Generator: `stream_user_ages()` 
* No SQL `AVG()` 
* Use no more than two loops 
* Optimized for large datasets

---

### **Python Script (`average_age.py`)**

```python
import mysql.connector

def connect_to_prodev():
    """Connect to ALX_prodev database."""
    return mysql.connector.connect(
        host="localhost",
        user="your_mysql_username",
        password="your_mysql_password",
        database="ALX_prodev"
    )

def stream_user_ages(connection):
    """Generator that yields ages from the user_data table."""
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield age
    cursor.close()

def calculate_average_age():
    """Calculate the average age using the generator."""
    connection = connect_to_prodev()
    total_age = 0
    count = 0

    for age in stream_user_ages(connection):
        total_age += age
        count += 1

    connection.close()

    if count == 0:
        print("No users found.")
    else:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")

if __name__ == "__main__":
    calculate_average_age()
```

---

### Sample Output:

```
Average age of users: 54.67
```
---
