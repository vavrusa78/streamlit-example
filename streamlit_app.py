import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define a function that calculates the cashback data
def calculate_cashback(num_employees, avg_monthly_users_percentage, avg_volume_per_employee, cashback_percentage=2):
    cashback_percentage /= 100
    avg_monthly_users_percentage /= 100
    months = np.arange(1, 13)
    active_users_percentage = np.where(months <= 6, months / 6 * avg_monthly_users_percentage, avg_monthly_users_percentage)
    monthly_active_users = num_employees * active_users_percentage
    individual_monthly_cashback = avg_volume_per_employee * cashback_percentage
    total_monthly_cashback = individual_monthly_cashback * monthly_active_users
    individual_cumulative_cashback = np.cumsum(np.repeat(individual_monthly_cashback, 12))
    total_cumulative_cashback = np.cumsum(total_monthly_cashback)

    cashback_data = pd.DataFrame({
        'Month': months,
        'Active Users': monthly_active_users,
        'Individual Monthly Cashback': individual_monthly_cashback,
        'Total Monthly Cashback': total_monthly_cashback,
        'Individual Cumulative Cashback': individual_cumulative_cashback,
        'Total Cumulative Cashback': total_cumulative_cashback
    })

    return cashback_data

# Use Streamlit to create the web app
st.title('Cashback Calculator')

# Create input fields for the user to enter their data
num_employees = st.number_input('Enter the total number of employees', value=1000)
avg_monthly_users_percentage = st.number_input('Enter the average percentage of active users after 6 months', value=40)
avg_volume_per_employee = st.number_input('Enter the average expenditure per individual', value=5000)

# Call the function to calculate the cashback data
cashback_data = calculate_cashback(num_employees, avg_monthly_users_percentage, avg_volume_per_employee)

# Display the data in a table
st.dataframe(cashback_data)

# Create a plot of the individual and total cumulative cashback
fig, ax = plt.subplots()
ax.plot(cashback_data['Month'], cashback_data['Individual Cumulative Cashback'], label='Individual Cumulative Cashback')
ax.plot(cashback_data['Month'], cashback_data['Total Cumulative Cashback'], label='Total Cumulative Cashback')
ax.set_xlabel('Month')
ax.set_ylabel('Cumulative Cashback')
ax.set_title('Cumulative Cashback over One Year')
ax.legend()
ax.grid(True)

# Display the plot
st.pyplot(fig)
