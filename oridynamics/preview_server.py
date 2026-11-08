#!/usr/bin/env python3
"""Local-only homepage preview with single byte-range support for video seeking."""
import argparse
import os
import re
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener


class RangeHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('X-OriDynamic-Preview', 'range-v1')
        super().end_headers()

    def send_head(self):
        self.range_remaining = None
        path = self.translate_path(self.path)
        match = re.fullmatch(r'bytes=(\d*)-(\d*)', self.headers.get('Range', '').strip())
        if not match or not any(match.groups()) or not os.path.isfile(path):
            return super().send_head()
        try:
            source = open(path, 'rb')
        except OSError:
            self.send_error(404, 'File not found')
            return None
        stat = os.fstat(source.fileno())
        modified = self.date_time_string(stat.st_mtime)
        if self.headers.get('If-Range') not in (None, modified):
            source.close()
            return super().send_head()
        size = stat.st_size
        first, last = match.groups()
        start = int(first) if first else max(0, size - int(last))
        end = min(int(last), size - 1) if first and last else size - 1
        if start >= size or start > end:
            source.close()
            self.send_response(416)
            self.send_header('Content-Range', f'bytes */{size}')
            self.send_header('Content-Length', '0')
            self.end_headers()
            return None
        source.seek(start)
        self.range_remaining = end - start + 1
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(path))
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length', str(self.range_remaining))
        self.send_header('Last-Modified', modified)
        self.end_headers()
        return source

    def copyfile(self, source, outputfile):
        try:
            if self.range_remaining is None:
                return super().copyfile(source, outputfile)
            remaining = self.range_remaining
            while remaining:
                chunk = source.read(min(64 * 1024, remaining))
                if not chunk:
                    break
                outputfile.write(chunk)
                remaining -= len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            pass  # Browsers cancel old range requests when the user seeks again.


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=4187)
    parser.add_argument('--directory', type=Path, default=Path(__file__).resolve().parent / 'dist')
    parser.add_argument('--open', action='store_true', dest='open_browser')
    args = parser.parse_args()
    root = args.directory.resolve()
    url = f'http://localhost:{args.port}/'
    try:
        with build_opener(ProxyHandler({})).open(url + 'index.html', timeout=2) as response:
            current = response.read()
            supports_ranges = response.headers.get('X-OriDynamic-Preview') == 'range-v1'
    except (URLError, OSError):
        current = None
    if current is not None:
        if current == (root / 'index.html').read_bytes() and supports_ranges:
            print('Preview is already running: ' + url, flush=True)
            if args.open_browser:
                webbrowser.open(url)
        else:
            print(f'Port {args.port} is occupied by another or older preview. Stop that server first.', flush=True)
        return
    handler = partial(RangeHandler, directory=str(root))
    with ThreadingHTTPServer(('127.0.0.1', args.port), handler) as server:
        print('OriDynamic preview with video seeking: ' + url, flush=True)
        if args.open_browser:
            webbrowser.open(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print('\nPreview stopped.')


if __name__ == '__main__':
    main()
