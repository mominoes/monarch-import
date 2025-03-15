# monarch-import

Canadian banks don't support
[open banking](https://www.canada.ca/en/financial-consumer-agency/services/banking/open-banking.html).
The only secure way to share data with 3p finance apps is to upload data manually. This repo helps
convert RBC transactions into a format compatible with Monarch.

## Usage instructions - RBC

### 0. Setup

In [convert.py](./convert.py), tailor `transform_account_num()` to your accounts (first time only).

### 1. Download transactions

1. [Download transaction files](https://www.rbcroyalbank.com/onlinebanking/bankingusertips/accountingsoftware/index.html)
   from your bank into `./inputs/`.

_Note:_

It's hard to reliably download all transactions from last month without missing any: see
[details](#difficulty-retrieving-last-months-transactions). The best compromise I've found is:

1. Download transactions every month
1. Download at least a few days after end-of-month to give time for Authorized txns to become Posted
1. Download "all transactions on file", not "only new transactions since the last download", and
   delete last month's download before running the script
1. Dedupe transactions that were counted twice
1. As a double check, ensure no txns from the beginning of the month were ignored: manually add them
   if so

### 2. Run script

1. Merge and dedupe multiple files: `python3 merge.py ./inputs ./merged/merged-deduped-input.csv`
1. Run script: `python3 convert.py ./merged/merged-deduped-input.csv 3 xxx` (`3` = month of the
   year; `xxx` = output file prefix)
1. Import output CSV file of transactions into Monarch

### Difficulty retrieving last month's transactions

Chequing transactions are available from the past 90-120 days. Credit card transactions, on the
other hand, are only available as far back as your last statement. Also, "The download (copy)
includes transactions posted as of the last business day." This makes it hard to guarantee that you
won't miss transactions if doing a monthly download.

Say your credit card statement is from the 2nd to the 1st of the month, and that it takes up to 3
days for an Authorised txn to be marked Posted.

- Statement 1: Jan 2nd - Feb 1st
- Statement 2: Feb 2nd - Mar 1st
- Statement 3: Mar 2nd - Apr 1st

Let's say you're aiming to get all txns for the month of Feb (Feb 1st - last). If you download on:

- Mar 1st: You'll miss Authorised txns from last few days of Feb
- Mar 2nd / 3rd: The "last statement" is now considered Statement 2, so you'll miss txns from Feb
  1st, and you'll still miss Authorized txns from last few days of Feb
- Mar 4th: The "last statement" is now considered Statement 2, so you'll miss txns from Feb 1st

So you can't do a monthly download and still get all txns. Instead, you need to download at least 2x
/ month (e.g. Mar 1st and 4th), and deduplicate txns that get downloaded twice.

#### When this issue wouldn't apply

We can avoid this issue if your statement _ends_ X days after the end of the month, where X > 3 (the
Authorized --> Posted delay). E.g. if your statement is from 5th to 4th:

- Statement 1: Jan 5th - Feb 4th
- Statement 2: Feb 5th - Mar 4th
- Statement 3: Mar 5th - Apr 4th

You can reliably download on Mar 4th:

- The "last statement" is considered Statement 1, and includes the early days of Feb
- The "current statement" is considered Statement 2, and includes the later days of Feb
- Mar 4th is > 3 days away from the last days of Feb, meaning Authorized txns would have had enough
  time to become Posted
