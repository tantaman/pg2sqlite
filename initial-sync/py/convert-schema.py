import sys
from sqlalchemy import create_engine, MetaData
from sqlalchemy.schema import CreateTable
from sqlalchemy.pool import StaticPool

def convert_schemas(postgres_conn_str, sqlite_schema_file):
    # Connect to PostgreSQL
    postgres_engine = create_engine(postgres_conn_str)
    metadata = MetaData()
    metadata.reflect(bind=postgres_engine)

    # Connect to SQLite
    sqlite_engine = create_engine(f'sqlite://', poolclass=StaticPool)

    # Generate and print SQLite-compatible CREATE TABLE statements
    with open(sqlite_schema_file, 'w') as f:
        for table in metadata.tables.values():
            sqlite_table = CreateTable(table).compile(sqlite_engine)
            f.write(str(sqlite_table).strip() + ';\n')

    print(f'Schema has been converted and saved to {sqlite_schema_file}')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert.py <postgres_connection_string> <sqlite_schema_file>")
        sys.exit(1)

    postgres_conn_str = sys.argv[1]
    sqlite_db_file = sys.argv[2]

    convert_schemas(postgres_conn_str, sqlite_db_file)
