// ADR-001 C01 — candidate-only V01–V04. No runtime or narration imports.
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { resolve, relative, dirname, join, sep, posix } from 'node:path';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const S = 'novydres/sistema/arquitetura/fase-a/schemas/';
const EPISTEMIC = new Set(['CONFIRMED', 'NPC_CLAIM', 'GM_PREPARED', 'CONDITIONAL', 'UNKNOWN']);
const VISIBILITY = new Set(['PLAYER_SAFE', 'PC_KNOWN', 'NPC_BELIEF', 'GM_HIDDEN', 'SYSTEM_AUDIT']);
const OWNERS = ['novydres/cenario/', 'novydres/personagens/', 'novydres/cronicas/', 'novydres/sistema/regras/'];
const norm = id => id.normalize('NFC').toLocaleLowerCase('und');
const isText = v => typeof v === 'string' && v.trim().length > 0;
const gitBlob = bytes => createHash('sha1').update('blob ' + bytes.length + '\0').update(bytes).digest('hex');
const pathSafe = p => typeof p === 'string' && !p.startsWith('/') && !p.split('/').includes('..') && !p.includes('\\');

export function validateShape(obj, schema, where = '$') {
  const errors = [];
  function visit(value, rule, loc) {
    if (rule.type) {
      const types = Array.isArray(rule.type) ? rule.type : [rule.type];
      const ok = types.some(t => t === 'null' ? value === null :
        t === 'array' ? Array.isArray(value) :
        t === 'object' ? value !== null && typeof value === 'object' && !Array.isArray(value) :
        t === 'integer' ? Number.isInteger(value) :
        typeof value === t);
      if (!ok) { errors.push(loc + ': expected ' + types.join('|')); return; }
    }
    if (rule.enum && !rule.enum.includes(value)) errors.push(loc + ': outside enum');
    if (typeof value === 'string') {
      if (rule.minLength !== undefined && value.length < rule.minLength) errors.push(loc + ': too short');
      if (rule.pattern && !(new RegExp(rule.pattern)).test(value)) errors.push(loc + ': pattern mismatch');
    }
    if (typeof value === 'number' && rule.minimum !== undefined && value < rule.minimum) errors.push(loc + ': below minimum');
    if (Array.isArray(value)) {
      if (rule.uniqueItems && new Set(value.map(x => JSON.stringify(x))).size !== value.length) errors.push(loc + ': duplicate array item');
      if (rule.items) value.forEach((x, i) => visit(x, rule.items, loc + '[' + i + ']'));
    }
    if (value && typeof value === 'object' && !Array.isArray(value)) {
      for (const key of rule.required || []) if (!Object.hasOwn(value, key)) errors.push(loc + ': missing ' + key);
      if (rule.additionalProperties === false) for (const key of Object.keys(value))
        if (!Object.hasOwn(rule.properties || {}, key)) errors.push(loc + ': unexpected ' + key);
      for (const [key, sub] of Object.entries(rule.properties || {}))
        if (Object.hasOwn(value, key)) visit(value[key], sub, loc + '.' + key);
    }
  }
  visit(obj, schema, where);
  return errors;
}

function scan(dir, out) {
  if (!existsSync(dir)) return;
  for (const ent of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, ent.name);
    if (ent.isDirectory()) scan(p, out);
    else if (ent.isFile() && (ent.name === 'assunto.json' || p.endsWith('/estado/atual.json'))) out.push(p);
  }
}

export function validateCandidates(root = process.cwd(), { overrides = {} } = {}) {
  const errors = [], deferred = [], checked = [];
  const push = (code, path, detail) => errors.push({ code, path, detail });
  const read = p => Object.hasOwn(overrides, p) ? structuredClone(overrides[p]) : JSON.parse(readFileSync(resolve(root, p), 'utf8'));
  const schemas = Object.fromEntries(['subject', 'record', 'relation', 'knowledge', 'checkpoint'].map(name =>
    [name, JSON.parse(readFileSync(resolve(root, S + name + '-candidate.schema.json'), 'utf8'))]));
  const entries = [];
  for (const prefix of OWNERS) scan(resolve(root, prefix), entries);
  entries.sort();
  const subjects = new Map(), items = [];
  for (const abs of entries) {
    const p = relative(root, abs).split(sep).join('/');
    let doc;
    try { doc = read(p); } catch (e) { push('V01_JSON', p, String(e)); continue; }
    const isState = p.endsWith('/estado/atual.json');
    const schema = schemas[isState ? 'checkpoint' : 'subject'];
    for (const err of validateShape(doc, schema)) push('V01_SCHEMA', p, err);
    checked.push(p);
    if (!isText(doc.subject_id)) { push('V02_ID', p, 'missing subject_id'); continue; }
    const n = norm(doc.subject_id);
    const previous = subjects.get(n);
    if (previous && !(dirname(previous.path) === dirname(p) && previous.isState !== isState))
      push('V02_COLLISION', p, 'subject_id collides with ' + previous.path);
    if (!/^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$/.test(doc.subject_id)) push('V02_ID', p, 'subject_id must be stable lowercase kebab-case');
    if (!isState) {
      if (doc.status !== 'CANDIDATE') push('V04_PROMOTION', p, 'prototype cannot become active by schema edit');
      if (!isText(doc.owner_scope) || !p.startsWith(doc.owner_scope + '/'))
        push('V04_OWNER', p, 'owner_scope does not own this path');
    } else if (doc.not_operational !== true) push('V04_PROMOTION', p, 'historical checkpoint cannot become operational');
    if (!previous) subjects.set(n, { doc, path:p, isState });
    items.push({ doc, path:p, isState });
  }

  // Check historical source bytes at the exact pinned Git blob value, not current master.
  function checkRefs(doc, p, historicalCommit = null) {
    for (const ref of doc.source_refs || []) {
      if (!pathSafe(ref.id)) { push('V03_SOURCE_PATH', p, 'invalid relative source'); continue; }
      const f = resolve(root, ref.id);
      if (!existsSync(f) || !statSync(f).isFile()) {
        // Historical sources absent from candidate HEAD remain addressable by commit/path/blob.
        const commit = ref.source_commit || historicalCommit;
        if (/^[a-f0-9]{40}$/.test(commit || '') && /^[a-f0-9]{40}$/.test(ref.sha || '')) {
          try {
            const actual = execFileSync('git', ['rev-parse', commit + ':' + ref.id], { cwd: root, encoding: 'utf8', stdio:['ignore','pipe','ignore'] }).trim();
            if (actual === ref.sha) {
              deferred.push({ path:p, target:ref.id, reason:'PINNED_HISTORICAL_SOURCE_NOT_IN_CANDIDATE_HEAD' });
              continue;
            }
          } catch { /* source unavailable from local checkout */ }
        }
        push('V03_SOURCE_MISSING', p, ref.id);
        continue;
      }
      if (ref.sha && gitBlob(readFileSync(f)) !== ref.sha) push('V03_SOURCE_SHA', p, ref.id);
      if (!ref.sha && !ref.source_commit) deferred.push({ path:p, target:ref.id, reason:'SOURCE_UNPINNED' });
    }
  }
  for (const { doc, path:p, isState } of items) {
    const historicalCommit = isState ? doc.source_commit : p.endsWith('/estado/assunto.json')
      ? read(posix.join(dirname(p), 'atual.json')).source_commit : null;
    checkRefs(doc, p, historicalCommit);
    if (!isState) {
      for (const linked of doc.related_subject_ids || []) {
        if (!subjects.has(norm(linked))) push('V03_SUBJECT_REF', p, linked);
      }
      const parent = dirname(p);
      const others = readdirSync(resolve(root, parent)).filter(f => f.endsWith('.json') && !f.endsWith('.source.json') && f !== 'assunto.json' && f !== 'atual.json');
      for (const file of others) {
        const childPath = posix.join(parent, file); let child;
        try { child = read(childPath); } catch(e) { push('V01_JSON', childPath, String(e)); continue; }
        checked.push(childPath);
        if (child.subject_id !== doc.subject_id) push('V04_OWNER', childPath, 'payload subject_id differs from owner');
        checkRefs(child, childPath);
        if (file === 'relacoes.json') {
          for (const e of validateShape(child, schemas.relation)) push('V01_SCHEMA', childPath, e);
          for (const rel of child.relations || []) {
            if (rel.owner_subject_id !== doc.subject_id) push('V04_RELATION_OWNER', childPath, rel.relation_id);
            if (!EPISTEMIC.has(rel.epistemic_status) || !VISIBILITY.has(rel.visibility)) push('V04_EPISTEMIC', childPath, rel.relation_id);
            if (rel.inverse_is_derived !== true) push('V03_INVERSE', childPath, rel.relation_id);
            for (const target of [rel.from_subject_id, rel.to_subject_id]) {
              if (!isText(target) || !subjects.has(norm(target))) {
                if (child.external_target_id_not_migrated_in_phase_b === true && target === 'pc-bartholomeu-krauser')
                  deferred.push({ path:childPath, target, reason:'EXTERNAL_NOT_MIGRATED_C41' });
                else push('V03_TARGET_NOT_FOUND', childPath, String(target));
              }
            }
          }
        }
        if (file === 'conhecimento.json') {
          if (child.status === 'CANDIDATE_C45_NOT_ACTIVE') {
            const rows=child.records;
            if (child.subject_id !== doc.subject_id ||
                doc.subject_id !== 'chr001-knowledge-' + child.actor_id ||
                doc.visibility !== 'SYSTEM_AUDIT' ||
                !child.actor_id?.startsWith('npc-') ||
                child.no_global_fact_promotion !== true ||
                child.no_cross_actor_inference !== true ||
                child.no_player_disclosure !== true ||
                child.source_record_count !== 47 ||
                !Array.isArray(rows) || rows.length === 0 ||
                new Set(rows.map(x=>x.source_row_index)).size !== rows.length ||
                rows.some(x=>!Number.isInteger(x.source_row_index) ||
                  x.source_row_index < 0 || x.source_row_index >= 47 ||
                  x.record?.entity !== child.actor_id ||
                  !['confirmed','claims','suspected','unknown'].every(k=>Array.isArray(x.record[k]))))
              push('V04_ACTOR_SOURCE_SCOPE', childPath, 'C45 actor slice must retain exact situated record indexes, classes and no promotion');
          } else {
            for (const e of validateShape(child, schemas.knowledge)) push('V01_SCHEMA', childPath, e);
            if (!subjects.has(norm(child.actor_id || '')) || !doc.subject_id.endsWith('-' + child.actor_id))
              push('V04_ACTOR', childPath, 'actor must match locally sourced NPC (C41 sample)');
            if (child.claims_are_not_world_facts !== true) push('V04_CLAIM_PROMOTION', childPath, 'NPC_CLAIM cannot be CONFIRMED by copying');
          }
        }
        if (file === 'trama.json' && (child.future_contact_realized !== false || child.pc_obligation_created !== false))
          push('V04_UNSOURCED_FUTURE', childPath, 'historical candidate does not attest future contact or obligation');
        if (file === 'historia.json' && child.technical_ledger_proven !== false)
          push('V04_FAKE_LEDGER', childPath, 'historical prose does not attest technical ledger');
      }
    } else {
      const a=doc.resources || {}, c=doc.checkpoint || {};
      if (!Number.isInteger(a.xp_total) || a.xp_spent + a.xp_remaining !== a.xp_total) push('V04_RESOURCES', p, 'XP totals inconsistent');
      if (!Number.isInteger(a.willpower_provisional_max) || a.willpower_available + a.willpower_superficial_damage + a.willpower_aggravated_damage !== a.willpower_provisional_max)
        push('V04_RESOURCES', p, 'willpower totals inconsistent');
      if (c.mortal === true && c.embrace_occurred === true) push('V04_STATE', p, 'mortal and embraced simultaneously');
      for (const [key, shaKey] of [['source_live','sha'],['cycle','sha'],['manifest_ref','blob_sha']]) {
        const ref=doc[key];
        if (ref && ref.path) checkRefs({source_refs:[{id:ref.path,sha:ref[shaKey]}]}, p, doc.source_commit);
      }
    }
  }
  return { ok: errors.length === 0, checked: checked.length, subjects: subjects.size, errors, deferred };
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const result = validateCandidates();
  console.log(JSON.stringify(result, null, 2));
  process.exitCode = result.ok ? 0 : 1;
}
