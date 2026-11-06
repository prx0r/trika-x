"""Practice-track tests: eligibility gate + C1 unit invariants."""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKOUTS = ROOT.parent.parent
PRACTICE = Path(os.environ.get('SATSANG_PRACTICE_CHECKOUT', CHECKOUTS / 'satsang-practice'))
TW = Path(os.environ.get('TRANSLATION_WORK', CHECKOUTS / 'translation-work'))
SAN = Path(os.environ.get('SANSKRITHELP_CHECKOUT', CHECKOUTS / 'sanskrithelp'))
DB = Path(os.environ.get('DEITYBODY_CHECKOUT', CHECKOUTS / 'deitybody'))


def available(*paths):
    try:
        return all(path.is_file() for path in paths)
    except OSError:
        return False


def load_tool(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


class PracticeTests(unittest.TestCase):
    def test_eligibility_tiers(self):
        e = load_tool("eligibility")
        self.assertEqual(e.classify("sit and watch the breath", "anava", "")["eligibility"], "doable")
        d = e.classify("stop breath, feel the void", "", "")
        self.assertEqual(d["eligibility"], "study")
        self.assertTrue(any("retention" in c for c in d["cautions"]))
        r = e.classify("install the deity with seed mantra from guru", "", "")
        self.assertEqual(r["eligibility"], "requires-diksha")
        self.assertIn("withheld", r["cautions"][0])
        s = e.classify("consider the nature of consciousness", "", "")
        self.assertEqual(s["eligibility"], "study")
        # fail-closed: unknown never doable
        u = e.classify("xqzzy plugh", "mystery", "???")
        self.assertEqual(u["eligibility"], "study")

    def test_path_assembly_no_diy_diksha(self):
        import hashlib
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        units = ROOT / "data" / "unit-vbt-d001.json"
        diksha = {"unit_id": "vbt-dX", "eligibility": {"eligibility": "requires-diksha"},
                  "safety": ["conferred"], "source_refs": []}
        unreviewed = {"unit_id": "vbt-dY", "eligibility": {"eligibility": "doable"},
                      "status": "approved", "steps": [{"text": "a private draft"}]}
        dp = root / 'diksha.json'
        dp.write_text(json.dumps(diksha))
        up = dp.with_name('unreviewed-unit.json')
        up.write_text(json.dumps(unreviewed))
        out = root / 'path-test.json'
        r = subprocess.run([sys.executable, str(ROOT / "tools" / "path_assemble.py"),
                            "--units", str(units), str(dp), str(up), "--spine", "ts-six",
                            "--slug", "test", "--out", str(out)],
                           text=True, capture_output=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        p = json.loads(out.read_text())
        self.assertEqual(p["path_id"], "path:trika/test")
        by_id = {it["unit_id"]: it for it in p["items"]}
        self.assertEqual(by_id["vbt-dX"]["render"]["mode"], "STUDY")
        self.assertNotIn("unit", by_id["vbt-dX"]["render"])
        self.assertEqual(by_id["vbt-dY"]["render"]["mode"], "STUDY")
        self.assertFalse(by_id["vbt-dY"]["render"]["practice_authorized"])
        self.assertNotIn("steps", by_id["vbt-dY"]["render"])
        self.assertEqual(p['prereq_edges'], [])
        self.assertEqual(len(p['sequence_edges']), 2)
        body = {k: v for k, v in p.items() if k != "path_sha256"}
        self.assertEqual(p["path_sha256"], hashlib.sha256(
            json.dumps(body, sort_keys=True).encode()).hexdigest())

    def test_day_gate_counts_posting_days(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        log = Path(tmp.name) / 'day-test.jsonl'
        def run(*args):
            return subprocess.run([sys.executable, str(ROOT / "tools" / "day_gate.py"),
                                   "--log", str(log), *args],
                                  text=True, capture_output=True)
        self.assertEqual(run("post", "--date", "2026-11-06", "--unit", "vbt-d001").returncode, 0)
        self.assertEqual(run("post", "--date", "2026-11-06", "--unit", "vbt-d002").returncode, 0)
        st = json.loads(run("status").stdout)
        self.assertEqual(st["day_N"], 1)  # same day re-post keeps N
        self.assertEqual(st["posts"], 2)
        run("post", "--date", "2026-11-08", "--unit", "vbt-d003")
        st = json.loads(run("status").stdout)
        self.assertEqual(st["day_N"], 2)  # empty 11-07 never advances

    def test_c1_unit_invariants(self):
        u = json.loads((ROOT / "data" / "unit-vbt-d001.json").read_text(encoding="utf-8"))
        self.assertEqual(u["unit_id"], "vbt-d001")
        self.assertEqual(u["status"], "review")
        self.assertEqual(u['eligibility']['eligibility'], 'study')
        self.assertTrue(u["source_refs"])
        self.assertEqual(u["source_refs"][0]["locator"], "vbt-p03")
        # model never writes timings
        for s in u["steps"]:
            self.assertIsNone(s["seconds"])
        # technique marked R-gloss, never root text
        self.assertIn("R-gloss", u["technique_provenance"])
        # sha matches content
        body = {k: v for k, v in u.items() if k != "unit_sha256"}
        self.assertEqual(u["unit_sha256"], hashlib.sha256(
            json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest())
        # safety present
        self.assertTrue(u["safety"])

    def test_renderer_with_synthetic_sources(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'vbt').mkdir()
            (root / 'vbt/passages.jsonl').write_text(json.dumps({
                'locator': 'vbt-p03', 'verses': '22-31'}) + '\n')
            source = root / 'daily.json'
            source.write_text(json.dumps({'entries': [{'dharana': 2, 'verse': 24,
                'technique': 'synthetic gloss', 'upaya': '', 'trains': ''}]}))
            out = root / 'unit.json'
            r = subprocess.run([sys.executable, str(ROOT / 'tools' / 'syllabus_unit.py'),
                                '--dharana', '2', '--vbt', str(source), '--tw', str(root),
                                '--out', str(out)], text=True, capture_output=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            result = json.loads(out.read_text())
            self.assertEqual(result['source_refs'][0]['locator'], 'vbt-p03')
            self.assertEqual(result['status'], 'review')
            self.assertIn('NOT root text', result['technique_provenance'])

    def test_bodymap_drift_does_not_claim_source_validation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            san, db = root / 'sanskrithelp', root / 'deitybody'
            paths = [san / 'public/memory/data/matrika_body_map.json',
                     db / 'data/matrika_body_map.json', db / 'site/data/matrika_body_map.json']
            for path in paths:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('{"candidate": true}\n')
            env = os.environ.copy()
            env.update(SANSKRITHELP_CHECKOUT=str(san), DEITYBODY_CHECKOUT=str(db))
            cmd = [sys.executable, str(ROOT / 'tools/bodymap_check.py')]
            match = subprocess.run(cmd, env=env, text=True, capture_output=True)
            self.assertEqual(match.returncode, 0, match.stdout + match.stderr)
            self.assertIn('textual accuracy not checked', match.stdout)
            paths[-1].write_text('{"candidate": false}\n')
            self.assertNotEqual(subprocess.run(cmd, env=env, capture_output=True).returncode, 0)

    @unittest.skipUnless(available(PRACTICE / 'pilot-inputs/vbt-daily.json',
                                  TW / 'vbt/passages.jsonl'),
                         'external practice pilot and translation-work are unavailable')
    def test_external_renderer_for_another_mapped_unit(self):
        # This integration test needs the external source checkouts.
        with tempfile.TemporaryDirectory() as td:
            r = subprocess.run([sys.executable, str(ROOT / 'tools' / 'syllabus_unit.py'),
                                '--dharana', '2', '--vbt', str(PRACTICE / 'pilot-inputs/vbt-daily.json'),
                                '--tw', str(TW), '--out', str(Path(td) / 'unit.json')],
                               text=True, capture_output=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    @unittest.skipUnless(available(SAN / 'public/memory/data/matrika_body_map.json',
                                  DB / 'data/matrika_body_map.json',
                                  DB / 'site/data/matrika_body_map.json'),
                         'external body-map source is unavailable')
    def test_bodymap_one_truth(self):
        result = subprocess.run([sys.executable, str(ROOT / "tools" / "bodymap_check.py")],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('mirrors identical; textual accuracy not checked', result.stdout)


    def test_unit_to_syllabus_plug(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for eligibility, status in [('doable', 'approved'), ('study', 'review'),
                                        ('requires-diksha', 'review')]:
                unit = {'unit_id': 'synthetic', 'eligibility': {'eligibility': eligibility},
                        'status': status, 'steps': [{'text': 'draft technique'}],
                        'technique_R': 'draft technique'}
                src, out = root / 'unit.json', root / 'score.json'
                src.write_text(json.dumps(unit))
                r = subprocess.run([sys.executable, str(ROOT / 'tools' / 'unit_to_score.py'),
                                    '--unit', str(src), '--out', str(out)],
                                   text=True, capture_output=True)
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
                result = json.loads(out.read_text())
                self.assertEqual(result['steps'], [])
                self.assertEqual(result['gate']['mode'], 'STUDY')
                self.assertFalse(result['gate']['practice_authorized'])


if __name__ == "__main__":
    unittest.main()
