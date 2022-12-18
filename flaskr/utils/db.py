from pymongo import MongoClient

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        client = MongoClient(
            current_app.config['DATABASE'],
            document_class=dict,
        )
        g.db = client.flaskr
    return g.db


def close_db(e=None):
    g.pop('db', None)


def init_db():
    db = get_db()
    collections = db.list_collection_names()

    if 'users' in collections:
        db['users'].drop()

    if 'blogs' in collections:
        db['blogs'].drop()

    db.create_collection('users')
    db['users'].create_index('username', unique=True)
    db['users'].create_index('password')

    db.create_collection('blogs')
    db['blogs'].create_index('author_id')
    db['blogs'].create_index('title')
    db['blogs'].create_index('body')


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Database initialized.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
