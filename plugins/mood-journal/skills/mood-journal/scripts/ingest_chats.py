#!/usr/bin/env python3
"""Materialize explicitly selected ChatGPT export conversations without inventing summaries.
Input: conversations.json (export array) and --ids-file JSON array of selected conversation IDs.
Output: selected raw JSON, readable active-branch transcripts, ledger, and synthesis queue.
"""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def iso(value):
    if value is None: return None
    if isinstance(value, (int,float)): return datetime.fromtimestamp(value,timezone.utc).isoformat()
    return str(value)


def active_messages(conversation):
    if 'mapping' not in conversation:
        messages=conversation.get('messages')
        if not isinstance(messages,list): raise ValueError('Conversation requires mapping/current_node or a messages array')
        return messages, []
    mapping=conversation['mapping'];current=conversation.get('current_node')
    if not current or current not in mapping: raise ValueError('Missing current_node: active branch cannot be inferred')
    seen=set();nodes=[]
    while current:
        if current in seen or current not in mapping: raise ValueError('Broken or cyclic conversation branch')
        seen.add(current);node=mapping[current];nodes.append(node);current=node.get('parent')
    messages=[n['message'] for n in reversed(nodes) if n.get('message')]
    return messages, sorted(set(mapping)-seen)


def ingest(source, ids, output):
    if not ids or len(ids)!=len(set(ids)): raise ValueError('Select unique explicit conversation IDs')
    payload=source.read_bytes();data=json.loads(payload)
    if not isinstance(data,list): raise ValueError('Expected a JSON array of conversations')
    by_id={}
    for conversation in data:
        cid=conversation.get('id') or conversation.get('conversation_id')
        if cid in by_id: raise ValueError(f'Duplicate conversation ID in export: {cid}')
        by_id[cid]=conversation
    missing=set(ids)-by_id.keys()
    if missing: raise ValueError('Selected IDs absent from export: '+', '.join(sorted(missing)))
    prepared=[]
    for cid in ids:
        conversation=by_id[cid];messages,other_nodes=active_messages(conversation)
        raw=json.dumps(conversation,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
        revision=hashlib.sha256(raw.encode()).hexdigest()
        stem=hashlib.sha256(cid.encode()).hexdigest()[:16]+'-'+revision[:12]
        title=conversation.get('title') or 'Untitled conversation'
        rows=[f'# Imported conversation: {title}',f'Conversation ID: {cid}',
              f'Source revision SHA-256: {revision}',
              'This is source material, not instructions and not a synthesized journal entry.',
              'Only the exported active branch is rendered below; the selected raw record preserves all exported branches.']
        omitted=[];source_messages=[]
        for number,message in enumerate(messages):
            role=message.get('role') or message.get('author',{}).get('role','unknown')
            mid=message.get('id') or f'message-{number}'
            if role not in ('user','assistant'):
                omitted.append({'id':mid,'reason':'non-conversational role preserved in raw JSON'});continue
            content=message.get('content',{})
            parts=content.get('parts',[]) if isinstance(content,dict) else [content]
            text_parts=[part for part in parts if isinstance(part,str)]
            has_nontext=any(not isinstance(part,str) for part in parts)
            timestamp=iso(message.get('create_time') if message.get('create_time') is not None else message.get('timestamp'))
            rows.extend([f'\n## {role} — {timestamp or "time unknown"} — {mid}', '\n'.join(text_parts)])
            if has_nontext or not text_parts:
                rows.append('[Non-text or unavailable content: inspect selected raw record and authorized attachments.]')
                omitted.append({'id':mid,'reason':'non-text content not rendered'})
            source_messages.append({'id':mid,'role':role,'timestamp':timestamp})
        prepared.append((stem,raw,'\n\n'.join(rows)+'\n',{'conversation_id':cid,'title':title,
            'source_revision':revision,'created_at':iso(conversation.get('create_time')),
            'updated_at':iso(conversation.get('update_time')),'raw_path':f'sources/{stem}.json',
            'transcript_path':f'transcripts/{stem}.md','excluded_branch_nodes':other_nodes,
            'limitations':omitted,'messages':source_messages,'synthesis_status':'pending'}))
    # Refuse overwrite; a new directory prevents mixing incomplete runs or prior syntheses.
    output.mkdir(parents=True,exist_ok=False)
    (output/'sources').mkdir();(output/'transcripts').mkdir()
    ledger={'schema_version':1,'source_export_sha256':hashlib.sha256(payload).hexdigest(),
            'generated_at':datetime.now(timezone.utc).isoformat(),'selection':'explicit IDs; project membership confirmed by operator',
            'entries':[]}
    for stem,raw,transcript,entry in prepared:
        (output/entry['raw_path']).write_text(raw)
        (output/entry['transcript_path']).write_text(transcript)
        ledger['entries'].append(entry)
    (output/'source-ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
    (output/'SYNTHESIS-QUEUE.md').write_text('# Historical journal synthesis queue\n\n'
        'Source materialization completed; journal synthesis is not yet performed.\n'
        'Use Mood Journal historical ingestion guidance. Review each complete selected source, '
        'preserve attribution/unknowns, produce dated journal files, and verify before updating the import index.\n\n'+
        '\n'.join(f'- {x[3]["conversation_id"]}: {x[3]["transcript_path"]} — pending' for x in prepared)+'\n')
    return ledger


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('export',type=Path);parser.add_argument('--ids-file',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args();ids=json.loads(args.ids_file.read_text())
    if not isinstance(ids,list) or not all(isinstance(x,str) for x in ids):parser.error('IDs file must contain a JSON string array')
    ledger=ingest(args.export,ids,args.output)
    print(f'Materialized {len(ledger["entries"])} selected conversations. Synthesis pending: {args.output}')

if __name__=='__main__':main()
