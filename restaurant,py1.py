"""
Final Project: Choose Your Own Python Project
Course: ADD-100 Programming Logic
Assignment: Final Project CRUD / Choose Your Own Python Project
Due Date: December 9

Student Information:
    Name: Raed Al Kiswani
    Course: ADD-100 Programming Logic
    Section: YOUR SECTION
    Date: December 9, 2025
    Project: Restaurant Ordering System (Final Project)

AI Use Disclosure:
    Portions of this program were created with assistance from ChatGPT (OpenAI).
    The student reviewed, tested, and modified the code to ensure understanding.
    https://chat.openai.com/
"""

from restaurant_system import MenuItem, Order

MENU_FILE = "menu.txt"
RECEIPT_FILE = "receipt.txt"
TAX_RATE = 0.08  # 8% tax


def load_menu(filename):
    """Load menu items from a text file into a dictionary."""
    menu = {}

    try:
        file = open(filename, "r", encoding="utf-8")

        for line in file:
            line = line.strip()

            # Skip blank lines or comment lines
            if line == "" or line.startswith("#"):
                continue

            parts = line.split(",")

            # Expecting: id,name,price,category
            if len(parts) != 4:
                print("Skipping bad menu line:", line)
                continue

            try:
                item_id = int(parts[0])
                name = parts[1]
                price = float(parts[2])
                category = parts[3]
            except ValueError:
                print("Skipping line with bad number:", line)
                continue

            menu[item_id] = MenuItem(item_id, name, price, category)

        file.close()

    except FileNotFoundError:
        print("ERROR: Cannot find menu file:", filename)

    return menu


def display_menu(menu):
    """Display all menu items grouped by category."""
    print("\n========== MENU ==========")

    # Build a dictionary of categories -> list of items
    categories = {}
    for item in menu.values():
        if item.category not in categories:
            categories[item.category] = []
        categories[item.category].append(item)

    # Print categories and items
    for cat in categories:
        print("\n---", cat.upper(), "---")
        for item in categories[cat]:
            print(f"{item.item_id}. {item.name:<20} ${item.price:.2f}")

    print("\n==========================\n")


def get_int_input(prompt, min_val=None, max_val=None):
    """
    Ask the user for an integer.
    Optionally check minimum and maximum values.
    """
    while True:
        user_input = input(prompt)

        try:
            num = int(user_input)
        except ValueError:
            print("Please enter a whole number.")
            continue

        if min_val is not None and num < min_val:
            print("Enter at least", min_val)
            continue

        if max_val is not None and num > max_val:
            print("Enter at most", max_val)
            continue

        return num


def handle_add_item(order, menu):
    """Let the user choose menu items and add them to the order."""
    while True:
        display_menu(menu)
        print("Enter 0 to go back to the main menu.")

        choice = get_int_input("Choose item number: ", 0)

        if choice == 0:
            break

        if choice not in menu:
            print("That item number is not on the menu.")
            continue

        qty = get_int_input("Quantity: ", 1)
        order.add_item(menu[choice], qty)
        print("Added", qty, "x", menu[choice].name)

        again = input("Add another item? (y/n): ").lower()
        if again != "y":
            break


def handle_view_order(order):
    """Print the current order contents."""
    print("\n========== CURRENT ORDER ==========")
    if order.is_empty():
        print("Your order is empty.")
    else:
        print(order.build_order_summary())
    print("===================================\n")


def ask_for_tip_percentage():
    """Ask the user if they want to leave a tip and return the tip rate."""
    while True:
        choice = input("Would you like to leave a tip? (y/n): ").lower()

        if choice == "y":
            tip_percent = get_int_input("Tip %: ", 0, 100)
            return tip_percent / 100.0
        elif choice == "n":
            return 0.0
        else:
            print("Please enter y or n.")


def save_receipt(filename, text):
    """Save the receipt text to a file."""
    try:
        file = open(filename, "w", encoding="utf-8")
        file.write(text)
        file.close()
        print("Receipt saved to", filename)
    except Exception:
        print("ERROR: Could not write the receipt file.")


def handle_checkout(order):
    """Checkout the current order and write the receipt."""
    if order.is_empty():
        print("You cannot checkout. Your order is empty.")
        return

    name = input("Enter your name for the receipt: ").strip()
    if name == "":
        name = "Guest"

    tip_rate = ask_for_tip_percentage()

    # Build the full receipt text using the Order class
    receipt = order.generate_receipt_text(name, TAX_RATE, tip_rate)

    print("\n======= RECEIPT PREVIEW =======")
    print(receipt)
    print("================================\n")

    save_receipt(RECEIPT_FILE, receipt)


def show_main_menu():
    """Print the main menu options."""
    print("========== RESTAURANT ==========")
    print("1. View menu and add items")
    print("2. View current order")
    print("3. Checkout")
    print("4. Exit")
    print("================================")


def main():
    """Main function to run the restaurant ordering system."""
    print("Welcome to the Restaurant Ordering System!")

    menu = load_menu(MENU_FILE)
    order = Order()

    while True:
        show_main_menu()
        choice = get_int_input("Choose (1-4): ", 1, 4)

        if choice == 1:
            handle_add_item(order, menu)
        elif choice == 2:
            handle_view_order(order)
        elif choice == 3:
            handle_checkout(order)
        elif choice == 4:
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
