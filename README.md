
# Xậy dựng hệ ETL trên nền tăng AWS Cloud
![0001-introduction](https://github.com/user-attachments/assets/feef186c-aa78-4ddc-9e33-a608fcd0c51b)


This report presents the development of an ETL Pipeline system on the AWS Cloud platform, aiming to automate the processes of data collection, processing, and analysis to support businesses in optimizing their strategic decisions. The system consists of three main stages: extracting data from PostgreSQL and other sources to store in Amazon S3; transforming data using AWS Glue through steps such as cleaning, standardizing, and processing; and finally, loading the processed data into Amazon Redshift for analysis and reporting. Tools such as AWS Glue, Amazon Redshift, Streamlit, and Tableau are utilized to manage data and generate visual reports, enabling businesses to make quick and accurate decisions. The results demonstrate that the ETL system not only fully automates the workflow but also ensures high efficiency in handling large datasets, supports real-time analytics, and meets the scalability demands of enterprises.

# (Phase 1): Extract - Transform - Load (ETL) (Project focus)
**The Analysis And Forecast Of Perfume Demand Project:** requires data on products, customers and purchase information. For the project we aggregate data from different sources from python's faker library, API and kaggle.
![etl-process-extract-transform-load-1](https://github.com/user-attachments/assets/0b96e37a-0af1-40e4-bb29-19c7b0da4754)
# (Phase 2): Overview and Forecasting 
**Visualization and Forecasting for Project:** Here we use a web framework Streamlit to help us present the results of the report and forecast. In Streamlit, users can interact with the chart at will and it can work online near realtime.
![image](https://github.com/user-attachments/assets/1b1338ec-ea74-4192-a569-ca26519daaf0)
![download](https://github.com/user-attachments/assets/a0fd844a-418e-4ea5-ac04-cbfd1bf1ea3c)
## Team members
* **Team Leader/Analytics Engineer/BI Engineer:** Oversee the entire project, planning and support on both technical and non-technical aspects.
  * [Hoang Nam](https://www.facebook.com/namnew2003/): Data Science & Business Analytics at DUE
  * [Lê Ngọc Bảo]: Data Science & Business Analytics at DUE
* **Other members:** Conduct data discovery and documentation, uncover business insights and provide client-driven recommendations.
  * [Bich Hoa](https://www.facebook.com/bich.hoa.050303): Data Science & Business Analytics at DUE
  * [My Linh](https://www.facebook.com/mylinhh1853): Data Science & Business Analytics at DUE
  * [Nguyễn Sỹ Tiến Đạt]: Data Science & Business Analytics at DUE
## About the data
### Data Source
#### (Data is taken from Kaggle and API from Ebay e-commerce platform)
* **Product Data:**
  * `Product_id`: Identifier of each product.
  * `Brand`: The brand of the perfume.
  * `Title`: The title of the listing.
  * `Type`:  The type of perfume (e.g., Eau de Parfum, Eau de Toilette).
  * `Price`: The price of the perfume.
  * `PriceWithCurrency`: The price with currency notation.
  * `Available`: The number of items available.
  * `AvailableText`: Text description of availability.
  * `Sold`: The number of items sold.
  * `LastUpdated`: The last updated timestamp of the listing.
  * `ItemLocation`: The location of the item.
#### (Data is extracted from API and created in `ETL_data.ipynb` file)
* **Weather_location Data:**
  * `time`: Time of weather data recording (by day, month, or year). Used to identify a specific time for weather data.
  * `tavg`: Average temperature (°C), showing the average temperature during the recorded time period.
  * `tmin`: Minimum temperature (°C), recording the minimum temperature during the day or observation period.
  * `tmax`: Maximum temperature (°C), recording the maximum temperature during the day or observation period.
  * `prcp`: Precipitation (mm), measuring the amount of rain recorded during the time period.
  * `snow`: Snowfall (mm), measuring the amount of snowfall during the time period (if any).
  * `wdir`: Wind direction (degrees), showing the wind direction in degrees from 0° (North) to 360° (South).
  * `wspd`: Average wind speed (m/s), measuring the average wind speed during the time period.
  * `wpgt`: Maximum wind speed (m/s), records the strongest wind speed during the observation period.
  * `pres`: Average air pressure (hPa), measures the atmospheric pressure at the recorded time.
  * `tsun`: Sunshine duration (minutes), total time the sun appears during the day.
* **Coordinates_location Data:**
  * `city`: City name. This is information used to identify a specific location in the data.
  * `lat`: The latitude of the city, showing the geographic location in the North-South direction on Earth.
  * `lon`: The longitude of the city, showing the geographic location in the East-West direction on Earth.
#### (The data is generated from Python libraries and is created in the `ETL_data.ipynb` file.)
* **Customer Data:**
  * `Customer_id`: A unique identifier for each customer. Used to distinguish customers in the database.
  * `Name`: The customer's full name.
  * `Address`: The customer's address, which helps identify the customer's place of residence or geographic location.
  * `Job`: The customer's occupation, which provides information about the field of work or professional role.
  * `Sex`: The customer's gender (e.g., Male, Female).
  * `Age`: The customer's age, often used for demographic analysis.
  * `Phone`: The customer's contact phone number, used for communication or support purposes.
  * `Email`: The customer's email address, often used for notifications, communications, or email marketing.
* **Order Data:**
  * `Order_time`: Order time, showing the date and time the order was created. This information is important for tracking and analyzing order trends over time.
  * `Order_id`: A unique identifier for each order. Used to distinguish and retrieve detailed information about each order.
  * `Customer_id`: The identifier of the customer associated with the order. This is a foreign key, connecting data to the customer table.
  * `Total`: The total value of the order, calculated based on the price and quantity of each product in the order. 
* **Order_details Data:**
  * `Orderdetail_id`: Unique identifier for each detail item in the order. Used to distinguish items in the order details table.
  * `Order_id`: The identifier of the order linked to the order details. This is a foreign key, connecting data to the order table.
  * `Sanpham_id`: The identifier of the product, linked to the product table. Used to identify the type of product in the order details.
  * `Quanlity`: The quantity of the product in the order.
  * `Price`: The price of the product (per unit), recorded to calculate the total order value.
### Cleaned Data
  * `order_time`: Order time, showing the date and time the order was created. This information is important for tracking and analyzing order trends over time.
  * `orderdetail_id`: Unique identifier for each detail item in the order. Used to distinguish items in the order details table.
  * `order_id`: A unique identifier for each order. Used to distinguish and retrieve detailed information about each order.
  * `customer_id`: A unique identifier for each customer. Used to distinguish customers in the database.
  * `product_id`: Identifier of each product.
  * `brand`: The brand of the perfume.
  * `type`:  The type of perfume (e.g., Eau de Parfum, Eau de Toilette).
  * `price`: The price of the perfume.
  * `quanlity`: The quantity of the product in the order.
  * `itemLocation`: The location of the item.
  * `weather`: Weather that the product is suitable for.
  * `address`: The customer's address, which helps identify the customer's place of residence or geographic location.
  * `sex`: The customer's gender (e.g., Male, Female).
  * `age`: The customer's age, often used for demographic analysis.
  * `lat`: The latitude of the location, which supports spatial analysis or visualization on a map.
  * `lon`: The longitude of the location, combined with lat to determine the exact geographic location.
  * `Doanh thu`: The total revenue of the order, calculated as `price` × `quantity` for each product in the order.
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
