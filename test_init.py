import click

@click.group()
def test_cli():
    pass

@test_cli.command()
def init_db():
    print("This should work!")

if __name__ == '__main__':
    test_cli()
