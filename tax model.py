import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Tax rates for Ontario (2024)
TAX_BRACKETS_SALARY = [
    (15000, 0.2),  # Approx. after basic personal amount
    (53359, 0.295),
    (96856, 0.374),
    (150000, 0.434),
    (220000, 0.464),
    (float("inf"), 0.5353),
]

TAX_BRACKETS_DIVIDEND = [
    (15000, 0.0),  # Approx. after basic personal amount
    (53359, 0.078),
    (96856, 0.152),
    (150000, 0.197),
    (220000, 0.216),
    (float("inf"), 0.39),
]

# CPP Contributions
CPP_MAX = 7098  # Max contribution (employer + employee)
CPP_THRESHOLD = 68500  # Max salary for CPP deductions

def calculate_taxes(income, brackets):
    """Calculates tax based on income and bracket rates."""
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

# Define function to model after-tax income based on salary and dividends
def model_income(salary, dividends):
    cpp_contrib = CPP_MAX if salary > CPP_THRESHOLD else 0
    salary_tax = calculate_taxes(salary, TAX_BRACKETS_SALARY)
    dividend_tax = calculate_taxes(dividends, TAX_BRACKETS_DIVIDEND)
    
    # Calculate total tax
    total_tax = salary_tax + dividend_tax
    net_income = salary + dividends - total_tax - cpp_contrib
    return salary_tax, dividend_tax, cpp_contrib, total_tax, net_income

# Streamlit User Interface
st.title('Tax Model: Salary and Dividends')
st.write("This tool helps you model the tax impact of salary and dividend income.")

# User input for salary and dividends
salary_input = st.number_input('Enter Salary (in CAD)', min_value=0, value=68500)
dividend_input = st.number_input('Enter Dividend Income (in CAD)', min_value=0, value=0)

# Call the model function to get results
salary_tax, dividend_tax, cpp_contrib, total_tax, net_income = model_income(salary_input, dividend_input)

# Display results in a dataframe
df = pd.DataFrame({
    "Component": ["Salary", "Dividends", "CPP Contribution", "Total Tax", "Net Income After Tax"],
    "Amount (CAD)": [salary_input, dividend_input, cpp_contrib, total_tax, net_income]
})

st.write(df)

# Visualization: Create a chart for the results
fig, ax = plt.subplots()
labels = ['Salary', 'Dividends', 'CPP Contribution', 'Total Tax', 'Net Income After Tax']
values = [salary_input, dividend_input, cpp_contrib, total_tax, net_income]

ax.bar(labels, values, color=['blue', 'green', 'orange', 'red', 'purple'])
ax.set_title('Tax Model: Salary and Dividends Breakdown')
ax.set_ylabel('Amount (CAD)')
ax.set_ylim(0, max(values) + 10000)

# Display the chart
st.pyplot(fig)

