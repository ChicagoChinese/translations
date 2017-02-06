from io import StringIO
from html.parser import HTMLParser
from pathlib import Path
import html
import collections

import attr
from markdown import markdown


@attr.s
class TLine:
    orig = attr.ib(default='')
    tran = attr.ib(default='')
    notes = attr.ib(default=attr.Factory(list))


class MyHtmlParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sio = StringIO()
        self.translation = None

    def get_output(self):
        return self.sio.getvalue()

    def handle_starttag(self, tag, attrs):
        if tag == 'translation':
            self.translation = []

    def handle_endtag(self, tag):
        if tag == 'translation':
            text = ''.join(self.translation)
            lines = get_translation_lines(text)
            html = get_translation_html(lines)
            self.sio.write(html)
            self.translation = None

    def handle_data(self, text):
        if self.translation is not None:
            self.translation.append(text)
        else:
            self.sio.write(text)

    def handle_startendtag(self, tag, attrs):
        if tag == 'video':
            url = dict(attrs).get('url')
            html = (
                '<div>'
                '<iframe src="{}" frameborder="0" allowfullscreen></iframe>'
                '</div>').format(url)
            self.sio.write(html)


def parse(filename):
    parser = MyHtmlParser()
    parser.feed(Path(filename).read_text())
    output = parser.get_output()
    return markdown(output)


def get_translation_lines(text):
    dd = {}
    lines = []

    for line in (l.strip() for l in text.splitlines() if l.strip()):
        last_line = lines[-1] if len(lines) else None

        if line.startswith(';'):
            last_line.tran = line[1:]
            dd[last_line.orig] = last_line.tran
        elif line.startswith('^'):
            last_line.notes.append(line[1:])
        else:
            tline = TLine(orig=line)
            lines.append(tline)

    for line in lines:
        if line.tran == '':
            line.tran = dd[line.orig]

    return lines


def get_translation_html(lines):
    escape = html.escape
    result = ['<div>']
    for tline in lines:
        result.append('<div class="line">')
        result.append(' <div class="orig">{}</div>'.format(escape(tline.orig)))
        result.append(' <div class="tran">{}</div>'.format(escape(tline.tran)))
        notes = '\n\n'.join(tline.notes)
        result.append(' <div class="note">{}</div>'.format(markdown(notes)))
        result.append('</div>')
    result.append('</div>')
    return '\n'.join(result)


with open('output.html', 'w') as fp:
    fp.write("""
    <html>
        <head>
        <meta charset='utf-8'>
        </head>
        <body>
    """)
    fp.write(parse('sample.md'))
    fp.write('</body></html>')
