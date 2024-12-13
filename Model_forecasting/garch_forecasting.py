import streamlit as st
import pandas as pd
import numpy as np
from arch import arch_model
import matplotlib.pyplot as plt
import warnings

# Ignore warnings
warnings.filterwarnings("ignore")

# Set page configuration
st.set_page_config(page_title="GARCH Forecasting", layout="wide")

st.title("GARCH Forecasting")
st.write("This page performs GARCH forecasting with parameter optimization.")

# Load default data
try:
    # Load fact_sales and dim_date
    fact_sales = pd.read_csv(r"C:\\Users\\ADMIN\\.ssh\\dvdrental\\factSales.csv")
    dim_date = pd.read_csv(r"C:\\Users\\ADMIN\\.ssh\\dvdrental\\dimDate.csv")

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
    weekly_sales['log_sales_amount_diff'] = weekly_sales['log_sales_amount'].diff().dropna()

    st.success("Default files loaded successfully.")
    
except Exception as e:
    st.error(f"Error loading default files: {e}")
    st.stop()

# Perform GARCH forecasting
if 'log_sales_amount_diff' in weekly_sales.columns:
    st.write("Performing GARCH Forecasting...")
    try:
        data = weekly_sales['log_sales_amount_diff'].dropna()

        # Define optimization function for GARCH parameters
        def optimize_garch(data, max_p=5, max_q=5):
            best_aic = float("inf")
            best_p, best_q = None, None
            best_model = None

            for p in range(1, max_p + 1):
                for q in range(1, max_q + 1):
                    try:
                        model = arch_model(data, vol='Garch', p=p, q=q, mean='AR', lags=1)
                        result = model.fit(disp="off")
                        if result.aic < best_aic:
                            best_aic = result.aic
                            best_p, best_q = p, q
                            best_model = result
                    except:
                        continue

            return best_p, best_q, best_aic, best_model

        # Optimize GARCH parameters
        best_p, best_q, best_aic, garch_fit = optimize_garch(data)

        # Display best parameters
        st.write(f"Best GARCH Model: p={best_p}, q={best_q}, AIC={best_aic}")
        st.text(garch_fit.summary())

        # Forecast
        forecast_horizon = 30  # Forecast for 30 weeks
        garch_forecast = garch_fit.forecast(horizon=forecast_horizon)

        # Get forecasted variance and mean
        forecast_variance = garch_forecast.variance.iloc[-1].values
        forecast_mean = garch_forecast.mean.iloc[-1].values

        # Transform back to original scale
        last_actual_value = weekly_sales['sales_amount'].iloc[-1]
        forecast_cumsum = np.cumsum(forecast_mean)
        forecast_values_transformed = np.exp(forecast_cumsum + np.log(last_actual_value))

        # Create forecast index
        forecast_index = pd.date_range(
            start=weekly_sales['week'].iloc[-1] + pd.Timedelta(weeks=1),
            periods=forecast_horizon,
            freq='W'
        )

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
        plt.title("GARCH Forecast")
        plt.xlabel("Week")
        plt.ylabel("Sales Amount")
        plt.legend()
        plt.grid()
        st.pyplot(plt)

    except Exception as e:
        st.error(f"Error during GARCH forecasting: {e}")
else:
    st.error("The dataset must contain 'log_sales_amount_diff' column for forecasting.")
