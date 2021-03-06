import json

from flask import Flask, request, redirect, send_from_directory, url_for
from flask.views import MethodView
from flask_restful import Resource, Api
from werkzeug.routing import BaseConverter

from common import site_dir, build_dir, site_root, categories
from render import render_template, Document


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter
api = Api(app)


class ApiCategories(Resource):
    def get(self, name):
        cat_dir = site_dir / name
        def gen():
            for f in cat_dir.glob('*.json'):
                doc = Document(f)
                yield dict(slug=doc.slug, title=doc.title)
        return list(gen())

    def post(self, name):
        result = request.get_json()
        json_file = site_dir / name / (result['slug'] + '.json')
        with json_file.open('w') as fp:
            json.dump(result, fp, indent=2)
        return result


class ApiDocs(Resource):
    def get(self, name, slug):
        json_file = site_dir / name / (slug + '.json')
        with json_file.open() as fp:
            result = json.load(fp)
            result['slug'] = slug
            return result

    def put(self, name, slug):
        json_file = site_dir / name / (slug + '.json')
        result = request.get_json()
        with json_file.open('w') as fp:
            json.dump(result, fp, indent=2)
        return result


api.add_resource(ApiCategories, '/api/categories/<name>/')
api.add_resource(ApiDocs, '/api/categories/<name>/docs/<slug>/')


@app.route('/')
def redirect_to_site_root():
    return redirect(site_root)


@app.route('/cms/')
def cms():
    return render_template(
        'cms.html',
        # categories=categories
        categories=['lyrics', 'document', 'video']
    )


@app.route(site_root)
def home():
    return render_template('index.html', categories=categories)


@app.route(site_root + '<regex("lyrics|document|video"):catname>/')
def category(catname):
    return render_template(
        'category.html', category=catname, docs=get_docs(catname))


@app.route(site_root + '<regex("lyrics|document|video"):catname>/<slug>/')
def translation(catname, slug):
    json_file = site_dir / catname / (slug + '.json')
    return render_template(
        'translation.html', category=catname, doc=Document(json_file))


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


def get_build_urls():
    """
    Return a sequence of URLs to generate HTML files from.

    """
    with app.test_request_context():
        yield url_for('home')
        for cat in categories:
            yield url_for('category', name=cat)
            for file_ in (site_dir / cat).glob('*.json'):
                yield url_for('translation', category=cat, slug=file_.stem)
