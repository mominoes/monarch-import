import pandas as pd
import sys
import os

def merge_and_sort_csv_files(input_dir, output_file):
    # Read and concatenate all CSV files
    input_files = [f"{input_dir}/{file}" for file in os.listdir(input_dir) if file.endswith(".csv")]
    combined_df = pd.concat([pd.read_csv(file, index_col=False) for file in input_files], ignore_index=True)

    # Remove duplicate rows
    combined_df.drop_duplicates(inplace=True)

    # Sort by the third column (index 2)
    sorted_df = combined_df.sort_values(by=combined_df.columns[2])

    # Write the sorted and deduplicated dataframe to the output file
    sorted_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python merge_and_sort_csv.py input_dir output_file")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_file = sys.argv[2]

    merge_and_sort_csv_files(input_dir, output_file)
