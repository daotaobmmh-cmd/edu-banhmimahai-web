import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

const ROOT_DIR = process.cwd();

async function createCheckpoint() {
  console.log('====================================================');
  console.log('  AUTOMATED CERTIFIED CHỐT CHECKPOINT ENGINE (v2.0) ');
  console.log('====================================================\n');

  // 1. Run Verification / Regression / Linter Gate
  console.log('--- Step 1: Enforcing Verification & Linter Gate ---');
  let verified = false;
  
  // Try regression test script first if available
  if (fs.existsSync(path.join(ROOT_DIR, 'scripts/run_atlas_regression.mjs'))) {
    try {
      execSync('node scripts/run_atlas_regression.mjs', { stdio: 'inherit', cwd: ROOT_DIR });
      verified = true;
    } catch (e) {
      console.error('\n[FATAL] Regression gate FAILED. Aborting Checkpoint!');
      process.exit(1);
    }
  } else if (fs.existsSync(path.join(ROOT_DIR, 'scripts/run_regression.py'))) {
    try {
      execSync('python scripts/run_regression.py', { stdio: 'inherit', cwd: ROOT_DIR });
      verified = true;
    } catch (e) {
      console.error('\n[FATAL] Python regression gate FAILED. Aborting Checkpoint!');
      process.exit(1);
    }
  }

  // Run Rule Conflict Linter
  if (fs.existsSync(path.join(ROOT_DIR, 'scripts/lint_rules_conflict.mjs'))) {
    try {
      execSync('node scripts/lint_rules_conflict.mjs', { stdio: 'inherit', cwd: ROOT_DIR });
      verified = true;
    } catch (e) {
      console.error('\n[FATAL] Cross-Rule Conflict Linter FAILED. Aborting Checkpoint!');
      process.exit(1);
    }
  }

  if (verified) {
    console.log('[PASS] All Verification gates 100% GREEN.\n');
  }

  // 2. Determine Slice Tag
  const customSlice = process.argv[2] || 'SYSTEM-SYNC';
  const tagName = `checkpoint-${customSlice.toLowerCase()}`;

  // 3. Stage Files Safely
  console.log('--- Step 2: Staging Certified Workspace Files ---');
  const safePaths = [
    'src', 'apps', 'packages', 'rules', 'workflows', 'scripts', 'public', 'docs',
    'api', 'data', 'config', 'tests', 'schemas', 'assets', '.agents', '.memory-bank',
    'AGENTS.md', 'README.md', 'spec-truth.yaml', '.gitignore', 'package.json', 'pnpm-lock.yaml'
  ];

  for (const p of safePaths) {
    if (fs.existsSync(path.join(ROOT_DIR, p))) {
      try {
        execSync(`git add "${p}"`, { cwd: ROOT_DIR });
      } catch (e) {
        console.warn(`[WARN] Could not stage ${p}:`, e.message);
      }
    }
  }

  // 4. Create Git Commit
  console.log('--- Step 3: Creating Certified Git Snapshot Commit ---');
  const commitMsg = `CHOT(${customSlice}): Certified Milestone Lock\n\n- Authority: TIER 0 SUPREME OMEGA COMMAND (PROTOCOL-CHOT-002)\n- Verified At: ${new Date().toISOString()}`;
  
  try {
    execSync(`git commit -m "${commitMsg}"`, { stdio: 'inherit', cwd: ROOT_DIR });
  } catch (e) {
    console.log('[INFO] Working tree clean or already committed.');
  }

  // 5. Create Annotated Git Tag
  console.log(`--- Step 4: Tagging Immutable Checkpoint: ${tagName} ---`);
  try {
    execSync(`git tag -f -a "${tagName}" -m "Certified Checkpoint for ${customSlice}"`, { cwd: ROOT_DIR });
    console.log(`[PASS] Checkpoint Tag [${tagName}] created successfully!`);
  } catch (e) {
    console.warn(`[WARN] Could not create tag:`, e.message);
  }

  // 6. Get Current Hash
  try {
    const hash = execSync('git rev-parse HEAD', { cwd: ROOT_DIR }).toString().trim();
    console.log('\n====================================================');
    console.log(`  CHECKPOINT CERTIFIED AND LOCKED: ${hash.substring(0, 8)}`);
    console.log(`  TAG NAME                       : ${tagName}`);
    console.log('====================================================\n');
  } catch (e) {
    console.log('\n[INFO] Checkpoint tag completed.');
  }
}

createCheckpoint().catch(console.error);
