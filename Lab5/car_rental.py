
"""Car rental management system with security and code-quality improvements."""

import hashlib
import os
import re
import secrets
import sqlite3
import tempfile
from datetime import datetime


# Global rental state
FLEET = {}
BOOKINGS = []

DB_CONNECTION = sqlite3.connect(":memory:")
DB_CONNECTION.execute(
    """
    CREATE TABLE customers (
        name TEXT,
        licence TEXT,
        phone TEXT
    )
    """
)


def add_car(plate, model="Unknown", daily_rate=0, features=None):
    """Add a car to the rental fleet."""
    if not plate:
        raise ValueError("Car registration plate cannot be empty.")

    if daily_rate < 0:
        raise ValueError("Daily rental rate cannot be negative.")

    if features is None:
        features = []

    FLEET[plate] = {
        "model": model,
        "rate": daily_rate,
        "available": True,
        "features": features,
    }
    return FLEET[plate]


def register_customer(name, licence, phone):
    """Register a customer using a parameterized SQL query."""
    DB_CONNECTION.execute(
        "INSERT INTO customers VALUES (?, ?, ?)",
        (name, licence, phone),
    )
    DB_CONNECTION.commit()


def find_customer(name):
    """Find customers by name without allowing SQL injection."""
    query = "SELECT * FROM customers WHERE name = ?"
    return DB_CONNECTION.execute(query, (name,)).fetchall()


def rent_car(plate, customer, start, end):
    """Calculate rental cost and create a booking."""
    if plate not in FLEET:
        raise ValueError("Car not found.")

    if not FLEET[plate]["available"]:
        raise ValueError("Car is not available.")

    if not find_customer(customer):
        raise ValueError("Customer not registered.")

    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    days = (end_date - start_date).days

    if days <= 0:
        raise ValueError("End date must be after start date.")

    daily_rate = FLEET[plate]["rate"]
    cost = days * daily_rate

    booking = {
        "code": booking_code(),
        "plate": plate,
        "customer": customer,
        "days": days,
        "cost": cost,
    }

    BOOKINGS.append(booking)
    FLEET[plate]["available"] = False

    return cost


def return_car(plate, km_driven):
    """Return a rented car and calculate any extra-distance charge."""
    if plate not in FLEET:
        raise ValueError("Car not found.")

    if km_driven < 0:
        raise ValueError("Kilometres driven cannot be negative.")

    FLEET[plate]["available"] = True

    if km_driven > 300:
        return (km_driven - 300) * 5

    return 0


def booking_code():
    """Generate a booking code using a secure random number generator."""
    return "BK-" + str(secrets.randbelow(90000) + 10000)


def licence_hash(licence):
    """Generate a SHA-256 hash of a driving licence number."""
    return hashlib.sha256(licence.encode("utf-8")).hexdigest()


def apply_promo(amount, discount_rate=0.10):
    """Apply a validated discount without executing arbitrary code."""
    if amount < 0:
        raise ValueError("Amount cannot be negative.")

    if not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1.")

    return amount * (1 - discount_rate)


def is_valid_plate(plate):
    """Check whether a vehicle registration plate has a valid format."""
    pattern = r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}"
    return bool(re.fullmatch(pattern, plate))


def write_receipt(booking):
    """Write a booking receipt to a securely created temporary file."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        suffix=".txt",
        delete=False,
    ) as receipt_file:
        receipt_file.write(
            f"Booking {booking['code']}: {booking['plate']} "
            f"for {booking['days']} days = Rs.{booking['cost']}\n"
        )
        path = receipt_file.name

    os.chmod(path, 0o600)
    return path


def admin_login(user, password):
    """Authenticate an administrator using an environment variable."""
    expected_password = os.environ.get("ADMIN_PASSWORD")

    if not expected_password:
        return False

    return (
        user == "admin"
        and secrets.compare_digest(password, expected_password)
    )


def available_cars():
    """Return the registration plates of all available cars."""
    return [
        plate
        for plate, details in FLEET.items()
        if details["available"]
    ]


def main():
    """Run the car rental demonstration."""
    add_car("KA01AB1234", "Swift", 1500)
    add_car("KA02CD5678", "Innova", 3000)
    add_car("KA03EF9999", "Nexon", 500)

    register_customer("Ravi", "DL-0420110012345", "9845012345")
    register_customer("Meera", "DL-0420110099999", "9845099999")

    print(
        "Rent Swift:",
        rent_car(
            "KA01AB1234",
            "Ravi",
            "2026-11-01",
            "2026-11-04",
        ),
    )

    print(
        "Rent Innova:",
        rent_car(
            "KA02CD5678",
            "Ravi",
            "2026-11-04",
            "2026-11-07",
        ),
    )

    # This input is treated as a normal customer name, not SQL code.
    print("Lookup injection:", find_customer("x' OR '1'='1"))

    print("Extra km charge:", return_car("KA01AB1234", 420))

    try:
        return_car("XX00XX0000", 50)
    except ValueError as error:
        print("Return unknown car:", error)

    print("Promo price:", apply_promo(4500, 0.10))
    print("Plate valid?", is_valid_plate("KA01AB1234"))
    print("Licence hash:", licence_hash("DL-0420110012345"))

    admin_password = os.environ.get("ADMIN_PASSWORD", "")
    print("Admin:", admin_login("admin", admin_password))

    print("Available:", available_cars())

    print("Receipt saved to:", write_receipt(BOOKINGS[0]))


if __name__ == "__main__":
    main()
