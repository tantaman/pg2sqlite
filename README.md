# PG to SQLite

After doing a bunch of research on the topic, I didn't find any satisfactory approaches.

Other approaches:

1. https://github.com/caiiiycuk/postgresql-to-sqlite
2. https://github.com/scratchmex/pgdump2sqlite
3. https://stackoverflow.com/questions/6148421/how-to-convert-a-postgres-database-to-sqlite/69293251#69293251

All these involve doing hacky tricks to fix up the `pgdump` output _and_ they're slow. Admittedly this could be faster too but it is fast enough for me at the moment. Currently ~18 seconds to convert a 1GB DB over 3 million rows.

SQLite has a `.import` command and Postgres has a `copy` command. We can use both in conjunction to eliminate any need to post-process the data.

These scripts:

1. Use `copy` on PG to create CSVs of each table
2. Use `.import` on SQLite to import those CSVs

with no extra data cleaning steps.

A script is included to convert Postgres schemas to SQLite compatible schemas using SQLAlchemy, a well maintained project that speaks many dialects of SQL. Although this step is not strictly required as SQLite will happily create default schemas during the `.import` step.

After importing these dumps into SQLite you can then replicate from PG to SQLite as we capture `snapshot name` and `WAL LSN` of the export.

Usage:

There's three scripts (under initial-sync/py) meant to be used in turn.

1. convert-schema.py <postgres_connection_string> <out.sql>
   1. After this step, apply `out.sql` to your sqlite db
2. export_to_csv.py <postgres_connection_string> <csv_directory>
   1. This will report `WAL LSN` if you intend to sync with logical replication after initial import.
3. import_csv_to_sqlite.py <csv_directory> <sqlite_db_file_name>