# 🎭 DB-Anonymizer

A lightweight command-line tool to strip out real user data (PII) from production SQL dumps and replace it with anonymous, realistic data. 

Testing bugs with just two dummy users in your local database doesn't simulate real-world scale, but downloading a production dump with raw customer emails, passwords, and credit cards onto your laptop is a massive security risk (and violates data laws like GDPR or LGPD). 

This script solves that. It streams your giant SQL backup line by line, scrubs sensitive information using fast regex patterns, and creates a clean, anonymous database replica you can run locally without any legal or security headaches.

---

## ⚡ Quick Start

### 1. Grab the Script
Download the standalone Python script directly into your project directory:

```bash
curl -fsSL https://githubusercontent.com -o db_anonymizer.py
```

### 2. Scrub Your Database
Pass your production SQL dump file and define your new output file destination:

```bash
python3 db_anonymizer.py production_backup.sql local_dev_backup.sql
```

---

## 📐 How It Works

The script reads your SQL file line by line instead of loading the whole thing into memory, meaning it won't crash your laptop even if you are processing a 100GB file.

    📂 Open production SQL dump --> 🚀 Read file line by line
    --> Found emails, phones or cards
    
    -- Yes --> 🧠 Extract real data string
    -- No --> 📝 Write line exactly as it is to output file
    
    --> Is this value already in memory?
    -- No --> 🎲 Generate fake phone/email replacement
    -- Yes --> 🔄 Fetch previous fake value replacement
    
    --> 🔒 Swap real data with fake data]
    --> 🎉 Final Output: Safe, anonymous SQL backup
```

---

## 💎 Features

* **Memory Efficient Streaming:** Processes massive production database backups by reading small text chunks. It handles multi-gigabyte files easily on basic laptop hardware.
* **Consistent Data Masking:** If a real email like `user@gmail.com` shows up multiple times across different tables (Users, Logs, Billing), it gets replaced by the exact same fake email string every single time. Your database relationships and foreign keys stay fully intact.
* **Financial Scrubbing:** Automatically spots common credit card number patterns and wipes them out, swapping them for generic test card string footprints.
* **Zero Dependencies:** Written entirely in vanilla Python using native libraries. No third-party packages or heavy node_modules style setups required.

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more info.
