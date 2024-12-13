
# Xậy dựng hệ ETL trên nền tăng AWS Cloud
![0001-introduction](https://github.com/user-attachments/assets/feef186c-aa78-4ddc-9e33-a608fcd0c51b)

This report presents the development of an ETL Pipeline system on the AWS Cloud platform, aiming to automate the processes of data collection, processing, and analysis to support businesses in optimizing their strategic decisions. The system consists of three main stages: extracting data from PostgreSQL and other sources to store in Amazon S3; transforming data using AWS Glue through steps such as cleaning, standardizing, and processing; and finally, loading the processed data into Amazon Redshift for analysis and reporting. Tools such as AWS Glue, Amazon Redshift, Streamlit, and Tableau are utilized to manage data and generate visual reports, enabling businesses to make quick and accurate decisions. The results demonstrate that the ETL system not only fully automates the workflow but also ensures high efficiency in handling large datasets, supports real-time analytics, and meets the scalability demands of enterprises.


# (Phase 1): Extract - Transform - Load (ETL) (Project focus)
**The Analysis And Forecast Of Perfume Demand Project:** requires data on products, customers and purchase information. For the project we aggregate data from different sources from python's faker library, API and kaggle.
![etl-process-extract-transform-load-1](https://github.com/user-attachments/assets/0b96e37a-0af1-40e4-bb29-19c7b0da4754)

# (Phase 2): Overview and Forecasting 
**Visualization and Forecasting for Project:** Here we use a web framework Streamlit to help us present the results of the report and forecast. In Streamlit, users can interact with the chart at will and it can work online near realtime.
![download](https://github.com/user-attachments/assets/a0fd844a-418e-4ea5-ac04-cbfd1bf1ea3c)

# Team members
* **Team Leader/Analytics Engineer/BI Engineer:** Oversee the entire project, planning and support on both technical and non-technical aspects.
  * [Lê Ngọc Bảo]: Data Science & Business Analytics at DUE
* **Other members:** Conduct data discovery and documentation, uncover business insights and provide client-driven recommendations.
  * [Nguyễn Sỹ Tiến Đạt]: Data Science & Business Analytics at DUE

# About the data
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


