import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Federal and Ontario tax brackets (2024)
FEDERAL_BRACKETS = [
    (15000, 0.15),    # 15% up to 15,000
    (49020, 0.205),   # 20.5% from 15,000 to 49,020
    (98040, 0.26),    # 26% from 49,020 to 98,040
    (151978, 0.29),   # 29% from 98,040 to 151,978
    (float('inf'), 0.33)  # 33% above 151,978
]

PROVINCIAL_BRACKETS = [
    (11865, 0.0505),   # 5.05% up to 11,865
    (23420, 0.0915),   # 9.15% from 11,865 to 23,420
    (47630, 0.1116),   # 11.16% from 23,420 to 47,630
    (95259, 0.1216),   # 12.16% from 47,630 to 95,259
    (150000, 0.1316),  # 13.16% from 95,259 to 150,000
    (float('inf'), 0.1316)  # 13.16% above 150,000
]

# CPP Contributions
CPP_MAX = 7098  # Max contribution (employer + employee)
CPP_THRESHOLD = 68500  # Max salary for CPP deductions

def calculate_taxes(income, brackets):
    """Calculates tax based on income and tax brackets (federal/provincial)."""
    tax = 0
    prev_bracket =_
