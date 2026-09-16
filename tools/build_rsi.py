#!/usr/bin/env python3
"""Build the RSI dashboard with Python's standard library.

Refresh from a trusted viewer snapshot:
  python3 tools/build_rsi.py --snapshot /path/to/data.json
Reproduce from the committed public aggregate data:
  python3 tools/build_rsi.py

Only explicitly selected numeric results and model identifiers are exported.
Raw transcripts, commands, workspaces and filesystem paths are not published.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def export(snapshot):
    raw = snapshot.read_bytes()
    source = json.loads(raw)
    episodes = source['episodes']
    complete = [e for e in episodes if e.get('test_nll') is not None]
    identity_fields = ['core_git', 'train_manifest_sha256', 'task_manifest_sha256',
                       'challenge_manifest_sha256', 'evaluator_sha256', 'hidden_evaluation']
    for key in identity_fields:
        identities = {json.dumps(e['artifact_identities'][key], sort_keys=True) for e in complete}
        if len(identities) != 1:
            raise ValueError(f'Mixed evaluation identities: {key}')
    pairs = [(e['model_short'], e['track']) for e in episodes]
    if len(set(pairs)) != len(pairs):
        raise ValueError('Select one authorized attempt per model and track before exporting.')
    rows = []
    for e in episodes:
        candidates = {c['id']: c for c in e['candidates']}
        ended = {v['lease_id']: v for v in e['events'] if v['type'] == 'LEASE_ENDED'}
        commits = sorted([v for v in e['events'] if v['type'] == 'CANDIDATE_COMMITTED'],
                         key=lambda v: v['commit_index'])
        points = []
        for event in commits:
            candidate = candidates[event['candidate_id']]
            if candidate.get('val_nll') is None:
                continue
            elapsed = event['elapsed_seconds']
            points.append({
                'index': event['commit_index'],
                'lease': event.get('lease_id', candidate.get('source_lease')),
                'hours': sum(v['used_seconds'] for v in ended.values() if v['elapsed_seconds'] <= elapsed) / 3600,
                'nll': candidate['val_nll'],
                'final': candidate['id'] == e.get('final_candidate_id'),
            })
        ms = e.get('test_time_per_task')
        rows.append({
            'model': e['model_short'], 'track': e['track'],
            'status': e['status'], 'outcome': e.get('outcome'),
            'test_nll': e.get('test_nll'), 'score': e.get('test_score'),
            'ms': None if ms is None else 1000 * ms,
            'lease_hours': e['timing'].get('training_lease_seconds', 0) / 3600,
            'research_hours': e['timing'].get('official_elapsed_seconds', 0) / 3600,
            'leases': e['leases_used'], 'candidates': len(candidates),
            'first_analysis': e.get('first_val'), 'final_analysis': e.get('final_val'),
            'reasoning_effort': e.get('reasoning_effort'), 'points': points,
        })
    return {
        'schema_version': 1, 'generated_at': source['generated_at'],
        'source_sha256': hashlib.sha256(raw).hexdigest(),
        'core_revision': complete[0]['repo_commit'] if complete else None,
        'runtime': '1 × NVIDIA H200 SXM 141GB', 'task': 'lm-pretrain',
        'selection': 'Latest authorized attempt per model/track; previous failed attempts excluded.',
        'excluded_attempts': [
            {'model': v['model'], 'track': v['track'], 'outcome': v['outcome']}
            for v in source.get('excluded_attempts', [])
        ],
        'preview': True, 'rows': rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', type=Path)
    args = parser.parse_args()
    output = ROOT / 'rsi'
    output.mkdir(exist_ok=True)
    if args.snapshot:
        data = export(args.snapshot)
    else:
        data = json.loads((output / 'data.json').read_text())
    payload = json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False)
    # Catch accidental private paths before writing anything to the public site.
    for token in ['/mnt/', '/home/', '/media/', '/ibex/', 'api_key', 'Authorization', 'agent.stdout']:
        if token in payload:
            raise ValueError(f'Unexpected private information in public aggregates: {token}')
    (output / 'data.json').write_text(payload + '\n')
    template = (ROOT / 'tools' / 'rsi-template.html').read_text()
    if template.count('__RSI_DATA__') != 1:
        raise ValueError('The template must contain exactly one data placeholder.')
    page = template.replace('__RSI_DATA__', payload.replace('<', '\\u003c'))
    (output / 'index.html').write_text(page.replace('__DATA_URL__', 'data.json'))
    (ROOT / 'index.html').write_text(page.replace('__DATA_URL__', 'rsi/data.json'))
    print(f"Built latest-only dashboard: {len(data['rows'])} runs, snapshot {data['generated_at']}")


if __name__ == '__main__':
    main()
