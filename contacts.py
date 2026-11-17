
from database import (
    initialize_database,
    add_person,
    list_people,
    add_relationship
)


def show_menu():
    print("\n" + "=" * 40)
    print("       6DEGREES CONTACT MANAGER")
    print("=" * 40)
    print("1. Add a person")
    print("2. View all people")
    print("3. Connect two people")
    print("4. Exit")


def main():
    initialize_database()

    while True:
        show_menu()
        choice = input("\nChoose an option (1-4): ").strip()

        if choice == "1":
            name = input("Enter person's full name: ")
            add_person(name)

        elif choice == "2":
            list_people()

        elif choice == "3":
            list_people()

            try:
                first = int(input("\nFirst person's ID: "))
                second = int(input("Second person's ID: "))
                add_relationship(first, second)
            except ValueError:
                print("Please enter valid numeric IDs.")

        elif choice == "4":
            print("\nGoodbye from 6Degrees!")
            break

        else:
            print("Invalid option. Please choose 1-4.")


if __name__ == "__main__":
    main()
