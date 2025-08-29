import click

@click.group()
def cli():
    pass

@cli.command()
def init_db():
    print("Database initialized!")

if __name__ == '__main__':
    cli()
