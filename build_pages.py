#!/usr/bin/env python3
"""Build project homepages and package their referenced files for GitHub Pages."""
from html.parser import HTMLParser
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / '_site'
BASE_URL = os.environ.get('PAGES_BASE_URL', 'https://lg-frontierai.github.io/homepage').rstrip('/') + '/'
PROJECTS = ('oridynamics',)


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ('src', 'href', 'xlink:href', 'poster', 'data-figure'):
            if attrs.get(key):
                self.urls.append(attrs[key])
        if tag == 'meta' and attrs.get('property') == 'og:image':
            self.urls.append(attrs.get('content', ''))
        if attrs.get('srcset'):
            self.urls.extend(item.strip().split()[0] for item in attrs['srcset'].split(',') if item.strip())


def referenced_files(dist, site_url):
    base = urlsplit(site_url)
    pending = ['index.html', '.nojekyll', 'robots.txt', 'sitemap.xml']
    found = set()
    while pending:
        name = pending.pop()
        if name in found:
            continue
        path = dist / name
        if not path.resolve().is_relative_to(dist.resolve()) or path.is_symlink():
            raise ValueError(f'Invalid site asset: {name}')
        if not path.is_file():
            raise FileNotFoundError(f'Missing site asset: {name}')
        found.add(name)
        if path.suffix.lower() not in ('.html', '.css', '.svg'):
            continue
        text = path.read_text()
        refs = References()
        if path.suffix.lower() != '.css':
            refs.feed(text)
        refs.urls.extend(re.findall(r'url\(\s*[\'\"]?([^\)\'\"]+)[\'\"]?\s*\)', text))
        for ref in refs.urls:
            if not ref or ref.startswith('#'):
                continue
            url = urlsplit(urljoin(site_url + name, ref))
            if url.scheme not in ('http', 'https') or url.netloc != base.netloc:
                continue
            if not url.path.startswith(base.path):
                raise ValueError(f'Asset escapes the project URL: {ref}')
            relative = unquote(url.path[len(base.path):])
            if not relative or relative.endswith('/'):
                relative += 'index.html'
            pending.append(relative)
    return sorted(found)


def main():
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    shutil.copy2(ROOT / 'index.html', OUTPUT / 'index.html')
    (OUTPUT / '.nojekyll').touch()
    # Keep old bookmarks working without publishing the retired project assets.
    legacy = OUTPUT / 'oridynamic'
    legacy.mkdir()
    (legacy / 'index.html').write_text("""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>OriDynamics</title><meta http-equiv="refresh" content="0;url=../oridynamics/">
<script>location.replace('../oridynamics/' + location.search + location.hash);</script>
</head><body><a href="../oridynamics/">Continue to OriDynamics</a></body></html>""")
    for project in PROJECTS:
        source = ROOT / project
        site_url = urljoin(BASE_URL, project + '/')
        env = dict(os.environ, SITE_URL=site_url)
        subprocess.run([sys.executable, str(source / 'build.py')], env=env, check=True)
        files = referenced_files(source / 'dist', site_url)
        for name in files:
            target = OUTPUT / project / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / 'dist' / name, target)
        print(f'{project}: {len(files)} validated files -> {site_url}', flush=True)


if __name__ == '__main__':
    main()
