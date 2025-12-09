"""
restaurant_system.py

This file has two classes used for a simple restaurant ordering program:

- MenuItem: one item on the menu
- Order: holds the customer's items and calculates totals
"""


class MenuItem:
    """Represents a single item on the restaurant menu."""

    def __init__(self, item_id, name, price, category):
        """
        Create a new menu item.

        item_id  - number that identifies the item
        name     - name of the item
        price    - price as a float
        category - type of item (for example: 'Entree', 'Drink', 'Dessert')
        """
        self.item_id = item_id
        self.name = name
        self.price = price
        self.category = category

    def __str__(self):
        """Return a simple string with the name and price."""
        return f"{self.name} (${self.price:.2f})"


class Order:
    """Represents a customer's order."""

    def __init__(self):
        """Start with an empty order."""
        # dictionary: key = MenuItem object, value = quantity (int)
        self.items = {}

    def add_item(self, menu_item, quantity):
        """
        Add an item to the order.

        If the item is already in the order, increase the quantity.
        """
        if menu_item in self.items:
            self.items[menu_item] += quantity
        else:
            self.items[menu_item] = quantity

    def is_empty(self):
        """Return True if there are no items in the order."""
        return len(self.items) == 0

    def calculate_subtotal(self):
        """Return the subtotal (items * quantities)."""
        subtotal = 0.0
        for item, quantity in self.items.items():
            subtotal += item.price * quantity
        return subtotal

    def calculate_tax(self, tax_rate):
        """
        Return the tax amount.

        tax_rate is a decimal (example: 0.08 for 8%)
        """
        return self.calculate_subtotal() * tax_rate

    def calculate_tip(self, tip_rate):
        """
        Return the tip amount.

        tip_rate is a decimal (example: 0.15 for 15%)
        """
        return self.calculate_subtotal() * tip_rate

    def calculate_total(self, tax_rate, tip_rate):
        """Return subtotal + tax + tip."""
        subtotal = self.calculate_subtotal()
        tax_amount = self.calculate_tax(tax_rate)
        tip_amount = self.calculate_tip(tip_rate)
        total = subtotal + tax_amount + tip_amount
        return total

    def build_order_summary(self):
        """Build a text summary for all items in the order."""
        if self.is_empty():
            return "No items in the order yet."

        lines = []
        for item, quantity in self.items.items():
            line_total = item.price * quantity
            # example line: Burger x 2 @ $10.00 = $20.00
            line = f"{item.name} x {quantity} @ ${item.price:.2f} = ${line_total:.2f}"
            lines.append(line)

        return "\n".join(lines)

    def generate_receipt_text(self, customer_name, tax_rate, tip_rate):
        """
        Build a full receipt as one big string.

        This can later be printed to the screen or saved to a text file.
        """
        subtotal = self.calculate_subtotal()
        tax_amount = self.calculate_tax(tax_rate)
        tip_amount = self.calculate_tip(tip_rate)
        total = self.calculate_total(tax_rate, tip_rate)

        summary = self.build_order_summary()

        receipt_lines = []
        receipt_lines.append("====================================")
        receipt_lines.append("        SIMPLE RESTAURANT RECEIPT   ")
        receipt_lines.append("====================================")
        receipt_lines.append(f"Customer: {customer_name}")
        receipt_lines.append("")
        receipt_lines.append("Items:")
        receipt_lines.append(summary)
        receipt_lines.append("")
        receipt_lines.append(f"Subtotal: ${subtotal:.2f}")
        receipt_lines.append(f"Tax:      ${tax_amount:.2f}")
        receipt_lines.append(f"Tip:      ${tip_amount:.2f}")
        receipt_lines.append("------------------------------------")
        receipt_lines.append(f"TOTAL:    ${total:.2f}")
        receipt_lines.append("====================================")
        receipt_lines.append(" Thank you for your order!")
        receipt_lines.append("====================================")

        return "\n".join(receipt_lines)
