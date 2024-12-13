import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tbats import TBATS
import warnings

# Ignore warnings
warnings.filterwarnings("ignore")

# Set page configuration
st.set_page_config(page_title="TBATS Forecasting", layout="wide")

st.title("TBATS Forecasting")
st.write("This page performs TBATS forecasting with a seasonal adjustment for shorter cycles.")

# Load default data
try:
    # Load fact_sales and dim_date (Chỉ tải các cột cần thiết)
    fact_sales = pd.read_csv(r"C:\Users\ADMIN\.ssh\dvdrental\factSales.csv", usecols=['date_id', 'sales_amount'])
    dim_date = pd.read_csv(r"C:\Users\ADMIN\.ssh\dvdrental\dimDate.csv", usecols=['date_id', 'date'])

    # Preprocess data
    dim_date['date'] = pd.to_datetime(dim_date['date'])
    sales_data = fact_sales.merge(dim_date, on='date_id')
    sales_data['date'] = pd.to_datetime(sales_data['date'])

    # Aggregate sales data by week
    weekly_sales = sales_data.copy()
    weekly_sales['week'] = sales_data['date'].dt.to_period('W')
    weekly_sales = weekly_sales.groupby('week')['sales_amount'].sum().reset_index()
    weekly_sales['week'] = weekly_sales['week'].dt.to_timestamp()

    # Handle missing or invalid values
    weekly_sales['sales_amount'].fillna(0, inplace=True)

    # Hiển thị trước dữ liệu
    st.success("Default files loaded successfully.")

except Exception as e:
    st.error(f"Error loading default files: {e}")
    st.stop()

# Perform TBATS forecasting
if 'sales_amount' in weekly_sales.columns:
    st.write("Performing TBATS Forecasting...")
    try:
        # Giảm kích thước dữ liệu đầu vào (Lấy mẫu nếu dữ liệu quá lớn)
        if len(weekly_sales) > 100:
            weekly_sales = weekly_sales.tail(100)  # Chỉ lấy 100 tuần gần nhất
            st.warning("Data size is large. Using the last 100 weeks for forecasting.")

        # Define seasonal periods (adjust for shorter cycles)
        seasonal_periods = [4]  # 4 tuần (mùa vụ hàng tháng)

        # Initialize and fit TBATS model (Tắt ARMA nếu không cần)
        tbats_estimator = TBATS(
            seasonal_periods=seasonal_periods,
            use_arma_errors=False  # Tắt ARMA để giảm mức sử dụng RAM
        )
        tbats_model = tbats_estimator.fit(weekly_sales['sales_amount'])

        # Print model summary
        st.write("Model Summary:")
        st.text(tbats_model.summary())

        # Forecast
        forecast_steps = 12  # Dự báo 12 tuần (3 tháng)
        tbats_forecast = tbats_model.forecast(steps=forecast_steps)

        # Create a forecast index
        forecast_index = pd.date_range(
            start=weekly_sales['week'].iloc[-1] + pd.Timedelta(weeks=1),
            periods=forecast_steps,
            freq='W'
        )

        # Combine results for display
        combined_results = pd.DataFrame({
            'Date': list(weekly_sales['week']) + list(forecast_index),
            'Actual Sales': list(weekly_sales['sales_amount']) + [np.nan] * len(tbats_forecast),
            'Forecasted Sales': [np.nan] * len(weekly_sales['sales_amount']) + list(tbats_forecast)
        })

        st.write("Forecasted Results (Last 30 Rows):")
        st.dataframe(combined_results.tail(30))

        # Plot results
        plt.figure(figsize=(10, 5))
        plt.plot(weekly_sales['week'], weekly_sales['sales_amount'], label='Actual', color='blue', marker='o')
        plt.plot(forecast_index, tbats_forecast, label='Forecast', color='red', linestyle='--', marker='o')
        plt.axvline(x=weekly_sales['week'].iloc[-1], color='orange', linestyle='--', label='Forecast Start')
        plt.title("TBATS Forecast")
        plt.xlabel("Week")
        plt.ylabel("Sales Amount")
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

        # Giải phóng các biến không cần thiết
        del tbats_model, tbats_forecast, sales_data

    except Exception as e:
        st.error(f"Error during TBATS forecasting: {e}")
else:
    st.error("The dataset must contain 'sales_amount' column for forecasting.")
