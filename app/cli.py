from app import app
import os
import click

@app.cli.group()
def translate():
    """Internationalization and localization commands"""
    pass

@translate.command()
@click.argument('lang')
def init(lang):
    """Create language catalogue"""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel init -i messages.pot -d app/translations' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')

@translate.command()
def compile():
    """Get language"""
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')

@translate.command()
def update():
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d app/translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')