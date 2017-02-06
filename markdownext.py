from io import StringIO
from html.parser import HTMLParser

from markdown import markdown

import translation


def parse_file(filename):
    return parse(filename.read_text())


def parse(text):
    parser = MarkdownExtParser()
    parser.feed(text)
    output = parser.get_output()
    return markdown(output)


class MarkdownExtParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sio = StringIO()
        self.translation = None

    def get_output(self):
        return self.sio.getvalue()

    def handle_starttag(self, tag, attrs):
        if tag == 'translation':
            self.translation = []
        else:
            parts = ('{}="{}"'.format(k, v) for k, v in attrs)
            attr_str = (' ' + ' '.join(parts)) if len(attrs) else ''
            self.sio.write('<{}{}>'.format(tag, attr_str))

    def handle_endtag(self, tag):
        if tag == 'translation':
            text = ''.join(self.translation)
            self.sio.write(translation.to_html(text))
            self.translation = None
        else:
            self.sio.write('</{}>'.format(tag))

    def handle_data(self, text):
        if self.translation is not None:
            self.translation.append(text)
        else:
            self.sio.write(text)
