import hashlib
import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('prepare_submission',ROOT/'scripts/prepare_submission.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class PreparationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.assets=self.root/'assets';self.assets.mkdir()
        self.commit='a'*40
        self.release={'tag_name':'v2026.912.0','draft':False,'prerelease':False,'published_at':'2026-09-12T00:00:00Z','html_url':'https://github.com/example/example/releases/tag/v2026.912.0'}
        for kind in ('directory','skills','marketplace','submission-kit'):
            with zipfile.ZipFile(self.assets/f'mood-journal-2026.912.0-{kind}.zip','w') as z:
                if kind=='directory':z.writestr('plugin.json',json.dumps({'version':'2026.912.0'}))
                elif kind=='submission-kit':
                    z.writestr('submission/listing.json',json.dumps({'long_description':'Fictional journaling tool'}))
                    z.writestr('submission/test-results.md','Status: NOT RUN')
                else:z.writestr('fixture.txt','fictional')
        (self.assets/'RELEASE-NOTES.md').write_text('Initial release.\n- fix: preserve prior records\n')
        self.rehash()
    def tearDown(self):self.temp.cleanup()
    def rehash(self):
        hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in self.assets.iterdir() if p.name not in ('BUILD-INFO.json','SHA256SUMS')}
        info={'version':'2026.912.0','commit':self.commit,'working_tree_modified':False,'artifacts':hashes}
        p=self.assets/'BUILD-INFO.json';p.write_text(json.dumps(info));hashes[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
        (self.assets/'SHA256SUMS').write_text(''.join(f'{v}  {k}\n' for k,v in hashes.items()))
    def test_preparation_retains_missing_data_and_never_claims_submission(self):
        result=m.prepare(self.release,self.assets,self.commit,self.root/'out')
        self.assertFalse(result['submitted_to_openai'])
        self.assertIn('publisher_name',result['missing_or_unverified'])
        self.assertIn('recorded_live_test_results',result['missing_or_unverified'])
        self.assertIn('draft',(self.root/'out/USER-CHANGELOG-DRAFT.md').read_text())
    def test_rejects_draft_prerelease_and_unsafe_tag(self):
        for values in ({'draft':True},{'prerelease':True},{'tag_name':'../../bad'}):
            with self.subTest(values=values),self.assertRaises(ValueError):m.verify(dict(self.release,**values),self.assets,self.commit)
    def test_detects_asset_tampering(self):
        (self.assets/'RELEASE-NOTES.md').write_text('modified')
        with self.assertRaises(ValueError):m.verify(self.release,self.assets,self.commit)
    def test_detects_wrong_commit_and_duplicate_checksum(self):
        with self.assertRaises(ValueError):m.verify(self.release,self.assets,'b'*40)
        p=self.assets/'SHA256SUMS';p.write_text(p.read_text()+p.read_text().splitlines()[0]+'\n')
        with self.assertRaises(ValueError):m.verify(self.release,self.assets,self.commit)
    def test_rejects_unsafe_archive_even_with_valid_hash(self):
        with zipfile.ZipFile(self.assets/'mood-journal-2026.912.0-skills.zip','a') as z:z.writestr('../escape','bad')
        self.rehash()
        with self.assertRaises(ValueError):m.verify(self.release,self.assets,self.commit)
    def test_does_not_overwrite_prepared_output(self):
        out=self.root/'out';m.prepare(self.release,self.assets,self.commit,out)
        with self.assertRaises(FileExistsError):m.prepare(self.release,self.assets,self.commit,out)
