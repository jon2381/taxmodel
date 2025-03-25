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
    prev_bracket = 0

    for bracket, rate in brackets:
        if income > bracket:
            tax += (bracket - prev_bracket) * rate
            prev_bracket = bracket
        else:
            tax += (income - prev_bracket) * rate
            break

    return tax

def model_income(salary, dividends):
    cpp_contrib = CPP_MAX if salary > CPP_THRESHOLD else 0
    federal_tax = calculate_taxes(salary, FEDERAL_BRACKETS)
    provincial_tax = calculate_taxes(salary, PROVINCIAL_BRACKETS)
    total_tax = federal_tax + provincial_tax
    dividend_tax = calculate_taxes(dividends, PROVINCIAL_BRACKETS) + calculate_taxes(dividends, FEDERAL_BRACKETS) # Dividend taxes are taxed based on both federal and provincial rates
    total_tax += dividend_tax
    net_income = salary + dividends - total_tax - cpp_contrib
    return federal_tax, provincial_tax, dividend_tax, cpp_contrib, total_tax, net_income

# Streamlit User Interface
st.title('Tax Model: Salary and Dividends')
st.write("This tool helps you model the tax impact of salary and dividend income.")

# User input for salary and dividends
salary_input = st.number_input('Enter Salary (in CAD)', min_value=0, value=68500)
dividend_input = st.number_input('Enter Dividend Income (in CAD)', min_value=0, value=0)

# Call the model function to get results
federal_tax, provincial_tax, dividend_tax, cpp_contrib, total_tax, net_income = model_income(salary_input, dividend_input)

# Display results in a dataframe
df = pd.DataFrame({
    "Component": ["Federal Tax", "Provincial Tax", "Dividend Tax", "CPP Contribution", "Total Tax", "Net Income After Tax"],
    "Amount (CAD)": [federal_tax, provincial_tax, dividend_tax, cpp_contrib, total_tax, net_income]
})

st.write(df)

# Visualization: Create a chart for the results
fig, ax = plt.subplots()
labels = ['Federal Tax', 'Provincial Tax', 'Dividend Tax', 'CPP Contribution', 'Net Income After Tax']
values = [federal_tax, provincial_tax, dividend_tax, cpp_contrib, net_income]

ax.bar(labels, values, color=['blue', 'green', 'orange', 'red', 'purple'])
ax.set_title('Tax Model: Salary and Dividends Breakdown')
ax.set_ylabel('Amount (CAD)')
ax.set_ylim(0, max(values) + 10000)

# Display the chart
st.pyplot(fig)
