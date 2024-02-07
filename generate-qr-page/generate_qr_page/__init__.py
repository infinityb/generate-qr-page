#!/usr/bin/env python
import sys
import random
import base64
import io
import qrcode
import subprocess
import tempfile

xcoords = [20.690037, 282.12363, 543.55719]
ycoords = [52.206642, 148.19803, 244.18942, 340.18082, 436.17221, 532.16357, 628.15497, 724.14636, 820.13776, 916.12915]
panel_height=83.12915

preamble = """<!DOCTYPE html>
<html>
<head>
<style>
body {
    margin: 0;
    padding: 0;
}
@media print {
    @page {
        size: letter portrait;
        margin: 0;
        padding: 0;
    }
}</style>
</head><body>
<svg
   width="100%"
   height="100%"
   viewBox="0 0 816 1056"
   version="1.1"
   id="svg1"
   xml:space="preserve"
   inkscape:version="1.3.2 (091e20e, 2023-11-25, custom)"
   sodipodi:docname="drawing.svg"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg"><sodipodi:namedview
     id="namedview1"
     pagecolor="#ffffff"
     bordercolor="#000000"
     borderopacity="0.25"
     inkscape:showpageshadow="2"
     inkscape:pageopacity="0.0"
     inkscape:pagecheckerboard="0"
     inkscape:deskcolor="#d1d1d1"
     inkscape:document-units="in"
     inkscape:zoom="0.76988636"
     inkscape:cx="408.50185"
     inkscape:cy="515.66052"
     inkscape:window-width="1350"
     inkscape:window-height="1000"
     inkscape:window-x="67"
     inkscape:window-y="0"
     inkscape:window-maximized="0"
     inkscape:current-layer="layer1" />
    <g
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     id="layer1">
"""
postamble = """</g></svg></html>\n"""


def _good_run(cmd, *args, **kwargs):
    kwargs['check'] = True
    print(f"running: {cmd!r}", file=sys.stderr)
    return subprocess.run(cmd, *args, **kwargs)


def render_rect(rect, basex, basey, text):
    c = io.BytesIO()
    qrcode.make(f"https://u.staceyell.com/{text}").save(c)
    pngb64 = base64.b64encode(c.getbuffer()).decode('utf8')
    return f"""
        <rect
            style="fill:#ffffff;stroke-width:0;stroke:#000000;"
            id="rect{rect}"
            width="245.49077"
            height="{panel_height}"
            x="{basex}"
            y="{basey}" />
        <rect
            style="fill:#ffffff;stroke-width:0;stroke:#000000;"
            id="rect{rect}-qr-bbox"
            width="{panel_height}"
            height="{panel_height}"
            x="{basex}"
            y="{basey}" />
        <image xlink:href="data:image/png;base64,{pngb64}" x="{basex+10}" y="{basey}" height="{panel_height}" width="{panel_height}" />
        <text x="{basex+2+panel_height+10}" y="{basey+16}" font-family="monospace" font-size="7pt">{text}</text>
    """

def _gen_svg(fh):
    fh.write(preamble)
    for xidx, x in enumerate(xcoords):
        for yidx, y in enumerate(ycoords):
            text = 's0.' + ''.join(random.choice('23456789CFGHJMPQRVWXcfghjmpqrvwx') for _ in range(13))
            fh.write(render_rect(f"{xidx}-{yidx}", x, y, text))
    fh.write(postamble)
    fh.flush()

def main_generate_qr_svg():
    _gen_svg(sys.stdout)


def main_generate_qr_pdf():
    chrome_bin = 'chromium'
    if sys.platform == 'darwin':
        chrome_bin = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.html') as temp:
        _gen_svg(temp)
        _good_run([
            chrome_bin,
            '--headless',
            '--no-pdf-header-footer',
            '--disable-gpu',
            '--run-all-compositor-stages-before-draw',
            '--print-to-pdf=file1.pdf',
            temp.name,            
        ])
