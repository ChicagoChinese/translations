from io import StringIO
from html.parser import HTMLParser
from pathlib import Path
import html

import attr
from markdown import markdown
from mako.template import Template


template = Template(filename='translation.html')


def to_html(text):
    lines = get_translation_lines(text)
    return template.render(lines=lines)


@attr.s
class TLine:
    """
    A translation line, i.e. a line of text that has a translated version and
    possibly some attached notes.

    """
    orig = attr.ib(default='')
    tran = attr.ib(default='')
    notes = attr.ib(default=attr.Factory(list))
    last = attr.ib(default=False)   # True if last line in section

    @property
    def rendered_notes(self):
        return markdown('\n\n'.join(self.notes))


def get_translation_lines(text):
    dd = {}
    lines = []

    for line in (l.strip() for l in text.splitlines()):
        last_line = lines[-1] if len(lines) else None

        if line.startswith(';'):
            last_line.tran = line[1:]
            dd[last_line.orig] = last_line.tran
        elif line.startswith('^'):
            last_line.notes.append(line[1:])
        elif line:
            tline = TLine(orig=line)
            lines.append(tline)
        else:
            if last_line is not None:
                last_line.last = True

    for line in lines:
        if line.tran == '':
            line.tran = dd.get(line.orig, '')

    return lines
