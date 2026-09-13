import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

const ROOT_DIR = process.cwd();

async function rollback() {
  console.log('====================================================');
  console.log('  INSTANT CHỐT ROLLBACK ENGINE (v2.0)               ');
  console.log('====================================================\n');

  // 1. Get available tags
  let tags = [];
  try {
    const raw = execSync('git tag -l "checkpoint-*" --sort=-creatordate', { cwd: ROOT_DIR }).toString().trim();
    tags = raw ? raw.split('\n').map(t => t.trim()).filter(Boolean) : [];
  } catch (e) {
    console.error('[ERROR] Could not query git tags:', e.message);
  }

  if (tags.length === 0) {
    console.log('[WARN] No checkpoint tags found.');
    process.exit(1);
  }

  const targetTag = process.argv[2] || tags[0];
  console.log(`Target Rollback Destination: [${targetTag}]`);
  console.log(`Available Checkpoints: ${tags.join(', ')}\n`);

  console.log(`--- Rolling back workspace to [${targetTag}] ---`);
  try {
    execSync(`git checkout "${targetTag}" -- .`, { stdio: 'inherit', cwd: ROOT_DIR });
    console.log('\n[PASS] All source files cleanly restored from checkpoint!');
  } catch (err) {
    console.error('\n[ERROR] Rollback failed:', err.message);
    process.exit(1);
  }
}

rollback().catch(console.error);
