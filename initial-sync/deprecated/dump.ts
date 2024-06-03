import {exec} from 'child_process';
import pg from 'pg';
const {Client} = pg;

// Define the connection details
const connectionString = process.env.UPSTREAM_URI!;
const outputFile = 'dump.sql';
const scriptPath = './run-dump.sh';

// Create a PostgreSQL client
const client = new Client({
  connectionString: connectionString,
});

async function runDump() {
  try {
    await client.connect();
    await client.query('BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;');
    
    // Export the snapshot
    const res = await client.query('SELECT pg_export_snapshot()');
    const snapshotId = res.rows[0].pg_export_snapshot;
    console.log('SNAPSHOT ID: ', snapshotId);

    let resolve: () => void;
    let reject: () => void;
    const execDone = new Promise<void>((res, rej) => {
      resolve = res;
      reject = rej;
    });
    console.log('RUNNING DUMP');
    exec(`${scriptPath} "${connectionString}" "${snapshotId}" "${outputFile}"`, (error, stdout, stderr) => {
      if (error) {
        reject();
        console.error(`Error: ${error.message}`);
        return;
      }
      if (stderr) {
        reject();
        console.error(`stderr: ${stderr}`);
        return;
      }
      resolve();
      console.log(`stdout: ${stdout}`);
    });
    await execDone;

    const walRes = await client.query('SELECT pg_current_wal_lsn()');
    console.log('WAL NAME: ', walRes.rows[0].pg_current_wal_lsn);
    await client.query('COMMIT');
  } catch (err: any) {
    console.error(`Error: ${err.message}`);
    await client.query('ROLLBACK');
  } finally {
    await client.end();
  }
}

runDump();