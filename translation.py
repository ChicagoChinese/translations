from io import StringIO
from html.parser import HTMLParser
from pathlib import Path
import html

import attr
from markdown import markdown


def to_html(text):
    lines = get_translation_lines(text)
    return get_translation_html(lines)


@attr.s
class TLine:
    """
    A line of text that has a translated version and possibly some attached
    notes.

    """
    orig = attr.ib(default='')
    tran = attr.ib(default='')
    notes = attr.ib(default=attr.Factory(list))

    @property
    def rendered_notes(self):
        return markdown('\n\n'.join(self.notes))


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

    def gen():
        yield '<div class="lyrics">'
        for tline in lines:
            yield '<div class="line row">'
            yield ' <div class="orig">{}</div>'.format(escape(tline.orig))
            yield ' <div class="tran">{}</div>'.format(escape(tline.tran))
            yield ' <div class="notes">{}</div>'.format(tline.rendered_notes)
            yield '</div>'
        yield '</div>'

    return '\n'.join(gen())
