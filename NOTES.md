1. Connect to PG
2. Begin a TX
3. Create a snapshot name: `SELECT pg_export_snapshot();`
4. Get the LSN `SELECT pg_current_wal_lsn();`
5. PGDump it `pg_dump --snapshot=_snapshotname`
6. Commit the TX
7. Import it https://github.com/scratchmex/pgdump2sqlite?tab=readme-ov-file
8. Start logical replication @ the LSN

---

Could do all the `copies` in a `TX` and report the `SNAPSHOT` name as well as `WAL LSN` so we can resume replication after importing the export.