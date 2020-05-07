import click
from _init import app_instance as app


@app.cli.command()
def test():
    click.echo('test')


app_instance = app
