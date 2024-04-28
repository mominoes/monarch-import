import argparse
import calendar
import pandas as pd

def transform_account_num(account_num):
    if str.endswith(account_num, "1234567"):
        return "RBC Chequing 1"
    if str.endswith(account_num, "1234567"):
        return "RBC Saving 2"
    if str.endswith(account_num, "9876"):
        return "RBC Visa 3"
    if str.endswith(account_num, "9876"):
        return "RBC MasterCard 4"
    return ""

def transform_csv(input_file, month):
    # Read the input CSV file
    bank_data = pd.read_csv(input_file, index_col=False)

    # Print the first few rows of the input DataFrame for debugging
    print("\nFirst few rows of the input DataFrame:")
    print(bank_data.head())

    # Create a DataFrame for the output with Monarch Money format
    output_data = pd.DataFrame(columns=["Date", "Merchant", "Category", "Account", "Original Statement", "Notes", "Amount", "Tags"])

    # Populate each column in the output DataFrame based on the provided rules
    output_data["Date"] = pd.to_datetime(bank_data["Transaction Date"], format='%m/%d/%Y')
    output_data["Merchant"] = bank_data["Description 1"].fillna('') + " " + bank_data["Description 2"].fillna('')
    output_data["Category"] = ""  # Leave blank
    output_data["Account"] = bank_data["Account Number"].map(transform_account_num)
    output_data["Original Statement"] = output_data["Merchant"]
    output_data["Notes"] = ""  # Leave blank
    output_data["Amount"] = bank_data["CAD$"]

    # Keep only transactions for certain month
    output_data = output_data[output_data['Date'].dt.month == month]

    # Filter out unwanted accounts
    output_data = output_data[output_data['Account'] != ""]

    # Print the first few rows of the output DataFrame
    print("\nFirst few rows of the output DataFrame:")
    print(output_data.head())

    # Write the transformed data to a new CSV file
    output_file = f"monarch-rbc-{calendar.month_abbr[month]}.csv"
    output_data.to_csv(output_file, index=False)

    print("\nTransformation completed. Output saved to:", output_file)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Transform bank data CSV into Monarch Money format")
    parser.add_argument("input_file", help="Path to the input CSV file")
    parser.add_argument("month", type=int, help="Filter transactions by the specified month (1-12)")
    args = parser.parse_args()

    # Call the transform_csv function with provided input and output files
    transform_csv(args.input_file, args.month)
