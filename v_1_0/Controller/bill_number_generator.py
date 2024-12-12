from datetime import date
import os
def onlyread():
    today = date.today()
    year = today.strftime("%Y")
    month = today.strftime("%m")
    filename = "assets\\temp\\last_bill_number.txt"
    with open(filename, "r") as file:
        last_number = file.read().strip()
    base_number = int(last_number[len(year) + len(month) + 1:])
    return base_number
def update(value):
    today = date.today()
    year = today.strftime("%Y")
    month = today.strftime("%m")
    filename = "assets\\temp\\last_bill_number.txt"
            # Format the bill number with leading zeros
    bill_number = f"{year}{month}-{value:04d}"
    # Save the new bill number for next time
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as file:
        file.write(bill_number)
def generate_bill_number():
    
    """
    Generates a bill number based on the current date.

    Returns:
        str: The bill number (YYYYMM-000X format).
    """
    today = date.today()
    year = today.strftime("%Y")
    month = today.strftime("%m")
    
    # Reset bill number to 0001 on the 1st day of the month
    if today.day == 1:
        bill_number = f"{year}{month}-0001"
    else:
        # Load or create a file to store the last bill number
        filename = "assets\\temp\\last_bill_number.txt"
        try:
            with open(filename, "r") as file:
                last_number = file.read().strip()
        except FileNotFoundError:
            last_number = f"{year}{month}-0000"  # Use 0000 as initial value if file doesn't exist

        # Extract only the base number from the last bill number (remove year-month prefix)
        base_number = int(last_number[len(year) + len(month) + 1:])  # Skip "YYYYMM-" prefix
        new_number = base_number + 1

        # Format the bill number with leading zeros
        bill_number = f"{year}{month}-{new_number:04d}"

    # Save the new bill number for next time
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as file:
        file.write(bill_number)
    
    return bill_number

# Example usage for testing
# bill_number = generate_bill_number()
# print(f"Generated bill number: {bill_number}")
