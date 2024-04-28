# monarch-import

Convert CSV files of bank transactions into Monarch-compatible format. Banks supported so far: RBC
(CAD$).

Usage instructions:

1. Download a transactions file from bank
1. Tailor `transform_account_num()` to your accounts
1. Run script: `python3 convert.py <input_filename.csv> 3` (`3` = month of the year)
1. Import output CSV file of transactions into Monarch
