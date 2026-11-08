#!/usr/bin/env python3
"""Generate the English, paper-style OriDynamics homepage. Standard library only."""
import json
import base64
import os
import textwrap
from hashlib import sha256
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent
SITE_URL = os.environ.get('SITE_URL', 'https://lg-frontierai.github.io/homepage/oridynamics/').rstrip('/') + '/'
DATA = json.loads((ROOT / 'content.json').read_text())
SITE_GROUP = 'LGLab Frontier AI Group'
OUT = ROOT / 'dist'
OUT.mkdir(exist_ok=True)
CSS_VERSION = sha256((OUT / 'site.css').read_bytes()).hexdigest()[:12]
JS_VERSION = sha256((OUT / 'site.js').read_bytes()).hexdigest()[:12]
VIDEO = json.loads((ROOT / 'video-manifest.json').read_text())
def versioned_asset(path):
    return escape(path + '?v=' + sha256((OUT / path).read_bytes()).hexdigest()[:12], quote=True)

VIDEO_URL = versioned_asset(VIDEO['asset'])
VIDEO_POSTER_URL = versioned_asset(VIDEO['poster']['asset'])
MUSIC = VIDEO['music']
music_credit = (
    f'Music: “<a href="{escape(MUSIC["source"], quote=True)}" target="_blank" rel="noopener">{escape(MUSIC["title"])}</a>” '
    f'by <a href="{escape(MUSIC["artist_url"], quote=True)}" target="_blank" rel="noopener">{escape(MUSIC["artist"])}</a> · '
    f'<a href="{escape(MUSIC["license_url"], quote=True)}" target="_blank" rel="noopener">{escape(MUSIC["license"])}</a>. '
    f'{escape(MUSIC["modifications"])}'
)
(OUT / 'video-music-credits.txt').write_text((ROOT / 'video-music-credits.txt').read_text())

def icon(name):
    resource_icons = {'paper': 'file-pdf.svg', 'code': 'github.svg'}
    if name in resource_icons:
        svg = (ROOT / 'icons' / resource_icons[name]).read_text().strip()
        return svg.replace('<svg ', '<svg fill="currentColor" stroke="none" aria-hidden="true" focusable="false" ', 1)
    paths = {
        'expand': '<path d="M8 3H3v5m13-5h5v5M3 16v5h5m13-5v5h-5"/>',
        'copy': '<rect x="8" y="8" width="12" height="13" rx="2"/><path d="M15 8V3H3v13h5"/>',
        'close': '<path d="m6 6 12 12M18 6 6 18"/>',
        'play': '<path d="m8 5 11 7-11 7Z" fill="currentColor" stroke="none"/>',
        'pause': '<path d="M8 5v14M16 5v14" stroke-width="3"/>',
        'book': '<path d="M12 5v16M12 5C8 2 4 3 2 4v15c3-1 7-1 10 2 3-3 7-3 10-2V4c-2-1-6-2-10 1Z"/>',
    }
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true">{paths[name]}</svg>'

FIGURES = json.loads((ROOT / 'figure-manifest.json').read_text())
DIMENSIONS = {item['file']: tuple(item['dimensions']) for item in FIGURES['assets']}

# Replace only the presentation label; all scientific plot pixels stay intact.
if 'performance_axis_label' in FIGURES:
    label = FIGURES['performance_axis_label']
    source_width, source_height = DIMENSIONS[label['source']]
    source_data = base64.b64encode((OUT / 'assets' / label['source']).read_bytes()).decode('ascii')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{source_width}" height="{source_height}" viewBox="0 0 {source_width} {source_height}">
<title>OriDynamics overall performance — Z-score</title>
<image width="{source_width}" height="{source_height}" href="data:image/png;base64,{source_data}"/>
<rect x="25" y="310" width="65" height="290" fill="white"/>
<text x="60" y="453" transform="rotate(-90 60 453)" text-anchor="middle" dominant-baseline="central" font-family="Arial, Helvetica, sans-serif" font-size="44" fill="#4c3f6d">{escape(label['text'])}</text>
</svg>'''
    (OUT / 'assets' / label['output']).write_text(svg)
    DIMENSIONS[label['output']] = (source_width, source_height)

def figure(file, title, caption, eager=False, caption_heading=True):
    width,height=DIMENSIONS[file]
    image_url=versioned_asset(f'assets/{file}')
    heading=f'<strong>{escape(title)}.</strong> ' if caption_heading else ''
    return f'''<figure class="research-figure">
      <button class="figure-button" type="button" data-figure="{image_url}" data-title="{escape(title,quote=True)}" aria-label="Enlarge {escape(title,quote=True)}">
        <img src="{image_url}" width="{width}" height="{height}" alt="{escape(caption,quote=True)}" loading="{'eager' if eager else 'lazy'}" decoding="async" {'fetchpriority="high"' if eager else ''}>
        <span class="enlarge">{icon('expand')} View full size</span>
      </button>
      <figcaption>{heading}{caption}</figcaption>
    </figure>'''

def contributor(author):
    marks = [str(n) for n in author['affiliations']]
    if author.get('equal_contribution'):
        marks.append('*')
    if author.get('corresponding_author'):
        marks.append('†')
    return f'<span>{escape(author["name"])}<sup>{",".join(marks)}</sup></span>'

authors = DATA['authors_in_contributor_order']
# Keep Peicong Lin and Shuangjia Zheng together on their own line.
assert [a['name'] for a in authors[-2:]] == ['Peicong Lin', 'Shuangjia Zheng']
contributors = ', '.join(contributor(a) for a in authors[:-2])
contributors += ', <span class="author-pair">' + ', '.join(contributor(a) for a in authors[-2:]) + '</span>'
author_notes=[]
if any(a.get('equal_contribution') for a in DATA['authors_in_contributor_order']):
    author_notes.append('* Equal contribution')
if any(a.get('corresponding_author') for a in DATA['authors_in_contributor_order']):
    author_notes.append('† Corresponding authors')
author_note=' &nbsp; · &nbsp; '.join(author_notes)
affiliations=''.join(f'<span><sup>{n}</sup>{v}</span>' for n,v in DATA['affiliations'].items())
highlights=''.join(f'<li><strong>{escape(h["en_title"])}</strong><p>{escape(h["en"])}</p></li>' for h in DATA['highlights'])

overview=figure(FIGURES['homepage_figures']['overview'],'OriDynamics overview',
    'OriDynamics generates all-atom conformational ensembles across protein monomers, protein–ligand complexes and protein–protein assemblies within a unified framework.',caption_heading=False)

# Display the latest supplied figures in full, with the same assets used for zoom.
benchmark_html = figure(FIGURES['homepage_figures']['performance'], 'OriDynamics overall performance',
    'OriDynamics captures conformational dynamics across monomers, protein–ligand complexes, and protein–protein assemblies. It achieves leading overall performance among evaluated methods while reproducing key patterns of flexibility and interaction-site dynamics observed in molecular dynamics simulations.', caption_heading=False)

APPLICATION_CASES = json.loads((ROOT / 'application-cases.json').read_text())
CASE_EXPLANATIONS = json.loads((ROOT / 'case-explanations.json').read_text())
CASE_STRUCTURES = json.loads((ROOT / 'case-structure-map.json').read_text())['cases']
assert {case['id'] for case in APPLICATION_CASES} <= set(CASE_STRUCTURES)

def case_explanation(item):
    slug = item['id']
    data = CASE_EXPLANATIONS[slug]
    def citations(numbers):
        assert all(1 <= n <= len(data['references']) for n in numbers), f'Invalid reference in {slug}'
        return ''.join(f'<a class="case-ref-link" href="#case-ref-{slug}-{n}" aria-label="Reference {n}">[{n}]</a>' for n in numbers)
    structure = CASE_STRUCTURES[slug]
    allowed_pdbs = {entry['pdb'] for key in ('primary', 'supplementary') for entry in structure[key]}
    for ref in data['references']:
        kind = ref.get('kind', 'structure')
        assert kind in ('structure', 'dataset', 'current-work'), f'Unknown reference kind in {slug}'
        if kind == 'structure':
            assert ref.get('pdb_ids') and set(ref['pdb_ids']) <= allowed_pdbs, f'Reference outside approved PDB scope in {slug}'
        else:
            assert not ref.get('pdb_ids'), f'Non-structural reference must not assign PDB identities in {slug}'
        if ref['url'].startswith('https://www.rcsb.org/structure/'):
            assert kind == 'structure' and ref['url'].rsplit('/', 1)[-1] in ref['pdb_ids'], f'PDB reference mismatch in {slug}'
    structure_groups = []
    for key, label in [('primary', 'Primary PDB structures'), ('supplementary', 'Supplementary structural context')]:
        if structure[key]:
            entries = []
            for entry in structure[key]:
                pdb = entry['pdb']
                assert len(pdb) == 4 and pdb.isalnum() and pdb == pdb.upper()
                entries.append(f'<li><a class="case-pdb-id" href="https://www.rcsb.org/structure/{pdb}" target="_blank" rel="noopener">{pdb} ↗</a> <span>{escape(entry["description"])} {citations(entry["refs"])}</span></li>')
            structure_groups.append(f'<div class="case-pdb-group"><h4>{label}</h4><ul>{"".join(entries)}</ul></div>')
    steps = ''.join(f'<li><strong>{escape(step["title"])}</strong><p>{escape(step["text"])} {citations(step.get("refs", []))}</p></li>' for step in data['steps'])
    reading = ''.join(f'<p><strong>{escape(part["title"])}.</strong> {escape(part["text"])} {citations(part.get("refs", []))}</p>' for part in data['reading'])
    refs = ''.join(f'<li id="case-ref-{slug}-{n}" tabindex="-1"><a href="{escape(ref["url"], quote=True)}" target="_blank" rel="noopener">{escape(ref["label"])} ↗</a><p>{escape(ref["detail"])}</p></li>' for n, ref in enumerate(data['references'], 1))
    return f'''<template id="case-notes-{slug}">
      <section class="case-notes-section case-structure-context"><h3>Structures used in this case</h3>{''.join(structure_groups)}<p class="case-structure-note">{escape(structure['note'])}</p></section>
      <section class="case-notes-section"><h3>Biological role</h3><p>{escape(data['overview'])} {citations(data['overview_refs'])}</p></section>
      <section class="case-notes-section"><h3>Mechanism in brief</h3><ol class="case-mechanism-steps">{steps}</ol></section>
      <section class="case-notes-section case-reading"><h3>Reading this case</h3>{reading}<p class="case-interpretation"><strong>How to interpret the animation.</strong> {escape(data['interpretation'])}</p></section>
      <section class="case-notes-section"><h3>References</h3><ol class="case-reference-list">{refs}</ol></section>
    </template>'''

def application_composite(parts):
    # Reposition intact scientific subpanels on a shared 1200 x 900 canvas.
    panels = []
    for part in parts:
        x, y, width, height = part['source']
        bx, by, bw, bh = part['box']
        scale = min(bw / width, bh / height)
        pw, ph = width * scale, height * scale
        left, top = bx + (bw - pw) / 2, by + (bh - ph) / 2
        style = (f'left:{left/12:.8f}%;top:{top/9:.8f}%;width:{pw/12:.8f}%;height:{ph/9:.8f}%;'
                 f'--crop-width:{2600/width*100:.8f}%;--crop-left:{-x/width*100:.8f}%;--crop-top:{-y/height*100:.8f}%')
        panels.append(f'<span class="figure-crop" style="{style}"><img src="assets/applications.webp" width="2600" height="3260" alt="{escape(part["label"], quote=True)}" loading="lazy" decoding="async"></span>')
    return '<span class="application-composite">' + ''.join(panels) + '</span>'

def application_crop(label, x, y, width, height, case_frame=False, parts=None):
    # Display exact regions of the original scientific figure without resampling it.
    crop_style = (f'--crop-ratio:{width}/{height};--crop-width:{2600/width*100:.8f}%;'
                  f'--crop-left:{-x/width*100:.8f}%;--crop-top:{-y/height*100:.8f}%')
    image = f'<img src="assets/applications.webp" width="2600" height="3260" alt="{escape(label,quote=True)}" loading="lazy" decoding="async">'
    frame_class = 'application-figure-frame' if case_frame else 'figure-crop'
    if parts:
        image = application_composite(parts)
    elif case_frame:
        fit_width = min(100, width / height * 75)
        image = f'<span class="figure-crop" style="{crop_style};width:{fit_width:.8f}%">{image}</span>'
    return f'''<button class="figure-button {frame_class}" type="button" data-figure="assets/applications.webp" data-crop="{crop_style}" data-title="{escape(label,quote=True)}" style="{crop_style}" aria-label="Enlarge {escape(label,quote=True)}">
      {image}
      <span class="enlarge">{icon('expand')} View full size</span>
    </button>'''

def application_case(item):
    slug = item['id']
    label = escape(item['label'])
    heading = escape(item.get('heading', item['label']))
    subtitle = f'<p class="application-case-subtitle">{escape(item["subtitle"])}</p>' if item.get('subtitle') else ''
    if item.get('figure_asset'):
        figure_file = item['figure_asset']
        figure_url = escape(figure_file + '?v=' + sha256((OUT / figure_file).read_bytes()).hexdigest()[:12], quote=True)
        figure_title = escape(item['figure_label'], quote=True)
        left = f'''<button class="figure-button application-figure-frame" type="button" data-figure="{figure_url}" data-title="{figure_title}" aria-label="Enlarge {figure_title}">
          <img src="{figure_url}" width="1200" height="900" alt="{figure_title}" loading="lazy" decoding="async">
          <span class="enlarge">{icon('expand')} View full size</span>
        </button>'''
    elif item.get('figure_region'):
        left = application_crop(item['figure_label'], *item['figure_region'], case_frame=True, parts=item.get('figure_parts'))
    else:
        left = '<div class="application-figure-placeholder" aria-label="Figure to be added"><span>Figure to be added</span></div>'
    width = int(float(item['metadata']['width']))
    height = int(float(item['metadata']['height']))
    duration = float(item['metadata']['duration'])
    duration_seconds = round(duration)
    duration_label = f'{duration_seconds // 60}:{duration_seconds % 60:02d}'
    media_url = escape(item['asset'] + '?v=' + item['sha256'][:12], quote=True)
    preview_file = item.get('preview', item['poster'])
    preview_url = escape(preview_file + '?v=' + sha256((OUT / preview_file).read_bytes()).hexdigest()[:12], quote=True)
    cx, cy, cw, ch = item.get('cover_region', [240, 155, 960, 720])
    preview_style = f'--preview-width:{1440/cw*100:.6f}%;--preview-left:{-cx/cw*100:.6f}%;--preview-top:{-cy/ch*100:.6f}%'
    return f'''<section class="application-case" id="case-{slug}" aria-labelledby="case-{slug}-title">
      <header class="application-case-heading">
        <h4 class="application-case-title" id="case-{slug}-title">{heading}</h4>
        {subtitle}
      </header>
      <div class="application-media-row">
        <div class="application-figure-column">
          <div class="application-case-figure">{left}</div>
          <button type="button" class="case-notes-trigger" data-case-notes="{slug}" aria-haspopup="dialog" aria-controls="case-notes-dialog" aria-expanded="false" aria-label="Mechanism and references for {heading}">{icon('book')}<span>Mechanism &amp; references</span><span aria-hidden="true">↗</span></button>
        </div>
        <div class="application-player" data-label="{label}">
        <div class="application-stage">
        <video class="application-video" id="{slug}-application-video" data-duration="{duration:g}" controls muted loop playsinline preload="metadata" width="{width}" height="{height}" style="--video-ratio:{width}/{height}" poster="{preview_url}" aria-label="{label} application video" aria-describedby="{slug}-video-note">
          <source src="{media_url}" type="video/mp4">
          Your browser does not support embedded video. <a href="{escape(item['asset'],quote=True)}">Open the {label} video</a>.
        </video>
        <button type="button" class="application-preview" style="{preview_style}" aria-label="Play {label} video preview" hidden>
          <img src="{preview_url}" width="1440" height="1080" alt="" loading="lazy" decoding="async">
          <span class="preview-play">{icon('play')}<span>Play video</span><span class="preview-duration">{duration_label}</span></span>
        </button>
        </div>
        <p class="application-video-note" id="{slug}-video-note">Conformational visualization only. Not a time-resolved trajectory.</p>
        <div class="application-controls" role="group" aria-label="{label} playback controls" hidden>
          <button type="button" data-play aria-label="Play {label} video" title="Play"><span data-play-icon>{icon('play')}</span><span data-pause-icon hidden>{icon('pause')}</span></button>
          <span class="application-time" data-time>0:00 / {duration_label}</span>
          <input type="range" data-seek min="0" max="{duration:g}" step="0.1" value="0" aria-label="Seek {label} video" disabled>
          <button type="button" data-fullscreen aria-label="Full screen {label} video" title="Full screen">{icon('expand')}</button>
        </div>
        <p class="application-playback-status" role="status" hidden>Unable to play this video. <a href="{escape(item['asset'],quote=True)}" target="_blank" rel="noopener">Open video</a></p>
        </div>
      </div>
    </section>'''

application_html=f'''<article class="result-block application-group">
  <h3>Alternative states and partner-dependent responses</h3>
  <figure class="research-figure application-summary">
    {application_crop('Alternative-state recovery benchmarks, panels a and b',0,0,2600,650)}
    <figcaption>OriDynamics recovers alternative experimental conformations and structural responses to ligand or protein partners across ConforMix and ProMiSE.</figcaption>
  </figure>
  {''.join(application_case(item) for item in APPLICATION_CASES)}
</article>'''

# Keep given-name-first spelling and author order consistent with the header.
bib_names = [author['name'] for author in authors]
bib_author_lines = [' and '.join(bib_names[i:i + 3]) for i in range(0, len(bib_names), 3)]
bib_authors = ' and\n            '.join(bib_author_lines)
bib_title = textwrap.fill(
    DATA['title'].replace('OriDynamics', '{OriDynamics}'),
    width=78, initial_indent='  title = {', subsequent_indent='           ',
    break_long_words=False, break_on_hyphens=False,
) + '},'
bib='''@unpublished{oridynamic2026,
TITLE_FIELD
  author = {AUTHOR_LIST},
  year = {2026},
  note = {Manuscript, November 2026}
}'''.replace('TITLE_FIELD', bib_title).replace('AUTHOR_LIST', bib_authors)
heading_parts = DATA.get('homepage_title', DATA['title']).split(' through ', 1)
if len(heading_parts) == 2:
    heading_parts[1] = 'through ' + heading_parts[1]
heading_html = ' '.join(f'<span class="title-line">{escape(part)}</span>' for part in heading_parts)
html=f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(DATA['title'])}</title>
<meta name="description" content="{escape(DATA['suggested_hero']['description_en'],quote=True)}">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="website"><meta property="og:title" content="{escape(DATA['title'],quote=True)}">
<meta property="og:description" content="{escape(DATA['suggested_hero']['description_en'],quote=True)}">
<meta property="og:image" content="{escape(SITE_URL, quote=True)}assets/social-preview.png">
<meta property="og:url" content="{escape(SITE_URL, quote=True)}">
<link rel="canonical" href="{escape(SITE_URL, quote=True)}">
<link rel="icon" href="favicon.ico?v=oridynamic-v6-1" sizes="16x16 24x24 32x32 48x48 64x64 128x128 256x256">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png?v=oridynamic-v6-1">
<link rel="icon" type="image/png" sizes="192x192" href="assets/favicon-192.png?v=oridynamic-v6-1">
<link rel="icon" type="image/svg+xml" sizes="any" href="{versioned_asset('assets/favicon-oridynamic-v6.svg')}">
<link rel="apple-touch-icon" sizes="180x180" href="assets/favicon-180.png?v=oridynamic-v6-1">
<link rel="stylesheet" href="site.css?v={CSS_VERSION}"><script src="site.js?v={JS_VERSION}" defer></script>
</head><body>
<div class="ambient-background" aria-hidden="true">
  <div class="ambient-wing ambient-left"></div>
  <div class="ambient-wing ambient-right"></div>
</div>
<a class="skip-link" href="#video">Skip to the video</a>
<main>
<div class="intro-screen" id="top">
<header class="paper-header"><div class="container">
  <a class="wordmark" href="#top" aria-label="OriDynamics home"><img src="{versioned_asset('assets/oridynamics-logo.png')}" alt="OriDynamics" width="2037" height="772" decoding="async"></a>
  <h1>{heading_html}</h1>
  <p class="contributors">{contributors}</p>
  <div class="affiliation-block">
    <div class="affiliations">{affiliations}</div>
    <p class="author-note">{author_note}</p>
  </div>
  <div class="paper-links">
    <button class="pill" type="button" disabled title="Link will be available later">{icon('paper')}<span>Technical Report</span></button>
    <a class="pill" href="https://github.com/LG-FrontierAI/oridynamics" target="_blank" rel="noopener noreferrer">{icon('code')}<span>Github Code</span></a>
  </div>
  <p class="hero-slogan"><span>Understanding biomolecular dynamics</span>
    <span>is a key step toward biological intelligence.</span></p>
</div></header>
</div>

<section class="video-section reading-width" id="video" aria-label="Project video">
  <figure class="video-figure">
    <div class="video-frame">
      <video id="project-video" controls playsinline loop preload="metadata" width="{VIDEO['dimensions'][0]}" height="{VIDEO['dimensions'][1]}" poster="{VIDEO_POSTER_URL}" aria-label="{escape(VIDEO['title'], quote=True)}" aria-describedby="video-music-credit">
        <source src="{VIDEO_URL}" type="video/mp4">
        Your browser does not support embedded video. <a href="{VIDEO_URL}">Open the MP4 video</a>.
      </video>
    </div>
    <figcaption id="video-music-credit" class="video-music-credit">{music_credit}</figcaption>
  </figure>
</section>

<section class="section section-soft" id="abstract"><div class="reading-width">
  <h2>Abstract</h2><p class="abstract-text">{escape(DATA['homepage_abstract']['en'])}</p>
</div></section>

<section class="overview-section reading-width" id="overview" aria-labelledby="overview-title">
  <h2 id="overview-title">Overview</h2>
  {overview}
</section>

<section class="section" id="highlights"><div class="reading-width">
  <h2>Highlights</h2><ul class="highlights">{highlights}</ul>
</div></section>

<section class="section" id="performance"><div class="container">
  <h2>Performance</h2>
  {benchmark_html}
</div></section>

<section class="section section-soft" id="applications"><div class="container">
  <h2>Applications</h2>
  {application_html}
</div></section>

<section class="section citation-section" id="citation"><div class="reading-width">
  <h2 class="citation-title">Citation</h2>
  <div class="citation-box"><button type="button" id="copy-citation">{icon('copy')} <span>Copy BibTeX</span></button><pre id="citation-text">{escape(bib)}</pre><p id="copy-status" role="status" aria-live="polite"></p></div>
</div></section>
</main>
<footer><div class="reading-width"><a class="footer-top" href="#top">Back to top ↑</a><p>© 2026 {SITE_GROUP} · OriDynamics</p><p>Figures from the manuscript and project materials, updated November 2026.</p><p class="design-credit">Layout inspired by the <a href="https://odesign1.github.io/" target="_blank" rel="noopener">ODesign project page</a>.</p><p class="media-credit">{music_credit} <a href="video-music-credits.txt" target="_blank" rel="noopener">Music credits</a></p></div></footer>
<dialog id="figure-dialog" aria-labelledby="dialog-caption"><div class="dialog-toolbar"><h2 id="dialog-caption"></h2><a id="original-figure" href="{versioned_asset('assets/' + FIGURES['homepage_figures']['overview'])}" target="_blank" rel="noopener">Open image ↗</a><button type="button" id="close-dialog" aria-label="Close figure">{icon('close')}</button></div><div class="dialog-image"><div id="dialog-crop"><img id="dialog-img" alt=""></div></div></dialog>
<dialog id="case-notes-dialog" class="case-notes-dialog" aria-labelledby="case-notes-title">
  <div class="case-notes-toolbar">
    <p>Mechanism &amp; references</p>
    <div class="case-notes-actions">
      <div class="case-text-zoom" role="group" aria-label="Reading text size">
        <button type="button" data-notes-smaller aria-label="Decrease text size">A−</button>
        <output data-notes-zoom aria-live="polite" aria-label="Text size">100%</output>
        <button type="button" data-notes-larger aria-label="Increase text size">A+</button>
      </div>
      <button type="button" data-notes-expand aria-label="Expand reading window" aria-pressed="false" title="Expand reading window">{icon('expand')}</button>
      <button type="button" data-notes-close aria-label="Close case introduction" title="Close" autofocus>{icon('close')}</button>
    </div>
  </div>
  <div class="case-notes-scroll" tabindex="0" aria-label="Case introduction and references">
    <header class="case-notes-intro"><p class="case-notes-label"></p><h2 id="case-notes-title"></h2><p class="case-notes-topic"></p></header>
    <div class="case-notes-content"></div>
  </div>
</dialog>
{''.join(case_explanation(item) for item in APPLICATION_CASES)}
</body></html>'''
(OUT/'index.html').write_text(html)
(OUT/'.nojekyll').write_text('')
(OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n')
(OUT/'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{escape(SITE_URL)}</loc></url></urlset>\n')
print('Built English homepage: dist/index.html')
