#!/usr/bin/env node
// NOVYDRES CHR-001 / local structural and provenance gate. Node.js >=18, stdlib only.
// Execute on a checkout BEFORE publishing a cycle and AFTER checkout/readback.
// GitHub ChatGPT connector cannot execute this automatically; direct tool checks
// of HEAD, Git blobs and transition status remain mandatory.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import process from 'node:process';

const REFS = ['live', 'history_index', 'episode', 'character', 'knowledge', 'threads'];
const HEX = /^[0-9a-f]{40}$/;
const CYCLE_DIR = 'novydres/chronicles/CHR-001/orchestration';
const FORMAT = /^CYCLE_V(\d{4})\.json$/;

function insist(condition, message) {
  if (!condition) throw new Error('ORCHESTRATION_BLOCK: ' + message);
}
export function gitBlobSha(content) {
  const bytes = Buffer.isBuffer(content) ? content : Buffer.from(content, 'utf8');
  const pre = Buffer.from('blob ' + bytes.length + '\0');
  return crypto.createHash('sha1').update(pre).update(bytes).digest('hex');
}
function safePath(root, ref) {
  insist(typeof ref === 'string' && ref.startsWith('novydres/'), 'invalid repo path');
  insist(!ref.includes('..') && !ref.includes('\\') && !path.isAbsolute(ref), 'unsafe path');
  const target = path.resolve(root, ref);
  insist(target.startsWith(path.resolve(root) + path.sep), 'path outside repository');
  return target;
}
function loadFile(root, repoPath) {
  return fs.readFileSync(safePath(root, repoPath));
}
function loadJson(root, repoPath) {
  return JSON.parse(loadFile(root, repoPath).toString('utf8'));
}
export function discoverLatest(root) {
  const dir = safePath(root, CYCLE_DIR);
  insist(fs.existsSync(dir), 'cycle directory missing');
  const nums = fs.readdirSync(dir).map(x => {
    const m = FORMAT.exec(x);
    return m ? Number(m[1]) : null;
  }).filter(x => x !== null).sort((a, b) => a - b);
  insist(nums.length >= 1, 'no cycle exists');
  insist(nums[0] === 1, 'cycle sequence must start at 0001');
  for (let i = 1; i < nums.length; i++) insist(nums[i] === nums[i - 1] + 1, 'missing cycle or duplicate sequence');
  return CYCLE_DIR + '/CYCLE_V' + String(nums[nums.length - 1]).padStart(4, '0') + '.json';
}
function verifyRef(root, ref, label) {
  insist(ref && typeof ref === 'object' && HEX.test(ref.blob_sha || ''), label + ': missing SHA');
  const got = gitBlobSha(loadFile(root, ref.path));
  insist(got === ref.blob_sha, label + ': blob SHA mismatch for ' + ref.path);
}
function validateFrame(c) {
  insist(c?.schema_id === 'NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V1', 'wrong schema');
  insist(c.chronicle_id === 'CHR-001', 'wrong chronicle');
  insist(Number.isInteger(c.sequence) && c.sequence >= 1 && c.sequence <= 9999, 'invalid sequence');
  insist(c.cycle_id === 'CHR001-CYCLE-' + String(c.sequence).padStart(4, '0'), 'cycle id/sequence mismatch');
  insist(HEX.test(c.source_head_sha || ''), 'missing source HEAD lease');
  insist(/^M[1-5]\.\d{2}$/.test(c.provocation_id || ''), 'wrong provocation');
  insist(/^novydres\/MANIFEST_V\d+\.json$/.test(c.manifest_path || ''), 'invalid manifest path');
  insist(c.checkpoint && c.refs && c.plan && c.review && c.blocking && c.guards, 'missing core fields');
  insist(typeof c.checkpoint.last_event_id === 'string', 'missing last event');
  insist(/^C\d{2}$/.test(c.checkpoint.last_closed_scene) && /^C\d{2}$/.test(c.checkpoint.next_scene), 'scene ids invalid');
  insist(c.checkpoint.pending_persistence === false, 'PENDING_PERSISTENCE cannot transfer');
  insist(c.checkpoint.next_scene_status === 'NOT_STARTED', 'new scene already started');
  const g = c.guards;
  insist(['no_story_delta_in_prep','no_xp_fv_delta_in_prep','g28_scene_only','frozen_unchanged','no_public_spoilers'].every(k => g[k] === true), 'governance flags');
  insist(['READY_FOR_DRAMATURGO','READY_FOR_NARRATOR','PROVOCATION_CLOSURE_PENDING','BLOCKED_CONFLICT'].includes(c.status), 'unrecognized state');
  if (c.status === 'READY_FOR_DRAMATURGO') {
    insist(c.next_role === 'DRAMATURGO', 'role wrong');
    insist(['BOOTSTRAP','SCENE_COMMITTED'].includes(c.transition), 'transition wrong');
    insist(c.plan.validity === 'STALE' && c.review.decision === 'NOT_REVIEWED', 'unreviewed scene must reenter dramaturgy');
    insist(c.blocking.code !== null, 'Dramaturgo readiness needs review reason');
  } else if (c.status === 'READY_FOR_NARRATOR') {
    insist(c.next_role === 'NARRADOR', 'role wrong');
    insist(['PLAN_REVALIDATED','PLAN_REVISED'].includes(c.transition), 'only Dramaturgo can release Narrador');
    insist(['VALIDATED','REVISED'].includes(c.plan.validity), 'not a valid plan');
    insist(c.plan.reviewed_against_event_id === c.checkpoint.last_event_id, 'plan not reviewed against latest event');
    insist(c.review.against_last_event_id === c.checkpoint.last_event_id, 'review event drift');
    insist(c.review.public_rationale && c.review.public_rationale.length >= 20, 'review lacks rationale');
    insist(c.blocking.code === null && c.blocking.reason === null, 'blocked cycle cannot release Narrador');
  } else if (c.status === 'PROVOCATION_CLOSURE_PENDING') {
    insist(c.next_role === 'NONE' && c.transition === 'CLOSURE_RECOMMENDED', 'closure cannot begin a scene');
    insist(c.review.decision === 'CLOSURE_RECOMMENDED', 'closure not reviewed');
  } else {
    insist(c.next_role === 'NONE' && c.transition === 'BLOCKED', 'blocked state cannot release Narrador');
  }
}
function validateTransition(c, previous) {
  if (c.sequence === 1) {
    insist(c.previous_cycle === null && previous === null, 'bootstrap predecessor invalid');
    insist(c.transition === 'BOOTSTRAP' && c.status === 'READY_FOR_DRAMATURGO', 'bootstrap must request Dramaturgo');
    return;
  }
  insist(previous !== null && c.previous_cycle && HEX.test(c.previous_cycle.blob_sha || ''), 'predecessor missing');
  insist(c.sequence === previous.sequence + 1, 'nonconsecutive cycle');
  insist(c.provocation_id === previous.provocation_id || previous.status === 'PROVOCATION_CLOSURE_PENDING', 'provocation drift');
  insist(c.checkpoint.pending_persistence === false, 'cannot transfer pending data');
  if (c.transition === 'SCENE_COMMITTED') {
    insist(previous.status === 'READY_FOR_NARRATOR', 'scene committed without Narrador authorization');
    insist(c.status === 'READY_FOR_DRAMATURGO', 'scene must return to Dramaturgo');
    insist(c.checkpoint.last_closed_scene === previous.checkpoint.next_scene, 'wrong scene closed');
    insist(Number(c.checkpoint.next_scene.slice(1)) === Number(previous.checkpoint.next_scene.slice(1)) + 1, 'next scene not incremented');
    insist(c.checkpoint.last_event_id !== previous.checkpoint.last_event_id, 'scene lacks new event');
    insist(c.refs.episode.blob_sha !== previous.refs.episode.blob_sha, 'scene did not change episode');
    insist(c.plan.dossier.blob_sha === previous.plan.dossier.blob_sha, 'Narrador altered a planned dossier');
  } else if (['PLAN_REVALIDATED','PLAN_REVISED','CLOSURE_RECOMMENDED'].includes(c.transition)) {
    insist(previous.status === 'READY_FOR_DRAMATURGO', 'Dramaturgo turn out of order');
    insist(c.checkpoint.last_event_id === previous.checkpoint.last_event_id, 'Dramaturgo cannot invent story events');
    insist(c.checkpoint.last_closed_scene === previous.checkpoint.last_closed_scene && c.checkpoint.next_scene === previous.checkpoint.next_scene, 'Dramaturgo cannot open/close scene');
    for (const k of REFS) insist(c.refs[k].blob_sha === previous.refs[k].blob_sha && c.refs[k].path === previous.refs[k].path, 'Dramaturgo changed narrative source: ' + k);
    insist(c.review.against_last_event_id === c.checkpoint.last_event_id, 'Dramaturgo review missing current scene');
    if (c.transition === 'PLAN_REVALIDATED') {
      insist(c.plan.dossier.blob_sha === previous.plan.dossier.blob_sha, 'revalidation modified dossier');
      insist(c.review.decision === 'REVALIDATED' && c.plan.validity === 'VALIDATED', 'revalidation state invalid');
    } else if (c.transition === 'PLAN_REVISED') {
      insist(c.plan.dossier.blob_sha !== previous.plan.dossier.blob_sha, 'revision must publish new dossier');
      insist(c.review.decision === 'REVISED' && c.plan.validity === 'REVISED', 'revision state invalid');
    }
  } else if (c.transition === 'BLOCKED') {
    insist(c.status === 'BLOCKED_CONFLICT' && c.next_role === 'NONE', 'BLOCKED cannot transfer');
  } else insist(false, 'illegal transition: ' + c.transition);
}
export function validateCycle(root, repoPath) {
  const fileName = path.posix.basename(repoPath);
  const match = FORMAT.exec(fileName);
  insist(match && repoPath === CYCLE_DIR + '/' + fileName, 'wrong cycle path');
  const c = loadJson(root, repoPath);
  validateFrame(c);
  insist(Number(match[1]) === c.sequence, 'filename does not match sequence');
  insist(fs.existsSync(safePath(root, c.manifest_path)), 'manifest missing');
  for (const name of REFS) verifyRef(root, c.refs[name], name);
  verifyRef(root, c.plan.dossier, 'dossier');
  if (c.plan.sidecar !== null && c.plan.sidecar !== undefined) verifyRef(root, c.plan.sidecar, 'sidecar');
  const live = loadJson(root, c.refs.live.path);
  insist(live.last_confirmed_event_id === c.checkpoint.last_event_id, 'LIVE last event mismatch');
  insist(live.stage?.embrace_occurred === c.checkpoint.embrace_occurred, 'Abraço drift');
  let prev = null;
  if (c.sequence > 1) {
    insist(c.previous_cycle && c.previous_cycle.path === CYCLE_DIR + '/CYCLE_V' + String(c.sequence - 1).padStart(4, '0') + '.json', 'wrong previous path');
    verifyRef(root, c.previous_cycle, 'previous_cycle');
    prev = loadJson(root, c.previous_cycle.path);
    validateFrame(prev);
  }
  validateTransition(c, prev);
  return { cycle_id:c.cycle_id, role:c.next_role, status:c.status, transition:c.transition, last_event_id:c.checkpoint.last_event_id };
}
if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(new URL(import.meta.url).pathname)) {
  try {
    const i = process.argv.indexOf('--root');
    const root = path.resolve(i >= 0 ? process.argv[i + 1] : process.cwd());
    const j = process.argv.indexOf('--cycle');
    const p = j >= 0 ? process.argv[j + 1] : discoverLatest(root);
    const result = validateCycle(root, p);
    console.log(JSON.stringify({ok:true,...result}));
  } catch (e) {
    console.error(String(e));
    process.exitCode = 1;
  }
}
