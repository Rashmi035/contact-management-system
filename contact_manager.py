
import json
from pathlib import Path

FILE = Path(__file__).with_name("contacts.json")


def load_contacts():
    if FILE.exists():
        try:
            with FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list) and all(
                    isinstance(c, dict)
                    and isinstance(c.get("name"), str)
                    and isinstance(c.get("phone"), str)
                    for c in data
                ):
                    return data
                print("Invalid contact data. Starting with an empty list.")
        except (json.JSONDecodeError, OSError):
            print("Could not read saved contacts. Starting with an empty list.")
    return []


def save_contacts(contacts):
    try:
        with FILE.open("w", encoding="utf-8") as file:
            json.dump(contacts, file, indent=4)
        return True
    except OSError:
        print("Error: Could not save contacts.")
        return False



def add_contact(contacts):
    name = input("Enter name: ").strip()
    phone = input("Enter phone number: ").strip()

    if not name or not phone:
        print("Name and phone number cannot be empty.")
        return

    # Check whether the phone number already exists
    for contact in contacts:
        if contact["phone"] == phone:
            print("This phone number already exists!")
            return

    contacts.append({"name": name, "phone": phone})

    if save_contacts(contacts):
        print("Contact added successfully!")
    else:
        contacts.pop()

    name = input("Enter name: ").strip()
    phone = input("Enter phone number: ").strip()

    if not name or not phone:
        print("Name and phone number cannot be empty.")
        return

    contacts.append({"name": name, "phone": phone})
    if save_contacts(contacts):
        print("Contact added successfully!")
    else:
        contacts.pop()




def view_contacts(contacts):
    if not contacts:
        print("No contacts found.")
        return

    sorted_contacts = sorted(
        contacts,
        key=lambda contact: contact["name"].casefold()
    )

    for number, contact in enumerate(sorted_contacts, start=1):
        print(f"{number}. {contact['name']} - {contact['phone']}")

def search_contact(contacts):
    name = input("Enter name to search: ").strip().casefold()

    matches = [
        c for c in contacts
        if name and name in c["name"].casefold()
    ]

    if matches:
        for contact in matches:
            print(f"{contact['name']} - {contact['phone']}")
    else:
        print("Contact not found.")


def update_contact(contacts):
    name = input("Enter the exact name to update: ").strip().casefold()

    matches = [
        c for c in contacts
        if c["name"].casefold() == name
    ]

    if len(matches) != 1:
        print("Contact not found or name is not unique.")
        return

    new_phone = input("Enter new phone number: ").strip()
    if not new_phone:
        print("Phone number cannot be empty.")
        return

    old_phone = matches[0]["phone"]
    matches[0]["phone"] = new_phone

    if save_contacts(contacts):
        print("Contact updated successfully!")
    else:
        matches[0]["phone"] = old_phone


def delete_contact(contacts):
    name = input("Enter the exact name to delete: ").strip().casefold()

    matches = [
        c for c in contacts
        if c["name"].casefold() == name
    ]

    if len(matches) != 1:
        print("Contact not found or name is not unique.")
        return

    contact = matches[0]
    confirm = input(
        f"Delete {contact['name']}? (yes/no): "
    ).strip().casefold()

    if confirm != "yes":
        print("Deletion cancelled.")
        return

    index = contacts.index(contact)
    contacts.pop(index)

    if save_contacts(contacts):
        print("Contact deleted successfully!")
    else:
        contacts.insert(index, contact)


def main():
    contacts = load_contacts()

    while True:
        print("\n===== CONTACT MANAGEMENT SYSTEM =====")
        print("1. Add Contact")
        print("2. View All Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            view_contacts(contacts)
        elif choice == "3":
            search_contact(contacts)
        elif choice == "4":
            update_contact(contacts)
        elif choice == "5":
            delete_contact(contacts)
        elif choice == "6":
            print("Thank you for using the Contact Management System!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
