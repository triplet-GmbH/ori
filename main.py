import click

from backend.model.char import generate_char
from backend.model.user import User


@click.group()
def main():
    pass


@main.command()
def testdata():
    for _ in range(10):
        generate_char()


@main.command()
@click.argument('username')
@click.argument('password')
def put_user(username, password):
    User.put(username, password)
    print(f"User {username!r} created/updated.")


if __name__ in {"__main__", "__mp_main__"}:
    main()
