#!/usr/bin/env python3
"""Repository-specific structure checks, not an OpenAI approval validator."""
import argparse
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def validate(root=ROOT, submission=False):
    plugin=root/'plugins/mood-journal';skill=plugin/'skills/mood-journal'
    portable=json.loads((plugin/'plugin.json').read_text())
    compat=json.loads((plugin/'.codex-plugin/plugin.json').read_text())
    for key in ('name','version','description'):
        assert portable[key]==compat[key], f'Manifest mismatch: {key}'
    assert portable['name']==plugin.name
    assert re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)',portable['version'])
    assert portable['$schema']=='https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
    assert portable['extensions']['com.openai']=={'interface':compat['interface']}
    assert compat['license']=='CC-BY-SA-4.0'
    assert not any(x in compat for x in ('apps','mcpServers','hooks'))
    for path in plugin.rglob('*'):
        assert not path.is_symlink(), f'Symlink: {path}'
        assert path.name not in ('.app.json','.mcp.json','mcp.json','hooks.json')
    entry=(skill/'SKILL.md').read_text()
    assert entry.startswith('---\nname: mood-journal\ndescription: ')
    assert len(entry.split('---',2)[1])<1100
    for doc in skill.rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
            if '://' in target or target.startswith('#'):continue
            resolved=(doc.parent/target.split('#')[0]).resolve()
            assert resolved.is_relative_to(skill.resolve()), f'Non-self-contained skill reference: {target}'
            assert resolved.is_file(), f'Missing reference: {target}'
    for screenshot in compat['interface'].get('screenshots',[]):
        assert screenshot.startswith('./assets/') and screenshot.endswith('.png')
        assert (plugin/screenshot).is_file()
    for asset in ('logo','composerIcon'):
        assert (plugin/compat['interface'][asset]).is_file()
    market=json.loads((root/'.agents/plugins/marketplace.json').read_text())
    item=market['plugins'][0]
    assert item['source']=={'source':'local','path':'./plugins/mood-journal'}
    assert item['name']==portable['name']
    assert item['policy']=={'installation':'AVAILABLE','authentication':'ON_INSTALL'}
    cases=json.loads((root/'submission/test-cases.json').read_text())
    assert len(cases['positive'])>=5 and len(cases['negative'])>=3
    for name in ('LICENSE','NOTICE.md'):
        assert (root/name).read_bytes()==(plugin/name).read_bytes()==(skill/name).read_bytes()
    if submission:
        data=json.loads((root/'submission/listing.json').read_text())
        missing=[key for key in ('publisher_name','countries','developer_identity_verified',
                 'policy_attestations_completed','cloud_mobile_tests_completed') if not data.get(key)]
        for key in ('website_url','support_url','privacy_policy_url','terms_url'):
            if not isinstance(data.get(key),str) or not data[key].startswith('https://'): missing.append(key)
        assert not missing, 'Publisher completion still required: '+', '.join(missing)
    return portable['version']

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--submission',action='store_true')
    args=parser.parse_args();print('Validated package '+validate(submission=args.submission))
