import json
from pathlib import Path

from mako.lookup import TemplateLookup

from common import site_dir, template_dir, site_root
from markdownext import parse


lookup = TemplateLookup(
    directories=[str(template_dir)],
    strict_undefined=True,
)


def render_template(template_file, **kwargs):
    template_path = template_dir / template_file
    kwargs.update(
        ROOT=site_root,
        PATH=template_path,
    )
    tmpl = lookup.get_template(str(template_file))
    return tmpl.render(**kwargs)


class Document:
    def __init__(self, json_file):
        self.slug = json_file.stem
        with json_file.open() as fp:
            for k, v in json.load(fp).items():
                setattr(self, k, v)

    @property
    def content_html(self):
        return parse(self.content)
