import os
import sys
import psycopg2

def export_tables_to_csv(postgres_conn_str, output_dir):
    # Connect to PostgreSQL
    conn = psycopg2.connect(postgres_conn_str)
    cursor = conn.cursor()

    conn.autocommit = False
    cursor.execute("SELECT pg_current_wal_lsn();")
    wal_lsn = cursor.fetchone()[0]
    print(f"Current WAL LSN: {wal_lsn}")

    # Fetch all table names
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)
    tables = cursor.fetchall()

    # Create output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    # Export each table to a CSV file
    for table in tables:
        table_name = table[0]
        print(f"Exporting {table_name}...")
        output_file = os.path.join(output_dir, f"{table_name}.csv")
        with open(output_file, 'w') as f:
            cursor.copy_expert(f'COPY "{table_name}" TO STDOUT WITH CSV HEADER', f)
        print(f"{table_name} exported to {output_file}")

    conn.commit()
    cursor.close()
    conn.close()
    print("All tables have been exported.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python export_to_csv.py <postgres_connection_string> <output_directory>")
        sys.exit(1)

    postgres_conn_str = sys.argv[1]
    output_dir = sys.argv[2]

    export_tables_to_csv(postgres_conn_str, output_dir)
