import psycopg2

conn = psycopg2.connect(
    host="135.225.108.173",
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

def select_from_table(table_name):
  cursor.execute("SELECT * FROM FRUITS")
  rows = cursor.fetchall()
  return rows


  
# Example query
table_name = 'FRUITS'
items = ['Apple']
# insert_into_table(table_name, items)
rows = select_from_table(table_name)
print(rows)

cursor.close()
conn.close()