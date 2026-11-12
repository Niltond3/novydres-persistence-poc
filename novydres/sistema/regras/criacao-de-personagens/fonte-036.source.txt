"""Stateless CLI used by ChatGPT's transient Python runtime, NOT by the player."""
import argparse, json, sys
from webfirst_core import (create_store, parse_store, serialize_store, validate_store,
                           append_event, apply_pool_roll, apply_rouse, plan_drive_replace)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('operation',choices=['init','validate','append','roll','rouse','drive_replace'])
    p.add_argument('--store',help='JSON file read from Google Drive connector')
    p.add_argument('--cmd',help='JSON file with explicit ChatGPT request / rule parameters')
    p.add_argument('--source-event')
    a=p.parse_args()
    old=open(a.store,encoding='utf8').read() if a.store else None
    doc=create_store() if a.operation=='init' else parse_store(old)
    if a.operation=='validate': print(json.dumps(validate_store(doc),ensure_ascii=False,sort_keys=True));return
    if a.operation=='append': doc=append_event(doc,json.load(open(a.cmd,encoding='utf8')))
    if a.operation=='roll': doc=apply_pool_roll(doc,json.load(open(a.cmd,encoding='utf8')),source_event_id=a.source_event)
    if a.operation=='rouse': doc=apply_rouse(doc,source_event_id=a.source_event)
    if a.operation=='drive_replace':
        updated=json.load(open(a.cmd,encoding='utf8'))
        print(json.dumps({'replaceAllText':plan_drive_replace(old,updated)},ensure_ascii=False));return
    print(serialize_store(doc))
if __name__=='__main__':
    try: main()
    except Exception as exc:
        print(f'REJECTED: {type(exc).__name__}: {exc}',file=sys.stderr);sys.exit(2)
