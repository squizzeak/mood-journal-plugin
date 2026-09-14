import datetime as dt
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('release',ROOT/'scripts/release.py')
release=importlib.util.module_from_spec(spec);spec.loader.exec_module(release)

class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        shutil.copytree(ROOT/'plugins',self.root/'plugins')
        for folder in ('.agents','submission','docs'):
            shutil.copytree(ROOT/folder,self.root/folder)
        for file in ('README.md','LICENSE','NOTICE.md','PRIVACY.md','TERMS.md','CHANGELOG.md','.gitignore'):
            shutil.copy(ROOT/file,self.root/file)
        self.git('init','-b','main');self.git('config','user.name','Test');self.git('config','user.email','test@example.invalid')
        self.commit('feat: initial journal')
    def tearDown(self): self.temp.cleanup()
    def git(self,*args):return release.git(*args,cwd=self.root)
    def commit(self,message):
        self.git('add','.');self.git('commit','-m',message)
    def test_calver_same_day_and_year_rollover(self):
        self.assertEqual(release.next_version(dt.date(2026,9,12),['v2026.912.0','v2026.912.2','other']), '2026.912.3')
        self.assertEqual(release.next_version(dt.date(2027,1,2),['v2026.912.2']), '2027.102.0')
    def test_first_release_and_incremental_notes(self):
        meta=release.prepare([],dt.date(2026,9,12),self.root)
        self.assertEqual(meta['version'],'2026.912.0')
        self.assertIn('initial journal',(self.root/'.release/notes.md').read_text())
        self.commit('chore(release): v2026.912.0');self.git('tag','v2026.912.0')
        (self.root/'new.txt').write_text('new');self.commit('fix: preserve old dates')
        releases=[{'tag_name':'v2026.912.0','published_at':'2026-09-12T12:00:00Z','draft':False,'prerelease':False}]
        meta=release.prepare(releases,dt.date(2026,9,12),self.root)
        notes=(self.root/'.release/notes.md').read_text()
        self.assertEqual(meta['version'],'2026.912.1')
        self.assertIn('preserve old dates',notes);self.assertNotIn('initial journal',notes)
        self.assertIn('initial journal',(self.root/'CHANGELOG.md').read_text())
    def test_draft_ignored_no_new_content_rejected(self):
        self.git('tag','v2026.912.0')
        draft={'tag_name':'missing','published_at':None,'draft':True}
        self.assertIsNone(release.previous_release([draft],self.root))
        with self.assertRaises(ValueError):release.commit_notes('v2026.912.0',self.root)
    def test_dirty_tree_rejected(self):
        (self.root/'README.md').write_text('changed')
        with self.assertRaises(ValueError):release.prepare([],dt.date(2026,9,12),self.root)
    def test_missing_published_tag_rejected(self):
        with self.assertRaises(ValueError):
            release.previous_release([{'tag_name':'absent','published_at':'2026-09-12','draft':False}],self.root)
    def test_subjects_are_data(self):
        (self.root/'change').write_text('safe');self.commit('fix: `touch /tmp/not-executed` <unsafe> $(whoami)')
        notes=release.commit_notes(None,self.root)
        self.assertIn('\\`touch',notes);self.assertIn('&lt;unsafe&gt;',notes)
    def test_artifact_layout_and_reproducibility(self):
        (self.root/'private.txt').write_text('should not ship');self.commit('test: private exclusion fixture')
        (self.root/'plugins/mood-journal/untracked-secret').write_text('not tracked')
        a=self.root/'dist/a';b=self.root/'dist/b'
        release.build(self.root,a);release.build(self.root,b)
        for path in a.glob('*.zip'):
            self.assertEqual(path.read_bytes(),(b/path.name).read_bytes())
            with zipfile.ZipFile(path) as z:
                self.assertIsNone(z.testzip())
                self.assertFalse(any('private.txt' in name or 'untracked-secret' in name or '.git/' in name for name in z.namelist()))
        with zipfile.ZipFile(next(a.glob('*-directory.zip'))) as z:
            self.assertIn('plugin.json',z.namelist());self.assertNotIn('.codex-plugin/plugin.json',z.namelist())
            self.assertIn('assets/example-prompts.png',z.namelist())
            self.assertIn('skills/mood-journal/scripts/ingest_chats.py',z.namelist())
            self.assertIn('skills/mood-journal/references/handoff-entry-schema.md',z.namelist())
            self.assertIn('skills/mood-journal/scripts/select_handoff.py',z.namelist())
        with zipfile.ZipFile(next(a.glob('*-skills.zip'))) as z:
            self.assertIn('mood-journal/SKILL.md',z.namelist());self.assertIn('mood-journal/NOTICE.md',z.namelist())
        with zipfile.ZipFile(next(a.glob('*-submission-kit.zip'))) as z:
            self.assertIn('plugins/mood-journal/assets/example-prompts.png',z.namelist())
    def test_symlink_rejected(self):
        (self.root/'linked').symlink_to(self.root/'README.md');self.commit('test: symlink fixture')
        with self.assertRaises(ValueError):release.build(self.root)

if __name__=='__main__':unittest.main()
