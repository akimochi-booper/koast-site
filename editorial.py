"""Validated, dated editorial content for the static Koast site."""
from datetime import date
from pathlib import Path
import json
import re

CATEGORIES = {"City Events", "Airport Guides", "City Guides", "Wine Country", "Trips", "Corporate", "Industry"}

def load_posts(root):
    posts = []
    for path in sorted((Path(root) / "content" / "posts").glob("*.json")):
        post = json.loads(path.read_text(encoding="utf-8"))
        required = ("slug", "title", "description", "category", "image", "minutes", "published", "modified", "body", "cta")
        if any(not post.get(key) for key in required):
            raise ValueError(f"{path}: missing required editorial field")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", post["slug"]) or path.stem != post["slug"]:
            raise ValueError(f"{path}: invalid or mismatched slug")
        if post["category"] not in CATEGORIES:
            raise ValueError(f"{path}: unknown category")
        if any(char in post[key] for key in ("title", "description", "category", "image", "cta") for char in ('<', '>', '"')):
            raise ValueError(f"{path}: metadata must be plain text without HTML quotes")
        published = date.fromisoformat(post["published"])
        modified = date.fromisoformat(post["modified"])
        if modified < published:
            raise ValueError(f"{path}: modified date predates publication")
        if not isinstance(post["minutes"], int) or post["minutes"] < 1:
            raise ValueError(f"{path}: invalid read time")
        image = Path(post["image"])
        if image.name != post["image"] or not (Path(root)/"img"/image).is_file():
            raise ValueError(f"{path}: missing image")
        if re.search(r"<\s*(script|iframe|form|h1)\b|\bon[a-z]+\s*=|javascript:", post["body"], re.I):
            raise ValueError(f"{path}: unsupported active content or duplicate h1")
        posts.append(post)
    return sorted(posts, key=lambda p: (p["published"], p["slug"]), reverse=True)

def display_date(value):
    parsed = date.fromisoformat(value)
    return f"{parsed.strftime('%B')} {parsed.day}, {parsed.year}"
