import streamlit as st
import pandas as pd

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

# Define function to determine required pre-tax income to get $80K after tax
def get_required_income(brackets, target_net_income, cpp_contrib=0):
    """Finds the required pre-tax income to achieve a target after-tax income."""
    income = target_net_income + cpp_contrib  # Start with target + CPP estimate
    step = 100  # Incremental adjustment step

    while True:
        tax = calculate_taxes(income, brackets)
        net_income = income - tax - cpp_contrib

        if abs(net_income - target_net_income) < 100:  # Close enough to $80K
            return income, tax

        income += step

# Streamlit User Interface
st.title('Tax Model: Salary vs Dividends')
st.write("This tool helps you calculate the best tax strategy for salary vs dividends.")

salary_input = st.number_input('Enter Salary (in CAD)', min_value=0, value=68500)
target_income = st.number_input('Enter Desired After-Tax Income (in CAD)', min_value=0, value=80000)

salary_1, tax_1 = get_required_income(TAX_BRACKETS_SALARY, target_income, CPP_MAX)
cpp_1 = CPP_MAX
net_income_1 = salary_1 - tax_1 - cpp_1

salary_2 = CPP_THRESHOLD
cpp_2 = CPP_MAX
remaining_needed = target_income - (salary_2 - calculate_taxes(salary_2, TAX_BRACKETS_SALARY) - cpp_2)
dividend_2, tax_div_2 = get_required_income(TAX_BRACKETS_DIVIDEND, remaining_needed)
personal_tax_2 = calculate_taxes(salary_2, TAX_BRACKETS_SALARY) + tax_div_2
net_income_2 = salary_2 + dividend_2 - personal_tax_2 - cpp_2

dividend_3, tax_3 = get_required_income(TAX_BRACKETS_DIVIDEND, target_income)
cpp_3 = 0
net_income_3 = dividend_3 - tax_3

# Displaying results in the app
df = pd.DataFrame({
    "Scenario": ["Salary Only", "Salary + Dividend Mix", "Dividends Only"],
    "Salary Taken": [salary_1, salary_2, 0],
    "Dividends Taken": [0, dividend_2, dividend_3],
    "CPP Contributions": [cpp_1, cpp_2, cpp_3],
    "Personal Taxes Paid": [tax_1, personal_tax_2, tax_3],
    "Net Income After Tax": [net_income_1, net_income_2, net_income_3]
})

st.write(df)
