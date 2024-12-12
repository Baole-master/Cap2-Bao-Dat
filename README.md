
# Xậy dựng hệ ETL trên nền tăng AWS Cloud
![0001-introduction](https://github.com/user-attachments/assets/feef186c-aa78-4ddc-9e33-a608fcd0c51b)


This report presents the development of an ETL Pipeline system on the AWS Cloud platform, aiming to automate the processes of data collection, processing, and analysis to support businesses in optimizing their strategic decisions. The system consists of three main stages: extracting data from PostgreSQL and other sources to store in Amazon S3; transforming data using AWS Glue through steps such as cleaning, standardizing, and processing; and finally, loading the processed data into Amazon Redshift for analysis and reporting. Tools such as AWS Glue, Amazon Redshift, Streamlit, and Tableau are utilized to manage data and generate visual reports, enabling businesses to make quick and accurate decisions. The results demonstrate that the ETL system not only fully automates the workflow but also ensures high efficiency in handling large datasets, supports real-time analytics, and meets the scalability demands of enterprises.

# (Phase 1): Extract - Transform - Load (ETL) (Project focus)
**The Analysis And Forecast Of Perfume Demand Project:** requires data on products, customers and purchase information. For the project we aggregate data from different sources from python's faker library, API and kaggle.
![etl-process-extract-transform-load-1](https://github.com/user-attachments/assets/0b96e37a-0af1-40e4-bb29-19c7b0da4754)
# (Phase 2): Overview and Forecasting 
**Visualization and Forecasting for Project:** Here we use a web framework Streamlit to help us present the results of the report and forecast. In Streamlit, users can interact with the chart at will and it can work online near realtime.
![download](https://github.com/user-attachments/assets/a0fd844a-418e-4ea5-ac04-cbfd1bf1ea3c)
## Team members
* **Team Leader/Analytics Engineer/BI Engineer:** Oversee the entire project, planning and support on both technical and non-technical aspects.
  * [Lê Ngọc Bảo]: Data Science & Business Analytics at DUE
* **Other members:** Conduct data discovery and documentation, uncover business insights and provide client-driven recommendations.
  * [Nguyễn Sỹ Tiến Đạt]: Data Science & Business Analytics at DUE

## About the data
### Data Source
#### (Data is taken from Kaggle and API from Ebay e-commerce platform)
# ETL Pipeline: Data Attributes and Relationships

## Data Attributes

### Category
- **category_id**: Unique identifier for the category (Primary Key).
- **name**: Name of the category.
- **last_update**: Timestamp of the last update.

### Film
- **film_id**: Unique identifier for the film (Primary Key).
- **title**: Name of the film.
- **description**: Description of the film.
- **release_year**: Year the film was released.
- **language_id**: Language identifier for the film.
- **rental_duration**: Duration for which the film can be rented.
- **rental_rate**: Rental price for the film.
- **length**: Length of the film.
- **replacement_cost**: Cost to replace the film.
- **rating**: Rating of the film.
- **special_features**: Special features included.
- **last_update**: Timestamp of the last update.

### Inventory
- **inventory_id**: Unique identifier for inventory (Primary Key).
- **film_id**: Identifier for the film (Foreign Key).
- **store_id**: Identifier for the store.
- **last_update**: Timestamp of the last update.

### Rental
- **rental_id**: Unique identifier for the rental (Primary Key).
- **rental_date**: Date of the rental.
- **inventory_id**: Identifier for inventory (Foreign Key).
- **customer_id**: Identifier for the customer.
- **return_date**: Date of return.
- **staff_id**: Identifier for the staff handling the rental.
- **last_update**: Timestamp of the last update.

### Payment
- **payment_id**: Unique identifier for the payment (Primary Key).
- **customer_id**: Identifier for the customer.
- **staff_id**: Identifier for the staff processing the payment.
- **rental_id**: Identifier for the rental.
- **amount**: Amount paid.
- **payment_date**: Date of payment.

### Customer
- **customer_id**: Unique identifier for the customer (Primary Key).
- **store_id**: Identifier for the associated store.
- **first_name**, **last_name**: Name of the customer.
- **email**: Email address of the customer.
- **address_id**: Identifier for the address.
- **activebook**: Activity status.
- **create_date**: Creation date of the customer record.
- **last_update**: Timestamp of the last update.
- **active**: Status of the customer's account.

### Address
- **address_id**: Unique identifier for the address (Primary Key).
- **address**, **address2**: Address details.
- **district**: District.
- **city_id**: Identifier for the city.
- **postal_code**: Postal code.
- **phone**: Phone number.
- **last_update**: Timestamp of the last update.

### City
- **city_id**: Unique identifier for the city (Primary Key).
- **city**: Name of the city.
- **country_id**: Identifier for the country.
- **last_update**: Timestamp of the last update.

### Country
- **country_id**: Unique identifier for the country (Primary Key).
- **country**: Name of the country.
- **last_update**: Timestamp of the last update.

### Staff
- **staff_id**: Unique identifier for the staff (Primary Key).
- **first_name**, **last_name**: Name of the staff member.
- **address_id**: Identifier for the address.
- **email**: Email address of the staff member.
- **store_id**: Identifier for the store.
- **active**: Activity status.
- **username**, **password**: Login information.
- **picture**: Profile picture of the staff member.
- **last_update**: Timestamp of the last update.

### Store
- **store_id**: Unique identifier for the store (Primary Key).
- **manager_staff_id**: Identifier for the store manager.
- **address_id**: Identifier for the store's address.
- **last_update**: Timestamp of the last update.

### Language
- **language_id**: Unique identifier for the language (Primary Key).
- **name**: Name of the language.
- **last_update**: Timestamp of the last update.

### Film Category
- **film_id**: Unique identifier for the film (Primary Key).
- **category_id**: Unique identifier for the category (Primary Key).
- **last_update**: Timestamp of the last update.

### Film Actor
- **actor_id**: Unique identifier for the actor (Primary Key).
- **film_id**: Unique identifier for the film (Primary Key).
- **last_update**: Timestamp of the last update.

### Actor
- **actor_id**: Unique identifier for the actor (Primary Key).
- **first_name**, **last_name**: Name of the actor.
- **last_update**: Timestamp of the last update.

---

## Data Relationships

### Category
- **Many-to-Many** with `Film` via `Film Category`.
  - Example: Action films like *Die Hard* or *Mad Max*.

### Film
- **Many-to-Many** with `Category` via `Film Category`.
- **Many-to-Many** with `Actor` via `Film Actor`.
  - Example: *Inception* includes Leonardo DiCaprio and Joseph Gordon-Levitt.
- **One-to-Many** with `Inventory`.

### Inventory
- **One-to-Many** with `Rental`.
- **Many-to-One** with `Film`.
- **Many-to-One** with `Store`.

### Rental
- **Many-to-One** with `Inventory`.
- **Many-to-One** with `Customer`.
- **Many-to-One** with `Staff`.

### Payment
- **Many-to-One** with `Rental`.
- **Many-to-One** with `Customer`.
- **Many-to-One** with `Staff`.

### Customer
- **One-to-Many** with `Rental`.
- **One-to-Many** with `Payment`.
- **Many-to-One** with `Store`.

### Address
- **Many-to-One** with `Customer`.
- **Many-to-One** with `Staff`.

### City
- **One-to-Many** with `Address`.

### Country
- **One-to-Many** with `City`.

### Staff
- **Many-to-One** with `Store`.
- **One-to-Many** with `Rental`.
- **One-to-Many** with `Payment`.

### Store
- **One-to-Many** with `Inventory`.
- **One-to-Many** with `Staff`.

### Language
- **One-to-Many** with `Film`.

### Film Category
- **Many-to-One** with `Film`.
- **Many-to-One** with `Category`.

### Film Actor
- **Many-to-One** with `Film`.
- **Many-to-One** with `Actor`.

### Actor
- **One-to-Many** with `Film Actor`.

# Forecast And Business Plan Proposal

## Temperature and product type:
### Northern region (Hanoi, Hai Phong):
- The lowest average temperature ranges from **19.93°C** to **20.64°C**, indicating that winter is colder than other regions.
![image](https://github.com/user-attachments/assets/0c9cfb48-fc0f-4b4b-954d-10a5f7675a5e)
![image](https://github.com/user-attachments/assets/dff4300c-3fb9-4e4e-b4d6-f790fdf4262d)

- Here, with the seasonal nature of temperature, we will look at the past temperature in **Ha Noi** and **Hai Phong** from 12/2023 to the end of 02/2024.

![image](https://github.com/user-attachments/assets/e00f07c2-3462-4cea-81fe-6e88e66cc150)
![image](https://github.com/user-attachments/assets/1e062c7f-3458-4437-a279-96ff3bea7aeb)

- From the forecast temperature and the past temperature of **Ha Noi** and **Hai Phong** in the period from 12/2023 to the end of 02/2024, the temperature is very low and it always fluctuates with the temperature from **14.9°C** đến **22.15°C**  and in this temperature range with the type of product suitable for this customer is similar to our forecast that **Eau De Parfum** and **Perfume** have a concentration of **Eau De Parfum (15-20%)** and **Perfume (20-30%)** from 15-30%.

![image](https://github.com/user-attachments/assets/a749f336-1195-4134-a880-1cf2efeb226e)

- In the Northern market at 2 locations, **Ha Noi** and **Hai Phong**, **Eau De Parfum** is more dominant than **Perfume** and people prefer to use **Eau De Parfum**.
### Central region (Da Nang, Hue):
- The lowest average temperature ranges from **22.64°C (Hue)** to **25.45°C (Nha Trang)**, warmer than the North.

![image](https://github.com/user-attachments/assets/49ffb7a3-474f-4d08-b706-4ecd7304ee75)
![image](https://github.com/user-attachments/assets/3dd026db-3858-45c8-8582-67921173dab3)

- Here, with the seasonal nature of temperature, we will look at the past temperature in **Hue** and **Da Nang** from December 2023 to the end of February 2024.

![image](https://github.com/user-attachments/assets/73fa2a76-fd6b-40aa-8f6d-f89911c3b8a4)
![image](https://github.com/user-attachments/assets/913ca52f-53d4-4b08-ace0-0f15fbbac987)

- From the forecast temperature and the past temperature of **Hue**, **Da Nang** in the period of 12/2023 to the end of 02/2024, the average temperature is warmer than the North and it always goes sideways with the temperature from **20°C** to **25°C** and in this temperature range with the type of product suitable for this customer is similar to our forecast of **Eau De Toilette** and **Eau De Parfum** with the concentration of **Eau De Toilette (5-15%)** and **Eau De Parfum (15-20%)** from 5-20%.

![image](https://github.com/user-attachments/assets/1a5d3134-3623-4e95-a66c-70500e15040c)

- In **Da Nang** market, **Eau De Toilette** is higher than **Eau De Parfum**, but in **Hue** market, there is another advantage, **Eau De Parfum** is much higher than **Eau De Toilette**.
 ### Southern and South Central region (Ho Chi Minh, Ca Mau, Nha Trang):
- The lowest average temperature ranges from **26.16°C** to **26.99°C**, higher than both the North and Central regions, reflecting the typical hot and humid tropical monsoon climate.

![image](https://github.com/user-attachments/assets/354cd4ec-8286-4ca3-bf5c-f2c22fc278ec)
![image](https://github.com/user-attachments/assets/17fabe5c-cd41-4fe2-9d56-f2216fb52e3c)
![image](https://github.com/user-attachments/assets/626981b2-6580-4478-8157-ca5692ae2822)

- Here, with the seasonal nature of temperature, we will look at the past temperature in **Ho Chi Minh**, **Ca Mau** and **Nha Trang** from December 2023 to the end of February 2024.

![image](https://github.com/user-attachments/assets/24882092-c998-4d3d-9540-f20dc8ecfd29)
![image](https://github.com/user-attachments/assets/0c1d16ed-49af-4e90-8fb6-082f1a79326b)
![image](https://github.com/user-attachments/assets/85e5768e-5b65-4d81-8771-a47025bf2bc0)

- From the forecast temperature and historical temperature of **Ho Chi Minh City**, **Ca Mau** and **Nha Trang** in the period from 12/2023 to the end of 02/2024, the temperature is high, slightly higher than that of the North and Central regions and it always goes sideways with the temperature from **27°C** to **29°C** and is in this temperature range with **Eau De Cologne** and **Eau De Toilette** with concentration of **Eau De Cologne (2-4%)** and **Eau De Toilette (5-15%)**.

![image](https://github.com/user-attachments/assets/51a86a5b-d0a2-49a2-99bf-866d11954630)

- In the Southern and South Central markets, people use two types of perfumes: **Eau De Cologne** and **Eau De Toilette**, but consumers prefer **Eau De Toilette**.
## Manufacturer:
- With big perfume manufacturers like **Dior** and **Chanel** will be the top priority because it has a large traffic compared to other perfume brands.

![image](https://github.com/user-attachments/assets/0cd7ab80-7ce9-4ebf-98cc-24a44467294e)
![image](https://github.com/user-attachments/assets/924d11cf-30b9-4b7f-99d3-ff8e9820aa01)
![image](https://github.com/user-attachments/assets/be2d3ac1-f6b1-4c82-ab6a-a326be9c0f91)
![image](https://github.com/user-attachments/assets/094b6b65-81c0-431e-aa33-33f836066f01)

- With the search volume for products of two big brands like **Dior** and **Chanel** in the past being very high, it can be said that it is double that of other brands. With the forecast for the import and distribution plan for the next 90 days, the forecast for the search volume of Dior and Chanel perfumes tends to increase well, with Gucci and Bharara also being two famous brands in the market but the forecast for the next 90 days is that the search volume will gradually decrease.
## Business Plan Recommendations for next 90 days:
### Manufacturer:
- **Focus on two major perfume brands:** **Dior** and **Chanel**.
### Product Type:
 **Northern Region (Hanoi, Hai Phong):**
- Advertise and reach customers with **Eau De Parfum (15-20%)** concentration and **Perfume (20-30%)** concentration products.
- Prioritize importing and marketing **Eau De Parfum** as the main product.

 **Central region (Da Nang, Hue):**
- Advertise and reach customers with **Eau De Toilette (5-15%)** concentration and **Eau De Parfum (15-20%)** concentration products.
- Prioritize importing and marketing **Eau De Parfum** in **Hue** as the main product.

 **Southern and South Central region (Ho Chi Minh, Ca Mau, Nha Trang):**
- Advertise and reach customers with **Eau De Cologne (2-4%)** concentration and **Eau De Toilette (5-15%)** concentration products.
- Prioritize importing and marketing **Eau De Toilette** in **Ho Chi Minh** as the main product.
## Project Flow Chart

## Project Steps
### 1. Extract - Transform - Load (ETL) - ETL Pipeline
The pipeline helps update and store data contained in the `ETL_data.ipynb` file. The data in this system is run automatically by the APScheduler library, which synthesizes product data files, data from libraries and APIs, then transforms and extracts it and stores it in the local Database.

**- Data Extraction:**
+ Synthesize product data from the `data_sanpham.csv` file.
+ Combine MeteoStat and Faker libraries to create simulated customer data, orders, detailed orders and nominatim API to get data on the coordinates of cities.

**- Data Cleaning:**
+ Use the pandas library to clean the data in the `data_sanpham.csv` file such as removing duplicates, handling null values ​​and handling outliers

**- Feature Engineering and Transformation:**
+ Here I use 2 models, ARIMA and LSTM, extracting values ​​and using models in the code in the `Metric.py` file
+ Training the LSTM model to predict the weather in the file `Modeltrain_LSTM.ipynb`
#### 1.1 Usage
Here are the steps to setup and run the pipeline:
1. Need a code running environment like VS Code or Jupyter Notebook, ... and download the above files to the same place as the code running environment folder.
2. Open the `ETL_data.ipynb` file and need to install the necessary libraries first, open your SQL server and fill in your server information in the section that needs to be replaced in the `ETL_data.ipynb` file and run it, because it is scheduled to run every 5 minutes so you need to wait.
### 2. Data Analysis & Predictive Modelling
- We present actionable results overview charts for senior executives on the Dashboard side, and on the Analytics side we include more in-depth data on customers, products, and orders.

![image](https://github.com/user-attachments/assets/751b7d9b-cfc4-4019-8b58-33e32f1d8bc0)
- With the forecasting model we are using to predict what the weather will be like in the next 90 days and what the search traffic for keywords related to the product will be in the coming months. This data combined with the company's historical data will help senior management make better decisions.

![image](https://github.com/user-attachments/assets/00562da4-6484-4c9c-811e-f656163b43d5)
### 3. Project overview video
[![End to end Project DataScience ( Analysis And Forecast Of Perfume Demand)](https://img.youtube.com/vi/<StL3QEe50uQ>/0.jpg)](https://youtu.be/StL3QEe50uQ)
