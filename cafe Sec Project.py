# Brew & Bite Cafe 55

MENU_SIZE = 12
MAX_ORDER = 30
GST_RATE = 0.05

menu = [
    {"id": 1, "name": "Espresso",          "category": "Coffee",  "price": 120.0},
    {"id": 2, "name": "Cappuccino",        "category": "Coffee",  "price": 160.0},
    {"id": 3, "name": "Cafe Latte",        "category": "Coffee",  "price": 170.0},
    {"id": 4, "name": "Cold Coffee",       "category": "Coffee",  "price": 180.0},
    {"id": 5, "name": "Masala Chai",       "category": "Tea",     "price": 60.0},
    {"id": 6, "name": "Green Tea",         "category": "Tea",     "price": 80.0},
    {"id": 7, "name": "Veg Sandwich",      "category": "Snacks",  "price": 110.0},
    {"id": 8, "name": "French Fries",      "category": "Snacks",  "price": 99.0},
    {"id": 9, "name": "Veg Burger",        "category": "Snacks",  "price": 130.0},
    {"id": 10, "name": "Chocolate Brownie", "category": "Dessert", "price": 140.0},
    {"id": 11, "name": "Cheesecake Slice",  "category": "Dessert", "price": 190.0},
    {"id": 12, "name": "Ice Cream Scoop",   "category": "Dessert", "price": 70.0}
]

order = []
bill_number = 1
day_sales = 0.0


# Read integer input safely
def read_int(prompt, minimum, maximum):
    while True:
        try:
            value = int(input(prompt))

            if minimum <= value <= maximum:
                return value

            print(f"Please enter a number between {minimum} and {maximum}.")

        except ValueError:
            print("Please enter a valid number.")


# Display menu
def show_menu():
    last_category = ""

    print("\n================ CAFE MENU ================")

    for item in menu:

        if item["category"] != last_category:
            print(f"\n-- {item['category']} --")
            last_category = item["category"]

        print(
            f"  {item['id']:2d}. "
            f"{item['name']:<20} "
            f"Rs {item['price']:6.2f}"
        )


# Add item to order
def add_item():
    show_menu()

    item_id = read_int(
        "\nEnter item number (0 to cancel): ",
        0,
        MENU_SIZE
    )

    if item_id == 0:
        return

    quantity = read_int(
        "Enter quantity: ",
        1,
        50
    )

    # Check if item already exists
    for item in order:

        if item["menu_index"] == item_id - 1:
            item["qty"] += quantity

            print(
                f"Updated: {menu[item_id - 1]['name']} "
                f"x {item['qty']}"
            )

            return

    # Check maximum order size
    if len(order) >= MAX_ORDER:
        print("Order is full!")
        return

    order.append({
        "menu_index": item_id - 1,
        "qty": quantity
    })

    print(
        f"Added: {menu[item_id - 1]['name']} "
        f"x {quantity}"
    )


# Calculate subtotal
def order_subtotal():
    total = 0.0

    for item in order:
        menu_item = menu[item["menu_index"]]
        total += menu_item["price"] * item["qty"]

    return total


# Print order
def print_order(file):

    file.write(
        f"\n{'No':<3} "
        f"{'Item':<20} "
        f"{'Qty':<4} "
        f"{'Amount':>10}\n"
    )

    file.write("------------------------------------------\n")

    for i, item in enumerate(order):

        menu_item = menu[item["menu_index"]]

        amount = menu_item["price"] * item["qty"]

        file.write(
            f"{i + 1:<3} "
            f"{menu_item['name']:<20} "
            f"{item['qty']:<4} "
            f"{amount:>10.2f}\n"
        )

    file.write("------------------------------------------\n")

    file.write(
        f"Subtotal: Rs {order_subtotal():.2f}\n"
    )


# View current order
def view_order():

    if len(order) == 0:
        print("\nYour order is empty.")
        return

    import sys
    print_order(sys.stdout)


# Remove item
def remove_item():

    if len(order) == 0:
        print("\nYour order is empty.")
        return

    import sys
    print_order(sys.stdout)

    line_number = read_int(
        "\nEnter line number to remove (0 to cancel): ",
        0,
        len(order)
    )

    if line_number == 0:
        return

    order.pop(line_number - 1)

    print("Item removed.")


# Generate bill
def generate_bill():

    global bill_number
    global day_sales
    global order

    if len(order) == 0:
        print("\nNothing to bill. Add some items first.")
        return

    customer_name = input("Customer name: ")

    discount_code = input(
        "Discount code (press Enter if none): "
    )

    subtotal = order_subtotal()

    discount = 0.0

    # Apply discount
    if discount_code == "CAFE10":

        discount = subtotal * 0.10

        print("Code applied: 10% off!")

    elif discount_code != "":
        print("Invalid code, no discount applied.")

    taxable = subtotal - discount

    gst = taxable * GST_RATE

    grand_total = taxable + gst

    filename = f"bill_{bill_number}.txt"

    # Display bill on screen
    print("\n========== BREW & BITE CAFE ==========")

    print(f"Bill No: {bill_number}")

    if customer_name:
        print(f"Customer: {customer_name}")
    else:
        print("Customer: Guest")

    print_order(__import__("sys").stdout)

    if discount > 0:
        print(f"Discount: -Rs {discount:.2f}")

    print(f"GST (5%): Rs {gst:.2f}")

    print(f"GRAND TOTAL: Rs {grand_total:.2f}")

    print("\nThank you for visiting! :)")

    # Save bill to text file
    with open(filename, "w") as file:

        file.write(
            "\n========== BREW & BITE CAFE ==========\n"
        )

        file.write(
            f"Bill No: {bill_number}\n"
        )

        file.write(
            f"Customer: "
            f"{customer_name if customer_name else 'Guest'}\n"
        )

        print_order(file)

        if discount > 0:
            file.write(
                f"Discount: -Rs {discount:.2f}\n"
            )

        file.write(
            f"GST (5%): Rs {gst:.2f}\n"
        )

        file.write(
            f"GRAND TOTAL: Rs {grand_total:.2f}\n"
        )

        file.write(
            "\nThank you for visiting! :)\n"
        )

    print(f"\nBill saved to {filename}")

    # Save sales information
    with open("sales_log.txt", "a") as log:

        log.write(
            f"Bill {bill_number} | "
            f"{customer_name if customer_name else 'Guest'} | "
            f"Rs {grand_total:.2f}\n"
        )

    day_sales += grand_total

    bill_number += 1

    # Clear current order
    order.clear()


# Main program
def main():

    print("*** Welcome to Brew & Bite Cafe ***")

    while True:

        print("\n1. View Menu")
        print("2. Add Item")
        print("3. View Order")
        print("4. Remove Item")
        print("5. Generate Bill")
        print("6. Today's Sales")
        print("7. Exit")

        choice = read_int(
            "Choice: ",
            1,
            7
        )

        if choice == 1:
            show_menu()

        elif choice == 2:
            add_item()

        elif choice == 3:
            view_order()

        elif choice == 4:
            remove_item()

        elif choice == 5:
            generate_bill()

        elif choice == 6:
            print(
                f"\nBills today: {bill_number - 1} | "
                f"Total sales: Rs {day_sales:.2f}"
            )

        elif choice == 7:
            print("Goodbye!")
            break


# Start application
if __name__ == "__main__":
    main()
