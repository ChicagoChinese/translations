import subprocess
from pathlib import Path
from invoke import task
from flask import Flask, send_from_directory
from mako.lookup import TemplateLookup

import markdownext


app = Flask(__name__)
site = Path('site')
lookup = TemplateLookup(directories=[str(site)], strict_undefined=True)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    filepath = site / path

    if not filepath.exists() and filepath.suffix == '':
        md_path = filepath.with_suffix('.md')
        return render(
            '_markdown.html',
            title=md_path.stem,
            content=markdownext.parse_file(md_path))

    if filepath.is_dir():
        index_path = filepath / 'index.html'
        if index_path.exists():
            return render(index_path.relative_to(site))

    if filepath.exists():
        return send_from_directory(str(site), path)

    return 'File not found', 404


@task
def serve(ctx):
    app.run(port=8000, debug=True)


def run(cmd):
    subprocess.call(cmd, shell=True)


def render(template_name, **kwargs):
    kwargs.update(
        PATH=site / template_name,
        get_translation_files=get_translation_files)
    tmpl = lookup.get_template(str(template_name))
    return tmpl.render(**kwargs)


def get_translation_files(path):
    for p in path.parent.glob('*.md'):
        yield p.relative_to(site)
