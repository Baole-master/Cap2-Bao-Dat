import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import itertools
import warnings

# Ignore warnings
warnings.filterwarnings("ignore")

# Set page configuration
st.set_page_config(page_title="ARIMA Forecasting", layout="wide")

st.title("ARIMA Forecasting")
st.write("This page performs ARIMA forecasting with parameter optimization.")

# Load default data
try:
    # Load fact_sales and dim_date
    fact_sales = pd.read_csv(r"C:\Users\ADMIN\.ssh\dvdrental\factSales.csv")
    dim_date = pd.read_csv(r"C:\Users\ADMIN\.ssh\dvdrental\dimDate.csv")

    # Preprocess data
    dim_date['date'] = pd.to_datetime(dim_date['date'])
    sales_data = fact_sales.merge(dim_date, on='date_id')
    sales_data['date'] = pd.to_datetime(sales_data['date'])

    # Aggregate sales data by week
    weekly_sales = sales_data.copy()
    weekly_sales['week'] = sales_data['date'].dt.to_period('W')
    weekly_sales = weekly_sales.groupby('week')['sales_amount'].sum().reset_index()
    weekly_sales['week'] = weekly_sales['week'].dt.to_timestamp()

    # Replace zero sales with a small positive value for log transformation
    weekly_sales['sales_amount_adjusted'] = weekly_sales['sales_amount'].replace(0, 0.01)
    weekly_sales['log_sales_amount'] = np.log(weekly_sales['sales_amount_adjusted'])
    weekly_sales['log_sales_amount_diff'] = weekly_sales['log_sales_amount'].diff()

    st.success("Default files loaded successfully.")
except Exception as e:
    st.error(f"Error loading default files: {e}")
    st.stop()

# Perform ARIMA forecasting
if 'log_sales_amount_diff' in weekly_sales.columns:
    st.write("Performing ARIMA Forecasting...")
    try:
        # Handle missing values in the differenced series
        weekly_sales['log_sales_amount_diff'] = weekly_sales['log_sales_amount_diff'].fillna(0)

        # Define parameter ranges
        p = d = q = range(0, 2)
        param_combinations = list(itertools.product(p, d, q))

        # Grid search for the best parameters
        best_aic = float("inf")
        best_params = None
        best_model = None
        results_summary = []

        for param in param_combinations:
            try:
                model = ARIMA(
                    weekly_sales['log_sales_amount_diff'],
                    order=param
                )
                result = model.fit()

                results_summary.append({
                    'order': param,
                    'AIC': result.aic
                })

                if result.aic < best_aic:
                    best_aic = result.aic
                    best_params = param
                    best_model = result
            except:
                continue

        # Display the best parameters and AIC
        st.write(f"Best ARIMA Parameters: {best_params}")
        st.write(f"Best AIC: {best_aic}")

        # Forecast
        forecast_steps = 30  # Forecast the next 30 weeks
        forecast = best_model.get_forecast(steps=forecast_steps)
        forecast_index = pd.date_range(
            start=weekly_sales['week'].iloc[-1] + pd.Timedelta(weeks=1),
            periods=forecast_steps,
            freq='W'
        )
        forecast_values = forecast.predicted_mean

        # Transform back to original scale
        last_actual_value = weekly_sales['sales_amount'].iloc[-1]
        forecast_cumsum = np.cumsum(forecast_values)
        forecast_values_transformed = np.exp(forecast_cumsum + np.log(last_actual_value))

        # Combine results for display
        combined_results = pd.DataFrame({
            'Date': list(weekly_sales['week']) + list(forecast_index),
            'Actual Sales': list(weekly_sales['sales_amount']) + [np.nan] * len(forecast_values_transformed),
            'Forecasted Sales': [np.nan] * len(weekly_sales['sales_amount']) + list(forecast_values_transformed)
        })
        st.write("Forecasted Results:")
        st.dataframe(combined_results.tail(30))

        # Plot results
        plt.figure(figsize=(12, 6))
        plt.plot(weekly_sales['week'], weekly_sales['sales_amount'], label='Actual', color='blue', marker='o')
        plt.plot(forecast_index, forecast_values_transformed, label='Forecast', color='red', linestyle='--', marker='o')
        plt.axvline(x=weekly_sales['week'].iloc[-1], color='orange', linestyle='--', label='Forecast Start')
        plt.title("ARIMA Forecast")
        plt.xlabel("Week")
        plt.ylabel("Sales Amount")
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

    except Exception as e:
        st.error(f"Error during ARIMA forecasting: {e}")
else:
    st.error("The dataset must contain 'log_sales_amount_diff' column for forecasting.")
