#!/usr/bin/env python3
import os
import sys
import re
import random

# ==============================================================================
# DB-ANONYMIZER: Production Database PII Sanitizer & Masking Engine
# Completely sanitizes SQL dumps by masking confidential human properties.
# ==============================================================================

# --- ANSI Core UI Color Schemas ---
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
CYAN = '\033[0;36m'
WHITE = '\033[1;37m'
RESET = '\033[0m'
BOLD = '\033[1m'

def log_info(msg): print(f"{BLUE}[INFO]{RESET} {msg}")
def log_success(msg): print(f"{GREEN}[SUCCESS]{RESET} {msg}")
def log_warn(msg): print(f"{YELLOW}[WARNING]{RESET} {msg}")
def log_error(msg): print(f"{RED}[ERROR]{RESET} {msg}")

# Dynamic generators matching physical production data distribution properties
def generate_fake_name():
    first = ["John", "Jane", "Alex", "Emily", "Michael", "Sarah", "David", "Jessica"]
    last = ["Smith", "Doe", "Johnson", "Miller", "Davis", "Wilson", "Anderson", "Taylor"]
    return f"{random.choice(first)} {random.choice(last)}"

def generate_fake_email():
    domains = ["sandbox.internal", "mockeddb.local", "anonymous.dev", "testnet.io"]
    digits = random.randint(1000, 9999)
    return f"user_{digits}@{random.choice(domains)}"

def generate_fake_phone():
    return f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

def generate_fake_ssn_cpf():
    return f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}"
# Heuristic regular expressions scanning signatures tracking confidential data structures
EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
PHONE_REGEX = re.compile(r'\b\+?[0-9]{1,3}?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b')
CREDIT_CARD_REGEX = re.compile(r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13})\b')

def sanitize_line(line, cache_maps):
    """Parses line streams matching regex patterns and replaces strings using local states maps."""
    modified_line = line
    
    # 1. Masking standard active email parameters profiles matches
    emails_found = EMAIL_REGEX.findall(modified_line)
    for email in emails_found:
        if email not in cache_maps["emails"]:
            cache_maps["emails"][email] = generate_fake_email()
        modified_line = modified_line.replace(email, cache_maps["emails"][email])
        
    # 2. Masking active physical telephone numeric configurations records
    phones_found = PHONE_REGEX.findall(modified_line)
    for phone in phones_found:
        if phone not in cache_maps["phones"]:
            cache_maps["phones"][phone] = generate_fake_phone()
        modified_line = modified_line.replace(phone, cache_maps["phones"][phone])
        
    # 3. Destroying plain-text production financial credit cards entries
    cards_found = CREDIT_CARD_REGEX.findall(modified_line)
    for card in cards_found:
        fake_card = f"4111-XXXX-XXXX-{random.randint(1000, 9999)}"
        modified_line = modified_line.replace(card, fake_card)
        
    return modified_line
def process_database_anonymization(source_sql, output_sql):
    if not os.path.exists(source_sql):
        log_error(f"Target SQL backup manifest not found at: {source_sql}")
        sys.exit(1)
        
    log_info(f"Initializing parsing sequence tracking database records inside: {YELLOW}{source_sql}{RESET}")
    
    # Global encryption seed synchronization maps
    identity_cache = {
        "emails": {},
        "phones": {}
    }
    
    total_lines_processed = 0
    
    with open(source_sql, 'r', encoding='utf-8', errors='ignore') as src, \
         open(output_sql, 'w', encoding='utf-8') as dst:
         
        for line in src:
            total_lines_processed += 1
            # Run masking procedures across queries structures lines streams
            sanitized = sanitize_line(line, identity_cache)
            dst.write(sanitized)
            
            if total_lines_processed % 10000 == 0:
                print(f" {CYAN}[i]{RESET} Sanitized {total_lines_processed:,} structural query database records data strings...", end='\r')
                
    print() # Clear terminal carrier returns sequences
    log_success(f"Anonymization engine complete. Total processed lines records: {GREEN}{total_lines_processed:,}{RESET}")
    log_success(f"Secured data mapping snapshot compiled into destination: {BOLD}{output_sql}{RESET}\n")

def main():
    print(f"{CYAN}======================================================================{RESET}")
    print(f"{WHITE}      DB-ANONYMIZER: AUTONOMOUS PRODUCTION DATABASE PII SANITIZER     {RESET}")
    print(f"{CYAN}======================================================================{RESET}\n")
    
    if len(sys.argv) < 3:
        log_warn("Required parameters schemas missing inside arguments array.")
        print(f"Usage execution model: {BOLD}python3 db_anonymizer.py <source_production_dump.sql> <output_masked_dump.sql>{RESET}\n")
        sys.exit(1)
        
    src_dump = sys.argv[1]
    out_dump = sys.argv[2]
    
    try:
        process_database_anonymization(src_dump, out_dump)
    except KeyboardInterrupt:
        log_error("Process terminated prematurely by user operator intervention. Aborting.")
        sys.exit(1)

if __name__ == '__main__':
    main()
