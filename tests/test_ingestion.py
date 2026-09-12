import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ingest',ROOT/'plugins/mood-journal/skills/mood-journal/scripts/ingest_chats.py')
ingest=importlib.util.module_from_spec(spec);spec.loader.exec_module(ingest)

class IngestionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.source=self.root/'export.json'
        self.selected={'id':'selected','title':'Fictional reflection','create_time':1700000000,'current_node':'b',
            'mapping':{'a':{'parent':None,'message':{'id':'u','author':{'role':'user'},'create_time':1700000000,'content':{'parts':['I felt tired.']}}},
                       'b':{'parent':'a','message':{'id':'a','author':{'role':'assistant'},'content':{'parts':['What mattered today?']}}},
                       'alternate':{'parent':'a','message':{'id':'x','author':{'role':'assistant'},'content':{'parts':['Alternate response']}}}}}
        self.source.write_text(json.dumps([self.selected,{'id':'unselected','messages':[{'role':'user','content':'other project'}]}]))
    def tearDown(self):self.temp.cleanup()
    def test_selection_branch_provenance_no_synthesis(self):
        original=self.source.read_bytes();ledger=ingest.ingest(self.source,['selected'],self.root/'out')
        entry=ledger['entries'][0]
        self.assertEqual(len(ledger['entries']),1);self.assertEqual(entry['excluded_branch_nodes'],['alternate'])
        transcript=(self.root/'out'/entry['transcript_path']).read_text()
        self.assertIn('I felt tired.',transcript);self.assertNotIn('Alternate response',transcript)
        self.assertNotIn('other project',transcript)
        self.assertIn('Alternate response',(self.root/'out'/entry['raw_path']).read_text())
        self.assertEqual(entry['synthesis_status'],'pending');self.assertEqual(self.source.read_bytes(),original)
    def test_rejects_unknown_or_duplicate_selection(self):
        for ids in (['missing'],['selected','selected'],[]):
            with self.assertRaises(ValueError):ingest.ingest(self.source,ids,self.root/'out')
        self.assertFalse((self.root/'out').exists())
    def test_does_not_overwrite_previous_import(self):
        ingest.ingest(self.source,['selected'],self.root/'out')
        with self.assertRaises(FileExistsError):ingest.ingest(self.source,['selected'],self.root/'out')
    def test_branch_cycle_fails_before_writes(self):
        self.selected['mapping']['a']['parent']='b';self.source.write_text(json.dumps([self.selected]))
        with self.assertRaises(ValueError):ingest.ingest(self.source,['selected'],self.root/'out')
        self.assertFalse((self.root/'out').exists())
    def test_non_text_marked_not_invented(self):
        self.selected['mapping']['a']['message']['content']['parts'].append({'image':'unavailable'})
        self.source.write_text(json.dumps([self.selected]));ledger=ingest.ingest(self.source,['selected'],self.root/'out')
        self.assertEqual(ledger['entries'][0]['limitations'][0]['reason'],'non-text content not rendered')

if __name__=='__main__':unittest.main()
