def init_db():
    conn = get_connection()
    cur = conn.cursor()

    with open("schema.sql", "r", encoding="utf-8") as f:
        cur.execute(f.read())

    conn.commit()
    cur.close()
    conn.close()

    print("DB CREATED")