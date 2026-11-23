import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from stage_pages import ROOT_ASSETS, stage_pages


class PagesPackageTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.source = Path(temp.name) / "source"
        self.output = Path(temp.name) / "public"
        self.source.mkdir()
        for name in ROOT_ASSETS | {"index.html", "404.html"}:
            self.write(name)

    def write(self, name):
        path = self.source / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(name.encode())

    def test_exact_public_files_and_bytes(self):
        public = {"blog/example.html", "preview/motion/index.html", "preview/motion/player.mjs",
                  "preview/motion/assets/frame.gif", "img/icons/LICENSE.txt", "fonts/OFL.txt",
                  ".well-known/apple-app-site-association", ".well-known/assetlinks.json", ".well-known/security.txt"}
        internal = {"preview/motion/PROMPTS.md", "fonts/README.md", "docs/sample.html",
                    "content/legal/example.inc", "workers/chat/worker.js", ".git/config",
                    ".codex/config.toml", "dist/previous.html", "preview/.hidden/example.html",
                    "scripts/build.js", "private.js", ".well-known/notes.txt", ".well-known/.env",
                    ".well-known/private/assetlinks.json"}
        for name in public | internal:
            self.write(name)
        stage_pages(self.source, self.output)
        actual = {p.relative_to(self.output).as_posix(): p.read_bytes()
                  for p in self.output.rglob("*") if p.is_file()}
        expected = ROOT_ASSETS | public | {"index.html", "404.html"}
        self.assertEqual(actual, {name: name.encode() for name in expected})

    def test_missing_generated_file_fails(self):
        (self.source / "_redirects").unlink()
        with self.assertRaisesRegex(ValueError, "_redirects"):
            stage_pages(self.source, self.output)

    def test_existing_output_and_in_tree_output_fail(self):
        self.output.mkdir()
        with self.assertRaises(FileExistsError):
            stage_pages(self.source, self.output)
        with self.assertRaisesRegex(ValueError, "outside"):
            stage_pages(self.source, self.source / "dist")
