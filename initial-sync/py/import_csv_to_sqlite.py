import os
import sys
import subprocess

def import_csv_to_sqlite(csv_directory, sqlite_db_file):
    # List all CSV files in the directory
    csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]

    # Iterate over each CSV file and import it into SQLite
    for csv_file in csv_files:
        table_name = os.path.splitext(csv_file)[0]
        csv_file_path = os.path.join(csv_directory, csv_file)
        
        # Construct the SQLite import command
        sqlite_command = f'sqlite3 {sqlite_db_file} "PRAGMA foreign_keys = 0" ".mode csv" ".import {csv_file_path} {table_name}"'
        
        try:
            # Run the SQLite import command
            subprocess.run(sqlite_command, shell=True, check=True)
            print(f"Imported {csv_file} into {table_name} table.")
        except subprocess.CalledProcessError as e:
            print(f"Error importing {csv_file}: {e}")

    print("All CSV files have been imported.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python import_csv_to_sqlite.py <csv_directory> <sqlite_db_file>")
        sys.exit(1)

    csv_directory = sys.argv[1]
    sqlite_db_file = sys.argv[2]

    import_csv_to_sqlite(csv_directory, sqlite_db_file)
