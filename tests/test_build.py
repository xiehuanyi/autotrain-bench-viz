"""Integration checks for portable, isolated static builds."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class StaticBuildTests(unittest.TestCase):
    def test_isolated_build_preserves_sources_and_resolves_alias_data(self):
        sources = [ROOT / 'index.html', ROOT / 'rsi' / 'index.html', ROOT / 'rsi' / 'data.json']
        before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'site with spaces'
            subprocess.run([sys.executable, str(ROOT / 'tools' / 'build_rsi.py'),
                            '--output-dir', str(output)], cwd=directory,
                           check=True, capture_output=True, text=True)
            self.assertEqual({p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()},
                             {'.nojekyll', 'index.html', 'rsi/index.html', 'rsi/data.json'})
            self.assertEqual(json.loads((output / 'rsi' / 'data.json').read_text()),
                             json.loads((ROOT / 'rsi' / 'data.json').read_text()))
            for page, expected_data in [('index.html', 'rsi/data.json'), ('rsi/index.html', 'data.json')]:
                html = (output / page).read_text()
                self.assertIn(f'href="{expected_data}"', html)
                self.assertNotIn('__RSI_DATA__', html)
                self.assertNotIn('__I18N_DATA__', html)
                self.assertNotIn('__DATA_URL__', html)
            self.assertEqual((output / 'index.html').read_bytes(), (ROOT / 'index.html').read_bytes())
        self.assertEqual(before, {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in sources})


if __name__ == '__main__':
    unittest.main()
