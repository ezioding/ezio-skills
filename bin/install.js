#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const os = require('os');

const args = process.argv.slice(2);
const force = args.includes('--force');
const listOnly = args.includes('--list');
const yes = args.includes('-y') || args.includes('--yes');

const installDirIdx = args.findIndex(a => a === '--install-dir');
const baseDir = installDirIdx >= 0
  ? path.resolve(args[installDirIdx + 1])
  : path.join(os.homedir(), '.claude');
const skillsDir = path.join(baseDir, 'skills');

const REPO_ROOT = path.join(__dirname, '..');
const SKIP_DIRS = new Set(['bin', 'node_modules', '.git']);

function discoverSkills() {
  return fs.readdirSync(REPO_ROOT, { withFileTypes: true })
    .filter(e => e.isDirectory() && !e.name.startsWith('.') && !SKIP_DIRS.has(e.name))
    .filter(e => fs.existsSync(path.join(REPO_ROOT, e.name, 'SKILL.md')))
    .map(e => e.name);
}

function copyDir(src, dst) {
  fs.mkdirSync(dst, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const dstPath = path.join(dst, entry.name);
    if (entry.isDirectory()) {
      copyDir(srcPath, dstPath);
    } else {
      if (!force && fs.existsSync(dstPath)) {
        console.log(`  ⏭  ${entry.name} already exists (use --force to overwrite)`);
        continue;
      }
      fs.copyFileSync(srcPath, dstPath);
    }
  }
}

function installSkill(name) {
  console.log(`\n📦 Installing ${name}...`);
  copyDir(path.join(REPO_ROOT, name), path.join(skillsDir, name));
  console.log(`✅ ${name} → ${path.join(skillsDir, name)}`);
}

async function selectSkills(skills) {
  console.log('\nAvailable skills:\n');
  skills.forEach((s, i) => console.log(`  ${i + 1}. ${s}`));
  console.log(`  ${skills.length + 1}. All\n`);

  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(resolve => {
    rl.question('Select (comma-separated numbers, or Enter for all): ', answer => {
      rl.close();
      const input = answer.trim();
      if (!input) return resolve(skills);
      const nums = input.split(',').map(s => parseInt(s.trim())).filter(n => !isNaN(n));
      if (nums.includes(skills.length + 1)) return resolve(skills);
      resolve(nums.filter(n => n >= 1 && n <= skills.length).map(n => skills[n - 1]));
    });
  });
}

async function main() {
  const skills = discoverSkills();

  if (listOnly) {
    console.log('Available skills:');
    skills.forEach(s => console.log(`  - ${s}`));
    return;
  }

  console.log(`\n🎯 ezio-skills installer`);
  console.log(`Install directory: ${skillsDir}`);

  const selected = yes ? skills : await selectSkills(skills);

  if (selected.length === 0) {
    console.log('No skills selected.');
    return;
  }

  fs.mkdirSync(skillsDir, { recursive: true });
  for (const skill of selected) installSkill(skill);

  console.log(`\n✨ Done! ${selected.length} skill(s) installed.`);
  console.log('Restart Claude Code to activate.\n');
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
