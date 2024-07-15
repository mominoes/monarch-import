# monarch-import

Convert CSV files of RBC bank transactions into a Monarch-compatible format.

## Usage instructions - RBC

Start by
[downloading transaction files](https://www.rbcroyalbank.com/onlinebanking/bankingusertips/accountingsoftware/index.html)
from your bank. Chequing transactions are available from the past 90-120 days. Credit card
transactions, on the other hand, are only available up to your last statement (insert rant).

Therefore, it's necessary to (1) download roughly every month, and (2) deduplicate transactions that
ended up getting downloaded twice. (Warning: this will also dedupe real transactions that look
identical).

Setup
1. In [convert.py](./convert.py), tailor `transform_account_num()` to your accounts

Run script
1. Download transaction data from RBC into `./inputs/`
1. Merge and dedupe multiple files: `python3 merge.py ./inputs ./merged/merged-deduped-input.csv`
1. Run script: `python3 convert.py ./merged/merged-deduped-input.csv 3 momin` (`3` = month of the year; `momin` = output file prefix)
1. Import output CSV file of transactions into Monarch
