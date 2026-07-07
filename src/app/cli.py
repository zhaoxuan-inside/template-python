import click


@click.group()
def main():
    pass

@main.command()
def hello():
    click.echo("Hello from app CLI!")

if __name__ == "__main__":
    main()
