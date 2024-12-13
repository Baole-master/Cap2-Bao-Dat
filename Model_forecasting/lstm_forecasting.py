import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Bidirectional, BatchNormalization
from keras.regularizers import l1_l2
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
import warnings

# Ignore warnings
warnings.filterwarnings("ignore")

# Set page configuration
st.set_page_config(page_title="LSTM Forecasting", layout="wide")

st.title("LSTM Forecasting")
st.write("This page performs LSTM forecasting with optimized architecture.")

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

    # Handle missing or invalid values
    if weekly_sales['sales_amount'].isnull().any():
        st.warning("Missing values found in 'sales_amount'. Replacing with 0.")
        weekly_sales['sales_amount'].fillna(0, inplace=True)

    st.success("Default files loaded successfully.")
    
except Exception as e:
    st.error(f"Error loading default files: {e}")
    st.stop()

# Prepare data for LSTM
try:
    data = weekly_sales[['week', 'sales_amount']].copy()
    data.set_index('week', inplace=True)

    # Normalize data
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(data)

    # Create dataset for LSTM
    def create_dataset(dataset, look_back=4):
        X, y = [], []
        for i in range(len(dataset) - look_back):
            X.append(dataset[i:i + look_back, 0])
            y.append(dataset[i + look_back, 0])
        return np.array(X), np.array(y)

    look_back = 4
    X, y = create_dataset(data_scaled, look_back)

    # Reshape X for LSTM
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    # Split into train and test sets
    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    # Build LSTM model
    model = Sequential()

    # Bidirectional LSTM layers
    model.add(Bidirectional(LSTM(units=128, return_sequences=True, input_shape=(look_back, 1), kernel_regularizer=l1_l2(0.01))))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))

    model.add(Bidirectional(LSTM(units=64, return_sequences=False, kernel_regularizer=l1_l2(0.01))))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))

    # Dense layers
    model.add(Dense(units=128, activation='relu'))
    model.add(Dense(units=1))

    # Compile model
    optimizer = Adam(learning_rate=0.0005)
    model.compile(optimizer=optimizer, loss='mean_squared_error')

    # Train model
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    history = model.fit(
        X_train, y_train,
        epochs=200,
        batch_size=32,
        validation_data=(X_test, y_test),
        callbacks=[early_stopping],
        verbose=1
    )

    # Predict on test data
    y_pred_test = model.predict(X_test)
    y_pred_test_rescaled = scaler.inverse_transform(np.concatenate((y_pred_test, np.zeros_like(y_pred_test)), axis=1))[:, 0]

    # Forecast future values
    future_steps = 30
    future_forecast = []
    last_input = X[-1]

    for _ in range(future_steps):
        next_pred = model.predict(last_input.reshape(1, look_back, 1))
        future_forecast.append(next_pred[0, 0])
        last_input = np.append(last_input[1:], next_pred[0, 0]).reshape(look_back, 1)

    future_forecast_rescaled = scaler.inverse_transform(np.concatenate((np.array(future_forecast).reshape(-1, 1), np.zeros_like(np.array(future_forecast).reshape(-1, 1))), axis=1))[:, 0]

    # Create forecast index
    forecast_index = pd.date_range(
        start=data.index[-1] + pd.Timedelta(weeks=1),
        periods=future_steps,
        freq='W'
    )

    # Plot results
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['sales_amount'], label='Actual', color='blue', marker='o')
    plt.plot(data.index[-len(y_pred_test_rescaled):], y_pred_test_rescaled, label='Test Forecast', color='green', marker='o')
    plt.plot(forecast_index, future_forecast_rescaled, label='Future Forecast', color='red', linestyle='--', marker='o')
    plt.axvline(x=data.index[-1], color='orange', linestyle='--', label='Forecast Start')
    plt.title('Weekly Sales Forecast with LSTM')
    plt.xlabel('Week')
    plt.ylabel('Sales Amount')
    plt.legend()
    plt.grid()
    st.pyplot(plt)

    # Display forecast results
    forecast_results = pd.DataFrame({
        'Date': forecast_index,
        'Forecasted Sales': future_forecast_rescaled.flatten()
    })

    st.write("Future Forecasted Results:")
    st.dataframe(forecast_results)

except Exception as e:
    st.error(f"Error during LSTM forecasting: {e}")
