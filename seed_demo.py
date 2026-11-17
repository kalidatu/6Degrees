
from database import initialize_database, connect


def seed_demo():
    """Create a fictional demonstration network."""

    initialize_database()

    names = [
        "Alex Rivera",
        "Morgan Lee",
        "Taylor Brooks",
        "Jordan Ellis",
        "Casey Parker",
    ]

    with connect() as db:
        for name in names:
            db.execute(
                "INSERT OR IGNORE INTO people (name) VALUES (?)",
                (name,)
            )

        ids = {
            name: db.execute(
                "SELECT id FROM people WHERE name = ?",
                (name,)
            ).fetchone()[0]
            for name in names
        }

        for first, second in zip(names, names[1:]):
            person1, person2 = sorted((ids[first], ids[second]))

            db.execute(
                """
                INSERT OR IGNORE INTO relationships
                (person1_id, person2_id)
                VALUES (?, ?)
                """,
                (person1, person2)
            )


if __name__ == "__main__":
    seed_demo()
    print("Demo network created successfully!")
