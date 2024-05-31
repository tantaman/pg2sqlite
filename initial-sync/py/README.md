# PostgreSQL to SQLite Schema Converter

This project provides a script to convert PostgreSQL table schemas to SQLite-compatible schemas using SQLAlchemy.

## Prerequisites

- Python 3.x
- PostgreSQL database

## Installation

1. Clone this repository:
    ```sh
    git clone https://your-repo-url/pg_to_sqlite.git
    cd pg_to_sqlite
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the script with the PostgreSQL connection string and the SQLite DB file name as arguments:
    ```sh
    python convert.py <postgres_connection_string> <sqlite_db_file>
    ```

    Example:
    ```sh
    python convert.py "postgresql://username:password@localhost/database_name" "sqlite_database.db"
    ```

2. The SQLite-compatible schema will be saved to `schema.sql`.

