import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, SimpleRNN, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import warnings

# Ignore warnings
warnings.filterwarnings("ignore")

# Set page configuration
st.set_page_config(page_title="RNN Forecasting", layout="wide")

st.title("RNN Forecasting")
st.write("This page performs RNN forecasting with optimized settings.")

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

    st.success("Default files loaded successfully.")
    
except Exception as e:
    st.error(f"Error loading default files: {e}")
    st.stop()

# Prepare data for RNN forecasting
try:
    data = weekly_sales['sales_amount'].values.reshape(-1, 1)

    # Normalize data
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(data)

    # Create time series sequences
    def create_sequences(data, sequence_length):
        X, y = [], []
        for i in range(len(data) - sequence_length):
            X.append(data[i:i + sequence_length])
            y.append(data[i + sequence_length])
        return np.array(X), np.array(y)

    sequence_length = 4
    X, y = create_sequences(data_scaled, sequence_length)

    # Split data into training and testing sets
    split_ratio = 0.8
    split_index = int(len(X) * split_ratio)
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    # Build RNN model
    model = Sequential()
    model.add(SimpleRNN(units=64, activation='relu', return_sequences=True, input_shape=(sequence_length, 1)))
    model.add(Dropout(0.2))
    model.add(SimpleRNN(units=32, activation='relu', return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))

    # Compile model
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train model
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    history = model.fit(X_train, y_train, epochs=100, batch_size=16, validation_data=(X_test, y_test), callbacks=[early_stopping], verbose=1)

    # Predict on test data
    predicted_scaled = model.predict(X_test)
    predicted = scaler.inverse_transform(predicted_scaled)

    # Reverse scale y_test
    y_test_original = scaler.inverse_transform(y_test)

    # Forecast future steps
    future_steps = 12
    future_data = data_scaled[-sequence_length:]
    future_predictions = []
    for _ in range(future_steps):
        future_pred = model.predict(future_data[np.newaxis, :, :])
        future_predictions.append(future_pred[0, 0])
        future_data = np.vstack([future_data[1:], future_pred])

    # Convert future predictions back to original scale
    future_predictions_original = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

    # Create forecast index
    forecast_index = pd.date_range(start=weekly_sales['week'].iloc[-1] + pd.Timedelta(weeks=1), periods=future_steps, freq='W')

    # Plot results
    plt.figure(figsize=(12, 6))
    plt.plot(weekly_sales['week'], weekly_sales['sales_amount'], label='Actual', color='blue', marker='o')
    plt.plot(weekly_sales['week'][-len(y_test_original):], predicted, label='Predicted', color='red', linestyle='--', marker='o')
    plt.plot(forecast_index, future_predictions_original, label='Future Forecast', color='green', linestyle='--', marker='o')
    plt.axvline(x=weekly_sales['week'].iloc[-1], color='orange', linestyle='--', label='Forecast Start')
    plt.title("RNN Forecast")
    plt.xlabel("Week")
    plt.ylabel("Sales Amount")
    plt.legend()
    plt.grid()
    st.pyplot(plt)

    # Display forecast results
    forecast_results = pd.DataFrame({
        'Date': forecast_index,
        'Forecasted Sales': future_predictions_original.flatten()
    })
    st.write("Forecasted Results:")
    st.dataframe(forecast_results)
except Exception as e:
    st.error(f"Error during RNN forecasting: {e}")
