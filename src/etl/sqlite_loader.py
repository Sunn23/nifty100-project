import sqlite3

def load_to_sqlite(tables, db_path):

    conn = sqlite3.connect(db_path)

    for table_name, df in tables.items():
        df.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False
        )

        print(f"Loaded {table_name}")

    conn.close()

    print(f"\nDatabase created: {db_path}")