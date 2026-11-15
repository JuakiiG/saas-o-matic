import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

// The database of a run lives in a folder of its own, outside `backend/data/`, which is the
// local database of whoever develops (CLAUDE.md, rule 8). The folder is created when the run
// starts and deleted when it ends, whatever the result.

const FOLDER_VARIABLE = 'SAAS_O_MATIC_E2E_FOLDER';
const FOLDER_PREFIX = 'saas-o-matic-e2e-';
// On Windows the file of the database can stay locked for a moment after the backend is killed.
const REMOVAL = { recursive: true, force: true, maxRetries: 10, retryDelay: 200 } as const;

function removeFolder(folder: string): void {
  try {
    rmSync(folder, REMOVAL);
  } catch (error) {
    // Not swallowed: a folder left behind must be seen, and the run must not end as passed.
    console.error(`The temporary folder ${folder} could not be deleted:`, error);
    process.exitCode = 1;
  }
}

/**
 * The folder of this run. Playwright loads its configuration in the process that runs the tests
 * and again in each worker: only the first one creates the folder, and deletes it when it exits,
 * after Playwright has stopped the servers; the workers find its path in the environment.
 */
export function temporaryFolder(): string {
  const inherited = process.env[FOLDER_VARIABLE];
  if (inherited !== undefined && inherited !== '') {
    return inherited;
  }
  const folder = mkdtempSync(join(tmpdir(), FOLDER_PREFIX));
  process.env[FOLDER_VARIABLE] = folder;
  process.on('exit', () => removeFolder(folder));
  return folder;
}
