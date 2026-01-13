import click

from backend.model.char import generate_char


@click.group()
def main():
    pass


@main.command()
def testdata():
    for _ in range(10):
        generate_char()


if __name__ in {"__main__", "__mp_main__"}:
    main()
