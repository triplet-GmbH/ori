import click

from backend.model.char import generate_char
from backend.model.user import User
from backend.model.migration import run_migrations, get_status

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


@main.group()
def migration():
    pass


@migration.command(name="run-pending")
def migration_run_pending():
    run_migrations()


@migration.command(name="status")
def migration_status():
    status = get_status()
    for name, done in status:
        print(f"{name}: {'done' if done else 'pending'}")


if __name__ in {"__main__", "__mp_main__"}:
    main()
