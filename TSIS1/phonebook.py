from connect import get_connection
import json


# =========================
# INIT DB
# =========================
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS groups (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        email VARCHAR(100),
        birthday DATE,
        group_id INT REFERENCES groups(id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phones (
        id SERIAL PRIMARY KEY,
        contact_id INT REFERENCES contacts(id) ON DELETE CASCADE,
        phone VARCHAR(20),
        type VARCHAR(10)
    );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("DB READY")


# =========================
# ADD CONTACT
# =========================
def add_contact():
    fn = input("First name: ")
    ln = input("Last name: ")
    email = input("Email: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO contacts(first_name, last_name, email)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (fn, ln, email))

    cid = cur.fetchone()[0]

    phone = input("Phone: ")
    cur.execute("""
        INSERT INTO phones(contact_id, phone, type)
        VALUES (%s, %s, %s)
    """, (cid, phone, "mobile"))

    conn.commit()
    cur.close()
    conn.close()

    print("ADDED")


# =========================
# SHOW ALL CONTACTS
# =========================
def show_contacts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.first_name, c.last_name, c.email, p.phone
        FROM contacts c
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY c.id
    """)

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


# =========================
# SEARCH EMAIL
# =========================
def search_email():
    q = input("Email: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM contacts
        WHERE email ILIKE %s
    """, (f"%{q}%",))

    print(cur.fetchall())

    cur.close()
    conn.close()


# =========================
# FILTER BY GROUP
# =========================
def filter_group():
    g = input("Group: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.*
        FROM contacts c
        JOIN groups g2 ON c.group_id = g2.id
        WHERE g2.name = %s
    """, (g,))

    print(cur.fetchall())

    cur.close()
    conn.close()


# =========================
# SORT CONTACTS
# =========================
def sort_contacts():
    print("1 name 2 email 3 id")
    c = input("> ")

    order = {
        "1": "first_name",
        "2": "email",
        "3": "id"
    }.get(c, "id")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM contacts ORDER BY {order}")
    print(cur.fetchall())

    cur.close()
    conn.close()


# =========================
# PAGINATION
# =========================
def pagination():
    page = int(input("page: "))
    size = 5
    offset = (page - 1) * size

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM contacts
        LIMIT %s OFFSET %s
    """, (size, offset))

    print(cur.fetchall())

    cur.close()
    conn.close()


# =========================
# EXPORT JSON
# =========================
def export_json():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts")
    data = cur.fetchall()

    with open("export.json", "w", encoding="utf-8") as f:
        json.dump(data, f, default=str)

    print("EXPORTED")


# =========================
# IMPORT JSON
# =========================
def import_json():
    with open("export.json", encoding="utf-8") as f:
        data = json.load(f)

    conn = get_connection()
    cur = conn.cursor()

    for d in data:
        cur.execute("""
            INSERT INTO contacts(first_name, last_name, email)
            VALUES (%s, %s, %s)
        """, (d[1], d[2], d[3]))

    conn.commit()
    print("IMPORTED")


# =========================
# PROCEDURE CALLS
# =========================
def add_phone():
    fn = input("First name: ")
    ln = input("Last name: ")
    ph = input("Phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s,%s,%s,%s)",
                (fn, ln, ph, "mobile"))

    conn.commit()


def move_group():
    fn = input("First name: ")
    ln = input("Last name: ")
    g = input("Group: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s,%s,%s)",
                (fn, ln, g))

    conn.commit()


# =========================
# FUNCTION SEARCH
# =========================
def search_func():
    q = input("Search: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (q,))
    print(cur.fetchall())


# =========================
# MENU
# =========================
def menu():
    while True:
        print("""
1 init
2 add
3 show
4 email search
5 group filter
6 sort
7 pagination
8 export
9 import
10 add phone
11 move group
12 search func
0 exit
""")

        c = input("> ")

        if c == "1": init_db()
        elif c == "2": add_contact()
        elif c == "3": show_contacts()
        elif c == "4": search_email()
        elif c == "5": filter_group()
        elif c == "6": sort_contacts()
        elif c == "7": pagination()
        elif c == "8": export_json()
        elif c == "9": import_json()
        elif c == "10": add_phone()
        elif c == "11": move_group()
        elif c == "12": search_func()
        elif c == "0":
            break


menu()