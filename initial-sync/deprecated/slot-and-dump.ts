// https://stackoverflow.com/questions/75852587/how-to-use-exported-snapshot-in-postgres-replication-slot

// 1. Sets up the replication slot
// 2. Dumps the database at the snapshot of the slot

/*
Once you got the snapshot name (like "00000004-000003B9-1") from the create replication slot result,
you begin another transaction on another connection, and the first statement in the transaction must be 
SET TRANSACTION SNAPSHOT <snapshot_name>, which you got from the above create_replication_slot command.

Note that the first connection must not be closed and no other commands can be executed before you start the snapshot consuming transaction on the second connection. Otherwise, the snapshot will be invalid anymore.
*/