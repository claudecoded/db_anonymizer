# Makefile for DB-Anonymizer automation tasks

.PHONY: test run clean help

help:
	@echo "Available commands:"
	@echo "  make run   - Run the anonymizer on the test database"
	@echo "  make test  - Execute automated integrity tests"
	@echo "  make clean - Remove generated mock SQL output files"

run:
	python3 db_anonymizer.py test_database.sql anonymized_output.sql

test:
	python3 -m unittest test_anonymizer.py

clean:
	rm -f anonymized_output.sql
	@echo "Clean complete."
