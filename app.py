from flask import Flask, redirect, send_from_directory

from common import site_dir, build_dir, site_root, categories
from render import render_template, Document


app = Flask(__name__)


@app.route('/')
def redirect_to_site_root():
    return redirect(site_root)


@app.route(site_root)
def home():
    return render_template('index.html', categories=categories)


@app.route(site_root + '<category>/')
def category(category):
    return render_template(
        'category.html', category=category, docs=get_docs(category))


@app.route(site_root + '<category>/<slug>/')
def translation(category, slug):
    json_file = site_dir / category / (slug + '.json')
    return render_template(
        'translation.html', category=category, doc=Document(json_file))


@app.route(site_root + '<path:path>')
def static_files(path):
    filepath = site_dir / path
    if filepath.exists():
        return send_from_directory(str(site_dir), path)
    else:
        return 'Page not found', 404


def get_docs(category):
    cat_dir = site_dir / category
    for json_file in cat_dir.glob('*.json'):
        yield Document(json_file)
