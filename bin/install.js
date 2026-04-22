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
const customInstallDir = installDirIdx >= 0 ? path.resolve(args[installDirIdx + 1]) : null;

const REPO_ROOT = path.join(__dirname, '..');
const SKIP_DIRS = new Set(['bin', 'node_modules', '.git']);

const KNOWN_AGENTS = [
  { name: 'Claude Code',        dir: path.join(os.homedir(), '.claude', 'skills') },
  { name: 'Codex',              dir: path.join(os.homedir(), '.codex', 'skills') },
  { name: 'Hermes',             dir: path.join(os.homedir(), '.hermes', 'hermes-agent', 'skills') },
  { name: 'Generic (~/.agents)',dir: path.join(os.homedir(), '.agents', 'skills') },
];

function discoverSkills() {
  return fs.readdirSync(REPO_ROOT, { withFileTypes: true })
    .filter(e => e.isDirectory() && !e.name.startsWith('.') && !SKIP_DIRS.has(e.name))
    .filter(e => fs.existsSync(path.join(REPO_ROOT, e.name, 'SKILL.md')))
    .map(e => e.name);
}

function detectAgents() {
  return KNOWN_AGENTS.filter(a => fs.existsSync(path.dirname(a.dir)));
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

function installSkill(name, skillsDir) {
  copyDir(path.join(REPO_ROOT, name), path.join(skillsDir, name));
  console.log(`  ✅ ${name} → ${path.join(skillsDir, name)}`);
}

function ask(rl, question) {
  return new Promise(resolve => rl.question(question, answer => resolve(answer.trim())));
}

async function selectItems(rl, label, items, allowAll = true) {
  console.log(`\n${label}\n`);
  items.forEach((s, i) => console.log(`  ${i + 1}. ${s.name || s}`));
  if (allowAll) console.log(`  ${items.length + 1}. All\n`);

  const answer = await ask(rl, 'Select (comma-separated numbers, or Enter for all): ');
  if (!answer) return items;
  const nums = answer.split(',').map(s => parseInt(s.trim())).filter(n => !isNaN(n));
  if (allowAll && nums.includes(items.length + 1)) return items;
  return nums.filter(n => n >= 1 && n <= items.length).map(n => items[n - 1]);
}

async function main() {
  const skills = discoverSkills();

  if (listOnly) {
    console.log('Available skills:');
    skills.forEach(s => console.log(`  - ${s}`));
    return;
  }

  console.log('\n🎯 ezio-skills installer');

  // Resolve target agent directories
  let targetDirs;
  if (customInstallDir) {
    targetDirs = [customInstallDir];
    console.log(`Install directory: ${customInstallDir}`);
  } else {
    const detected = detectAgents();
    if (detected.length === 0) {
      // No known agents found — ask for custom path
      const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
      const custom = await ask(rl, '\nNo known agent detected. Enter install directory: ');
      rl.close();
      targetDirs = [path.resolve(custom)];
    } else if (detected.length === 1 || yes) {
      targetDirs = detected.map(a => a.dir);
      console.log(`Detected agents: ${detected.map(a => a.name).join(', ')}`);
    } else {
      const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
      console.log('\nDetected agents:');
      const chosen = await selectItems(rl, 'Which agent(s) to install to?', detected);
      rl.close();
      targetDirs = chosen.map(a => a.dir);
    }
  }

  // Select skills
  let selected;
  if (yes) {
    selected = skills;
  } else {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    const skillItems = skills.map(s => ({ name: s }));
    const chosen = await selectItems(rl, 'Available skills:', skillItems);
    rl.close();
    selected = chosen.map(s => s.name || s);
  }

  if (selected.length === 0) {
    console.log('No skills selected.');
    return;
  }

  for (const dir of targetDirs) {
    fs.mkdirSync(dir, { recursive: true });
    console.log(`\n📂 Installing to ${dir}`);
    for (const skill of selected) installSkill(skill, dir);
  }

  const agentNote = targetDirs.length > 1 ? `${targetDirs.length} agents` : '1 agent';
  console.log(`\n✨ Done! ${selected.length} skill(s) installed to ${agentNote}.`);
  console.log('Restart your agent to activate.\n');
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
