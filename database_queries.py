import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="app_database",
    user="katypap",
    password="katypap",
    port="5432"
)

cursor = conn.cursor()


def insert_into_table(table_name, items):
    for item in items:
        cursor.execute(f"""
          INSERT INTO {table_name} VALUES ('{item}');
        """)
    conn.commit()

# Example query
cursor.execute("SELECT * FROM FRUITS")
rows = cursor.fetchall()
print(rows)

cursor.close()
conn.close()