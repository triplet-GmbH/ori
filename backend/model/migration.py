from . import CurrentDB


def migration_001_add_deleted_field():
    for char in CurrentDB.char.find({"deleted": {"$exists": False}}):
        CurrentDB.char.update_one(
            {"_id": char["_id"]},
            {"$set": {"deleted": False}}
         )


migrations = [
    (name, func)
    for name, func in globals().items()
    if name.startswith("migration_")
]


def run_migrations():
    for name, func in migrations:
        if not CurrentDB.migrations.find_one({"name": name}):
            print(f"executing {name}.")
            func()
            CurrentDB.migrations.insert_one({"name": name})
            print(f"{name} completed.")
    print("Migrations completed.")


def get_status() -> list[tuple[str, bool]]:
    done = [mig["name"] for mig in CurrentDB.migrations.find()]
    return [(name, name in done) for name, _ in migrations]

