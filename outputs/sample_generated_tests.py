import pytest
from sample_projects.banking.banking import process_loan, transfer_funds

# Auto-Generated AI Test for process_loan
def test_process_loan_denied_low_score():
    assert process_loan(50000, 550) == False

def test_process_loan_denied_high_amount():
    assert process_loan(150000, 650) == False

def test_process_loan_approved():
    assert process_loan(50000, 750) == True

# Auto-Generated AI Test for transfer_funds
def test_transfer_funds_success():
    accounts = {"A": 1000, "B": 500}
    assert transfer_funds("A", "B", 200, accounts) == True
    assert accounts["A"] == 800
    assert accounts["B"] == 700

def test_transfer_funds_insufficient():
    accounts = {"A": 1000, "B": 500}
    assert transfer_funds("A", "B", 1200, accounts) == False
    assert accounts["A"] == 1000
    assert accounts["B"] == 500
