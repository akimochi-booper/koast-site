"""Build the public Pages directory from generated HTML and its public assets."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

SOURCE = Path(__file__).resolve().parents[1]
PAGE_DIRECTORIES = {"airports", "blog", "cities", "legal", "routes", "services", "terms", "wine-tours", "wineries"}
ASSET_DIRECTORIES = {"css", "fonts", "img", "preview"}
WELL_KNOWN_FILES = {"apple-app-site-association", "assetlinks.json", "security.txt"}
ASSET_TYPES = {".css", ".gif", ".html", ".ico", ".jpg", ".js", ".mjs", ".png", ".svg", ".txt", ".webp", ".woff2"}
ROOT_ASSETS = {
    "_headers", "_redirects", "favicon-v2.ico", "llms.txt", "robots.txt", "sitemap.xml", "site.webmanifest",
    "sw.js", "koast-acquisition.js", "koast-chat.js", "koast-chat-links.js", "koast-chat-photos.js",
    "koast-chat-voice.js", "marketing-design.js", "quote-request.js", "wine-controls.js", "wine-days.js",
}


def stage_pages(source, destination):
    source, destination = source.resolve(), destination.resolve()
    if destination.is_relative_to(source):
        raise ValueError("Pages output must be outside the source checkout.")
    destination.mkdir()  # An existing or stale output must never be published.
    for root, directories, files in os.walk(source):
        folder = Path(root)
        relative = folder.relative_to(source)
        if folder == source:
            directories[:] = [name for name in directories if name in PAGE_DIRECTORIES | ASSET_DIRECTORIES | {".well-known"}]
        elif relative.parts[0] == ".well-known":
            directories.clear()
        else:
            directories[:] = [name for name in directories if not name.startswith(".")]
        for name in directories:
            if (folder / name).is_symlink():
                raise ValueError(f"Unexpected link in public directory: {relative / name}")
        for name in files:
            if name.startswith("."):
                continue
            path = folder / name
            if folder == source:
                public = name in ROOT_ASSETS or path.suffix == ".html"
            elif relative.parts[0] == ".well-known":
                public = name in WELL_KNOWN_FILES
            elif relative.parts[0] in PAGE_DIRECTORIES:
                public = path.suffix == ".html"
            else:
                public = path.suffix.lower() in ASSET_TYPES
            if public:
                if path.is_symlink() or not path.is_file():
                    raise ValueError(f"Unexpected non-file public asset: {relative / name}")
                target = destination / relative / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, target)
    for required in ROOT_ASSETS | {"index.html", "404.html"}:
        if not (destination / required).is_file():
            raise ValueError(f"Missing public release file: {required}")


def validate(destination, today):
    stage_pages(SOURCE, destination)
    return subprocess.run([sys.executable, str(SOURCE / "scripts/check_site.py"),
                           "--site-root", str(destination), "--today", today]).returncode


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--today", required=True)
    args = parser.parse_args()
    output = os.environ.get("KOAST_PAGES_OUTPUT")
    if output:
        sys.exit(validate(Path(output), args.today))
    with TemporaryDirectory(prefix="koast-pages-") as directory:
        sys.exit(validate(Path(directory) / "site", args.today))
