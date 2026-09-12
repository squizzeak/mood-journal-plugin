#!/usr/bin/env python3
"""Build allowlisted release artifacts; no third-party Python dependencies."""
import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = Path('plugins/mood-journal')
CALVER = re.compile(r'^v(\d{4})\.(\d{1,4})\.(\d+)$')
RELEASE_SUBJECT = re.compile(r'^chore\(release\): v\d{4}\.\d{1,4}\.\d+$')


def git(*args, cwd=ROOT):
    return subprocess.check_output(['git', *args], cwd=cwd, text=True).strip()


def next_version(day, tags):
    middle = day.month * 100 + day.day
    sequence = [int(m[3]) for tag in tags if (m := CALVER.fullmatch(tag))
                and int(m[1]) == day.year and int(m[2]) == middle]
    return f'{day.year}.{middle}.{max(sequence, default=-1) + 1}'


def previous_release(releases, cwd=ROOT):
    published = sorted((x for x in releases if not x.get('draft') and not x.get('prerelease')),
                       key=lambda x: x['published_at'], reverse=True)
    for item in published:
        tag = item['tag_name']
        # Resolve as an exact tag, never as a command-line option or revision expression.
        ref = f'refs/tags/{tag}'
        if subprocess.run(['git', 'show-ref', '--verify', '--quiet', ref], cwd=cwd).returncode:
            raise ValueError(f'Published release tag missing locally: {tag}; fetch all tags.')
        sha = git('rev-parse', '--verify', ref, cwd=cwd)
        if subprocess.run(['git', 'merge-base', '--is-ancestor', sha, 'HEAD'], cwd=cwd).returncode == 0:
            return tag
    if published:
        raise ValueError('No published release is an ancestor of HEAD; refusing an accidental initial release.')
    return None


def commit_notes(previous, cwd=ROOT):
    end = 'HEAD'
    if previous:
        sha = git('rev-parse', '--verify', f'refs/tags/{previous}', cwd=cwd)
        end = f'{sha}..HEAD'
    rows = git('log', '--reverse', '--format=%H%x09%s', end, cwd=cwd).splitlines()
    entries = [(sha, title) for row in rows if row for sha, title in [row.split('\t', 1)]
               if not RELEASE_SUBJECT.fullmatch(title)]
    if not entries:
        raise ValueError('No new non-release commits. Recover an incomplete release instead of duplicating it.')
    # Escape Markdown/HTML in untrusted commit subjects; never execute their content.
    def escape(text):
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return re.sub(r'([\\`*_\[\]])', r'\\\1', text)
    return '\n'.join(f'- {escape(title)} (`{sha[:12]}`)' for sha, title in entries) + '\n'


def prepare(releases, day, cwd=ROOT):
    if git('status', '--porcelain', cwd=cwd):
        raise ValueError('Preparation requires a clean working tree.')
    previous = previous_release(releases, cwd)
    version = next_version(day, git('tag', '--list', cwd=cwd).splitlines())
    notes = f'## v{version} — {day.isoformat()}\n\n'
    notes += f'Changes since {previous}.\n\n' if previous else 'Initial release.\n\n'
    notes += commit_notes(previous, cwd)
    old = (cwd/'CHANGELOG.md').read_text()
    # Current branch includes prior release commits; maintain the cumulative changelog.
    if old.startswith('# Changelog\n'):
        old = old[len('# Changelog\n'):].lstrip()
    for name in ('plugin.json', '.codex-plugin/plugin.json'):
        path = cwd/PLUGIN/name
        data = json.loads(path.read_text()); data['version'] = version
        path.write_text(json.dumps(data, indent=2) + '\n')
    (cwd/'CHANGELOG.md').write_text('# Changelog\n\n' + notes + '\n' + old)
    stage = cwd/'.release';stage.mkdir(exist_ok=True)
    (stage/'notes.md').write_text(notes)
    metadata = {'version':version, 'tag':f'v{version}', 'date':day.isoformat(),
                'previous_release':previous, 'source_commit':git('rev-parse', 'HEAD', cwd=cwd)}
    (stage/'metadata.json').write_text(json.dumps(metadata, indent=2)+'\n')
    return metadata


def write_zip(path, files):
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in sorted(files.items()):
            parts = Path(name).parts
            if name.startswith('/') or '..' in parts:
                raise ValueError(f'Unsafe archive path: {name}')
            info = zipfile.ZipInfo(name, (2020,1,1,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise ValueError(f'Corrupt ZIP: {path}')


def build(cwd=ROOT, output=None):
    output = output or cwd/'dist';output.mkdir(parents=True, exist_ok=True)
    version = json.loads((cwd/PLUGIN/'plugin.json').read_text())['version']
    # Only tracked, allowlisted files enter release archives. Reject symlinks.
    paths = git('ls-files', '-z', cwd=cwd).split('\0')
    tracked = {}
    for name in paths:
        if not name: continue
        path = cwd/name
        if path.is_symlink(): raise ValueError(f'Symlink not permitted in release: {name}')
        if path.is_file(): tracked[name] = path.read_bytes()
    prefix = str(PLUGIN)+'/'
    plugin = {name[len(prefix):]:value for name,value in tracked.items() if name.startswith(prefix)}
    portable = {name:value for name,value in plugin.items() if not name.startswith('.codex-plugin/')}
    skills = {name[len('skills/'):]:value for name,value in plugin.items() if name.startswith('skills/')}
    required = ('README.md','LICENSE','NOTICE.md','PRIVACY.md','TERMS.md','CHANGELOG.md')
    marketplace = {name:tracked[name] for name in required}
    marketplace['.agents/plugins/marketplace.json'] = tracked['.agents/plugins/marketplace.json']
    marketplace.update({prefix+name:value for name,value in plugin.items()})
    marketplace.update({name:value for name,value in tracked.items() if name.startswith(('docs/','submission/','scripts/','tests/','.github/')) or name in ('AGENTS.md','CONTRIBUTING.md','.gitignore','.gitattributes')})
    kit = {name:value for name,value in tracked.items() if name.startswith('submission/')}
    kit.update({name:tracked[name] for name in ('LICENSE','NOTICE.md','PRIVACY.md','TERMS.md')})
    kit['plugins/mood-journal/assets/logo.png'] = plugin['assets/logo.png']
    kit['plugins/mood-journal/assets/example-prompts.png'] = plugin['assets/example-prompts.png']
    kit.update({name:value for name,value in tracked.items() if name.startswith('docs/')})
    archives = {'directory':portable,'skills':skills,'marketplace':marketplace,'submission-kit':kit}
    results = []
    for kind, contents in archives.items():
        path = output/f'mood-journal-{version}-{kind}.zip'
        write_zip(path, contents); results.append(path)
    notes = cwd/'.release/notes.md'
    dest = output/'RELEASE-NOTES.md'
    dest.write_text(notes.read_text() if notes.exists() else (cwd/'CHANGELOG.md').read_text());results.append(dest)
    provenance = {'version':version,'commit':git('rev-parse','HEAD',cwd=cwd),
                  'working_tree_modified':bool(git('status','--porcelain',cwd=cwd)),
                  'artifacts':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in results}}
    dest = output/'BUILD-INFO.json';dest.write_text(json.dumps(provenance,indent=2)+'\n');results.append(dest)
    (output/'SHA256SUMS').write_text(''.join(f'{hashlib.sha256(x.read_bytes()).hexdigest()}  {x.name}\n' for x in results))
    return results


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('prepare','build'))
    parser.add_argument('--releases-json',type=Path,help='GitHub REST releases array (including all pages)')
    args=parser.parse_args()
    if args.command=='prepare':
        if not args.releases_json: parser.error('prepare requires --releases-json; use [] for a verified first release')
        data=json.loads(args.releases_json.read_text())
        releases=[item for page in data for item in page] if data and isinstance(data[0],list) else data
        result=prepare(releases,dt.datetime.now(dt.timezone.utc).date())
        print(json.dumps(result))
    else:
        for path in build(): print(path)

if __name__=='__main__': main()
