import subprocess
from pathlib import Path

from invoke import task

from common import site_dir, build_dir, site_root, categories
from render import render_template
from app import app


<<<<<<< HEAD
@task
def serve(ctx):
    """
    Serve the site at localhost:8000 so that you can see the results of your
    changes without building.

    """
    app.run(port=8000, debug=True)
=======
app = Flask(__name__)
site = Path('site')
build_dir = Path('build')
lookup = TemplateLookup(directories=[str(site)], strict_undefined=True)
>>>>>>> origin/master


@task
def serve_build(ctx):
    """
    Serve the contents of the build/ directory.

    """
    run('cd {} && python -m http.server'.format(build_dir))


@task
def clean(ctx):
    """
    Delete all files inside the build directory.

    """
    if build_dir.exists():
        run('rm -rf build/*')


@task
def build(ctx):
    """
    Build the static files for the web site and put them inside the build
    directory.

    """
    import shutil

<<<<<<< HEAD
    clean(ctx)
=======
@task
def build(ctx):
    for src in site.rglob('*?.*'):
        if src.name.startswith('_'):
            continue
        dest = build_dir / src.relative_to(site)
        print(src, dest)

@task
def publish(ctx):
    build()
    run('ghp-import -n -p build')


def run(cmd):
    subprocess.call(cmd, shell=True)
>>>>>>> origin/master

    client = app.test_client()

    # Generate HTML files using Flask.
    for url in get_build_urls():
        dest = build_dir / Path(url).relative_to(site_root) / 'index.html'
        print(dest)
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open('wb') as fp:
            data = client.get(url).data
            fp.write(data)

    # Copy static files.
    for src in site_dir.rglob('*?.*'):
        dest = build_dir / src.relative_to(site_dir)
        print(dest)
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(str(src), str(dest))


@task
def publish(ctx):
    """
    Publish the web site to GitHub Pages.

    """
    build(ctx)
    run('ghp-import -n -p {}'.format(build_dir))


def run(cmd):
    subprocess.call(cmd, shell=isinstance(cmd, str))


def get_build_urls():
    """
    Return a sequence of URLs to generate HTML files from.

    """
    yield site_root
    for category in categories:
        for file_ in (site_root / category).glob('*.json'):
            yield '{}{}/{}/'.format(site_root, category.name, file_.stem)
