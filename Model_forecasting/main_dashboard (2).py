import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import streamlit as st
from datetime import datetime
import plotly.graph_objects as go
import os
# Set the page layout to 'wide'
st.set_page_config(layout="wide", page_title="Sales Dashboard")

# Add custom CSS to handle the layout and scrollbar
st.markdown(
    """
    <style>
    /* Đặt chiều rộng của trang */
    .main {
        max-width: 1750px;
        padding-left: 20px;
        padding-right: 20px;
    }

    /* Di chuyển thanh cuộn */
    section.main > div {
        padding-right: 0px;
    }

    /* Tăng cột cho các số liệu */
    div[data-testid="metric-container"] {
        width: 200px;
        margin-right: 20px;
    }

    /* Tăng kích thước tiêu đề */
    .main-title {
        font-size: 3.5em !important; /* Tăng kích thước lớn hơn */
        font-weight: bold;
        color: #FF6B6B; /* Thay đổi màu tiêu đề */
        text-align: center; /* Căn giữa */
        margin-bottom: 30px;
        text-transform: uppercase;
    }

    /* Tăng font tiêu đề phụ */
    .sub-title {
        font-size: 1.5em;
        color: #3498DB;
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True,
)





# Load the datasets
chunk_size = 500000  # Chia nhỏ dữ liệu thành các phần nhỏ
fact_sales_chunks = pd.read_csv(r"C:\Users\ADMIN\.ssh\dvdrental\factSales.csv", chunksize=chunk_size)
dim_staff = pd.read_csv(r"C:\Users\ADMIN\.ssh\dvdrental\dimStaff.csv")
dim_film = pd.read_csv(r"C:\Users\ADMIN\.ssh\dvdrental\dimFilm.csv")
dim_date = pd.read_csv(r"C:\Users\ADMIN\.ssh\dvdrental\dimDate.csv")
dim_customer = pd.read_csv(r"C:\Users\ADMIN\.ssh\dvdrental\dimCustomer.csv")

st.markdown("<br><hr><br>", unsafe_allow_html=True)


# Tải dữ liệu từ CSV (hoặc từ bộ dữ liệu khác)
fact_sales = pd.read_csv(r"C:\Users\ADMIN\.ssh\dvdrental\factSales.csv")
dim_date = pd.read_csv(r"C:\Users\ADMIN\.ssh\dvdrental\dimDate.csv")
# Kiểm tra trùng lặp trong bảng dim_film
duplicate_films = dim_film[dim_film.duplicated(subset='film_id', keep=False)]
duplicate_customers = dim_customer[dim_customer.duplicated(subset='customer_id', keep=False)]
duplicate_dates = dim_date[dim_date.duplicated(subset='date_id', keep=False)]


# Drop duplicates in the dimension tables
dim_film = dim_film.drop_duplicates(subset='film_id')
dim_customer = dim_customer.drop_duplicates(subset='customer_id')
dim_date = dim_date.drop_duplicates(subset='date_id')
# Kết hợp dữ liệu sales với ngày tháng
sales_data = pd.merge(fact_sales, dim_date, on='date_id')

# Tính toán các chỉ số cần thiết
total_sales_all_time = sales_data['sales_amount'].sum()
total_transactions = len(sales_data)
st.title('Sales Data Analysis Dashboard with Filters')

# Filter Sidebar
st.sidebar.header("Filter Options")

# Country Filter (Dropdown with 'All' option)
country_options = ['All'] + list(dim_customer['country'].unique())
country_filter = st.sidebar.selectbox("Select Country", options=country_options, index=0)

# Film Category Filter (Multi-Select with 'All' option)
film_categories = ['All'] + list(dim_film['category'].unique())
category_filter = st.sidebar.multiselect("Select Film Category", options=film_categories, default=['All'])

# Year Filter (Multi-Select with 'All' option)
years_available = ['All'] + sorted(dim_date['year'].unique())
year_filter = st.sidebar.multiselect("Select Year(s)", options=years_available, default=['All'])

# Month Filter (Multi-Select with 'All' option)
month_filter = st.sidebar.multiselect(
    "Select Month(s)", options=['All'] + list(range(1, 13)), default=['All'])

# Xử lý tùy chọn "All" cho các bộ lọc
if 'All' in category_filter:
    filtered_film = dim_film  # Không lọc theo thể loại
else:
    filtered_film = dim_film[dim_film['category'].isin(category_filter)]

if 'All' in year_filter:
    filtered_sales_date = dim_date  # Không lọc theo năm
else:
    filtered_sales_date = dim_date[dim_date['year'].isin(year_filter)]

if 'All' in month_filter:
    filtered_sales_date = filtered_sales_date  # Không lọc theo tháng
else:
    filtered_sales_date = filtered_sales_date[filtered_sales_date['month'].isin(month_filter)]

# Function to process chunks of data and merge them incrementally
def process_chunk(chunk):
    # Nếu không chọn "All", chỉ lọc khách hàng theo quốc gia đã chọn
    if country_filter != 'All':
        chunk = pd.merge(chunk, dim_customer[dim_customer['country'] == country_filter], on='customer_id')
    else:
        chunk = pd.merge(chunk, dim_customer, on='customer_id')  # Nếu chọn "All", giữ lại toàn bộ khách hàng
    
    # Áp dụng bộ lọc cho phim
    chunk = pd.merge(chunk, filtered_film, on='film_id')
    
    # Áp dụng bộ lọc cho ngày
    chunk = pd.merge(chunk, filtered_sales_date, on='date_id')
    
    return chunk

# Khởi tạo DataFrame rỗng để lưu kết quả
filtered_sales = pd.DataFrame()

# Xử lý từng chunk của fact_sales
for chunk in fact_sales_chunks:
    processed_chunk = process_chunk(chunk)
    filtered_sales = pd.concat([filtered_sales, processed_chunk], ignore_index=True)

# Loại bỏ dữ liệu trùng lặp (nếu có)
filtered_sales = filtered_sales.drop_duplicates()



# Lọc dữ liệu cho tháng hiện tại
current_month = datetime.now().month
current_year = datetime.now().year
current_month_sales = sales_data[(sales_data['month'] == current_month) & (sales_data['year'] == current_year)]['sales_amount'].sum()
current_month_transactions = len(sales_data[(sales_data['month'] == current_month) & (sales_data['year'] == current_year)])

# Tính phần trăm thay đổi từ tháng trước
previous_month_sales = sales_data[(sales_data['month'] == current_month - 1) & (sales_data['year'] == current_year)]['sales_amount'].sum()
previous_month_transactions = len(sales_data[(sales_data['month'] == current_month - 1) & (sales_data['year'] == current_year)])

sales_percentage_change = ((current_month_sales - previous_month_sales) / previous_month_sales) * 100 if previous_month_sales > 0 else 0
transaction_percentage_change = ((current_month_transactions - previous_month_transactions) / previous_month_transactions) * 100 if previous_month_transactions > 0 else 0

# Hiển thị thông tin trên trang
st.title("Flight Reviews (KPI Display)")

# All Time Metrics
st.subheader("All Time Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Sales", value=f"${total_sales_all_time:,.2f}")
with col2:
    st.metric(label="Total Transactions", value=f"{total_transactions:,}")
with col3:
    st.metric(label="Average Sale per Transaction", value=f"${total_sales_all_time / total_transactions:,.2f}")
with col4:
    st.metric(label="Total Number of Reviews", value=f"{total_transactions:,}")

# This Month Metrics
st.subheader(f"This Month Metrics ({datetime.now().strftime('%B - %Y')})")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Sales This Month", value=f"${current_month_sales:,.2f}", delta=f"{sales_percentage_change:.2f}% from last month", delta_color="inverse")
with col2:
    st.metric(label="Transactions This Month", value=f"{current_month_transactions:,}", delta=f"{transaction_percentage_change:.2f}% from last month", delta_color="inverse")
with col3:
    if current_month_transactions > 0:
        st.metric(label="Avg Sale per Transaction", value=f"${current_month_sales / current_month_transactions:,.2f}")
    else:
        st.metric(label="Avg Sale per Transaction", value=f"N/A")
with col4:
    st.metric(label="Number of Reviews", value=f"{current_month_transactions:,}", delta=f"{current_month_transactions - previous_month_transactions} reviews from last month", delta_color="inverse")


## Loại bỏ các dòng trùng lặp trước khi tính toán
filtered_sales = filtered_sales.drop_duplicates()

# Hàm lấy tháng và năm cuối cùng hoặc theo bộ lọc
def get_selected_or_latest_year_month(filtered_sales, year_filter, month_filter):
    # Nếu không có bộ lọc nào được chọn, lấy năm và tháng mới nhất
    if 'All' in year_filter or len(year_filter) == 0:
        latest_year = filtered_sales['year'].max()
    else:
        latest_year = max(year_filter)  # Lấy năm được chọn từ bộ lọc
    
    if 'All' in month_filter or len(month_filter) == 0:
        latest_month = filtered_sales[filtered_sales['year'] == latest_year]['month'].max()
    else:
        latest_month = max(month_filter)  # Lấy tháng được chọn từ bộ lọc
        
    return latest_year, latest_month

# Lấy năm và tháng cuối cùng hoặc dựa trên bộ lọc
last_year, last_month = get_selected_or_latest_year_month(filtered_sales, year_filter, month_filter)

# Xác định tháng và năm trước đó
if last_month == 1:
    last_previous_month = 12
    last_previous_year = last_year - 1
else:
    last_previous_month = last_month - 1
    last_previous_year = last_year

# Lọc dữ liệu cho tháng hiện tại và tháng trước đó
valid_last_month = filtered_sales[(filtered_sales['month'] == last_month) & (filtered_sales['year'] == last_year)].drop_duplicates()
valid_last_previous_month = filtered_sales[(filtered_sales['month'] == last_previous_month) & (filtered_sales['year'] == last_previous_year)].drop_duplicates()



# Tính toán doanh thu và số lượng giao dịch
last_month_sales = valid_last_month['sales_amount'].sum()
last_month_transactions = len(valid_last_month)

last_previous_month_sales = valid_last_previous_month['sales_amount'].sum()
last_previous_month_transactions = len(valid_last_previous_month)

# Tính toán phần trăm thay đổi doanh thu và giao dịch
last_sales_percentage_change = ((last_month_sales - last_previous_month_sales) / last_previous_month_sales) * 100 if last_previous_month_sales > 0 else 0
last_transaction_percentage_change = ((last_month_transactions - last_previous_month_transactions) / last_previous_month_transactions) * 100 if last_previous_month_transactions > 0 else 0

# Hiển thị chỉ số của tháng cuối cùng
st.subheader(f"Last Time Metrics ({last_month} - {last_year})")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Sales Last Month", value=f"${last_month_sales:,.2f}", delta=f"{last_sales_percentage_change:.2f}% from the previous month", delta_color="inverse")
with col2:
    st.metric(label="Transactions Last Month", value=f"{last_month_transactions:,}", delta=f"{last_transaction_percentage_change:.2f}% from the previous month", delta_color="inverse")
with col3:
    if last_month_transactions > 0:
        st.metric(label="Avg Sale per Transaction", value=f"${last_month_sales / last_month_transactions:,.2f}")
    else:
        st.metric(label="Avg Sale per Transaction", value=f"N/A")
with col4:
    st.metric(label="Number of Reviews", value=f"{last_month_transactions:,}", delta=f"{last_month_transactions - last_previous_month_transactions} reviews from the previous month", delta_color="inverse")


df_reviews = pd.DataFrame(filtered_sales)
show_all_reviews = st.checkbox("Show all reviews", value=False)

# Filtered data based on checkbox state
if show_all_reviews:
    display_reviews = df_reviews
else:
    display_reviews = df_reviews.head(5)

# Display the reviews table with a dynamic header
st.subheader("Top 5 Most Recent Reviews" if not show_all_reviews else "All Reviews")
st.dataframe(display_reviews)


# Function to apply pastel colors to bar charts
# Function to apply pastel colors to bar charts with adjustable size
def pastel_bar_chart(x, y, title, xlabel, ylabel, width=10, height=6):
    fig, ax = plt.subplots(figsize=(width, height))  # Adjusting size here
    pastel_colors = plt.get_cmap("Pastel1").colors
    ax.bar(x, y, color=pastel_colors[:len(x)])
    ax.set_title(title, fontsize=16)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

import base64

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Convert your image to Base64
img_base64 = get_image_base64("C:/Users/ADMIN/Pictures/Screenshots/Screenshot 2024-10-31 145540.png")
st.markdown(
    f"""
    <h1 style='display: flex; align-items: center;'>
        <img src="data:image/png;base64,{img_base64}" width="60" style="margin-right: 10px;"/>
        Chart Breakdown
    </h1>
    """,
    unsafe_allow_html=True
)

st.header('Total Sales Over Time')
sales_over_time = filtered_sales.groupby(['year', 'month'])['sales_amount'].sum().reset_index()
sales_over_time = sales_over_time.sort_values(by=['year', 'month'])

# Adjust the size of the plot to fit a wider layout
fig, ax = plt.subplots(figsize=(14, 5))  # Increase width to make it fit layout better

# Plotting the data with a line and markers
ax.plot(sales_over_time['year'].astype(str) + '-' + sales_over_time['month'].astype(str),
        sales_over_time['sales_amount'], color=plt.get_cmap("Pastel1").colors[0], marker='o')

# Set the title and labels with adjusted font size
ax.set_title("Total Sales Over Time", fontsize=16)
ax.set_xlabel("Year-Month", fontsize=12)
ax.set_ylabel("Total Sales ($)", fontsize=12)

# Rotate x-axis labels
plt.xticks(rotation=45, ha='right')

# Remove all spines/borders around the plot
for spine in ax.spines.values():
    spine.set_visible(False)

# Add only horizontal grid lines with a light color and thin line
ax.yaxis.grid(True, color='lightgray', linestyle='-', linewidth=0.5)
ax.xaxis.grid(False)  # Disable vertical grid lines

# Display the plot
st.pyplot(fig)



# Top Performing Staff by Sales
st.header('Top Performing Staff by Sales')

# Data for bar chart
top_staff_sales = pd.merge(filtered_sales, dim_staff, on='staff_id').groupby('first_name_y')['sales_amount'].sum().reset_index().sort_values(by='sales_amount', ascending=False).head(10)

# Define a color palette that matches the exact order of staff names
staff_colors = ['#FF6B6B', '#66B3FF', '#FFCC99', '#99FF99', '#3FB8AF'][:len(top_staff_sales)]

# Bar chart
col1, col2 = st.columns(2)
with col1:
    fig_bar = plt.figure(figsize=(8, 6))
    ax = fig_bar.add_subplot(111)
    
    # Remove borders by hiding all spines
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Set only horizontal grid lines with lighter styling
    ax.yaxis.grid(True, color='lightgray', linestyle='-', linewidth=0.5)
    ax.xaxis.grid(False)  # Disable vertical grid lines

    # Plot the bar chart
    ax.bar(top_staff_sales['first_name_y'], top_staff_sales['sales_amount'], color=staff_colors)
    ax.set_title("Top Performing Staff by Sales")
    ax.set_xlabel("Staff Name")
    ax.set_ylabel("Total Sales ($)")
    plt.xticks(rotation=45)
    st.pyplot(fig_bar)

# Pie chart with matching colors
with col2:
    fig_pie = go.Figure(go.Pie(
        labels=top_staff_sales['first_name_y'],
        values=top_staff_sales['sales_amount'],
        hole=0.4,  # Donut effect
        textinfo='percent+label',  # Show percentage with labels
        marker=dict(colors=staff_colors),  # Apply the same color list
        pull=[0.05] * len(top_staff_sales['sales_amount']) 
    ))
    fig_pie.update_layout(title_text="Sales Distribution by Staff")
    st.plotly_chart(fig_pie)


# Top Film Categories by Sales
st.header('Top Film Categories by Sales')

# Data for bar chart
top_category_sales = filtered_sales.groupby('category')['sales_amount'].sum().reset_index().sort_values(by='sales_amount', ascending=False).head(10)

# Define a color palette that matches the exact order of film categories
category_colors = ['#FF6B6B', '#66B3FF', '#FFCC99', '#99FF99', '#3FB8AF', '#C1C1C1', '#B4A2FF', '#FF9999', '#B6E0FF', '#FFC8A2'][:len(top_category_sales)]

# Bar chart with modified layout
col1, col2 = st.columns(2)
with col1:
    fig_bar, ax = plt.subplots(figsize=(8, 6))
    ax.bar(top_category_sales['category'], top_category_sales['sales_amount'], color=category_colors)
    ax.set_title("Top Film Categories by Sales", fontsize=16)
    ax.set_xlabel("Film Category", fontsize=12)
    ax.set_ylabel("Total Sales ($)", fontsize=12)
    plt.xticks(rotation=45)
    
    # Remove all spines/borders around the plot
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Add only horizontal grid lines
    ax.yaxis.grid(True, color='lightgray', linestyle='-', linewidth=0.5)
    ax.xaxis.grid(False)  # Disable vertical grid lines

    # Display the plot
    st.pyplot(fig_bar)

# Pie chart with matching colors
with col2:
    fig_pie = go.Figure(go.Pie(
        labels=top_category_sales['category'],
        values=top_category_sales['sales_amount'],
        hole=0.4,  # Donut effect
        textinfo='percent+label',  # Show percentage with labels
        marker=dict(colors=category_colors),  # Apply the same color list
        pull=[0.05] * len(top_category_sales['sales_amount'])  # Slightly separate each segment
    ))
    fig_pie.update_layout(title_text="Sales Distribution by Category")
    st.plotly_chart(fig_pie)



st.header('Top Countries by Sales')

import plotly.express as px

# Group sales by country
sales_by_country = filtered_sales.groupby('country')['sales_amount'].sum().reset_index()

# Define custom color scale using staff_colors
custom_color_scale = [[0.0, '#FF6B6B'],   # Red
                      [0.25, '#66B3FF'],  # Light Blue
                      [0.5, '#FFCC99'],   # Light Orange
                      [0.75, '#99FF99'],  # Light Green
                      [1.0, '#3FB8AF']]   # Teal

# Create a map with Plotly
fig = px.choropleth(sales_by_country,
                    locations="country",
                    locationmode="country names",
                    color="sales_amount",
                    hover_name="country",
                    color_continuous_scale=custom_color_scale,  # Apply the custom color scale
                    labels={'sales_amount':'Total Sales ($)'})

# Set default background color for countries not in the data
fig.update_geos(
    showcountries=True,
    countrycolor="darkgrey",  # Color for country boundaries
    landcolor="white",        # Set countries with no data to white
    showcoastlines=True,
    coastlinecolor="Black",
    lakecolor="lightblue"
)

# Update layout for better appearance
fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type="equirectangular",
    ),
    width=1500,  # Width of the plot
    height=850   # Height of the plot
)

# Display the map
st.plotly_chart(fig)




film_sales_data = pd.merge(filtered_sales, dim_film, on='film_id')

st.header('Film Length vs Sales (Binned)')
bin_labels = ['0-30', '31-60', '61-90', '91-120', '121-150', '151-180']
film_sales_data['length_bin'] = pd.cut(film_sales_data['length_x'], bins=[0, 30, 60, 90, 120, 150, 180], labels=bin_labels)

# Drop NaN values that may have resulted from binning out-of-range values
film_length_sales_bins = film_sales_data[['length_bin', 'sales_amount']].dropna()

# Ensure that the 'length_bin' column is a string type to avoid KeyError in color mapping
film_length_sales_bins['length_bin'] = film_length_sales_bins['length_bin'].astype(str)

# Define custom colors for each bin
color_map = {
    '0-30': 'blue',
    '31-60': 'lightblue',
    '61-90': 'green',
    '91-120': 'yellow',
    '121-150': 'orange',
    '151-180': 'red'
}

# Create a box plot with slim boxes
fig = px.box(
    film_length_sales_bins,
    x="length_bin",
    y="sales_amount",
    color="length_bin",
    color_discrete_map=color_map,
    title="Film Length vs Sales (Binned)"
)

# Update layout for a white background, slim box width, and adjust figure size
fig.update_traces(width=0.1)  # Slim down the box width
fig.update_layout(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(color="black"),
    title_font_size=24,
    xaxis=dict(title="Film Length (minutes)", color="black"),
    yaxis=dict(title="Total Sales ($)", color="black"),
    legend=dict(title="Film Length Bins", x=1.05, y=1),
    width=1400,  # Increase the width for a more horizontal layout
    height=500   # Adjust the height if needed
)

# Show the plot in Streamlit
st.plotly_chart(fig)






# Sales Trends by Staff Location
st.header('Sales Trends by Staff Location')

# Data for bar chart
top_sales_by_city = pd.merge(filtered_sales, dim_staff, on='staff_id').groupby('store_city')['sales_amount'].sum().reset_index().sort_values(by='sales_amount', ascending=False).head(10)

# Define a color palette that matches the exact order of cities
city_colors = ['#FF6B6B', '#66B3FF', '#FFCC99', '#99FF99', '#3FB8AF', '#C1C1C1', '#B4A2FF', '#FF9999', '#B6E0FF', '#FFC8A2'][:len(top_sales_by_city)]

# Bar chart with modified layout
col1, col2 = st.columns(2)
with col1:
    fig_bar, ax = plt.subplots(figsize=(8, 6))
    ax.bar(top_sales_by_city['store_city'], top_sales_by_city['sales_amount'], color=city_colors)
    ax.set_title("Sales Trends by Staff Location", fontsize=16)
    ax.set_xlabel("City", fontsize=12)
    ax.set_ylabel("Total Sales ($)", fontsize=12)
    plt.xticks(rotation=45)
    
    # Remove all spines/borders around the plot
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Add only horizontal grid lines
    ax.yaxis.grid(True, color='lightgray', linestyle='-', linewidth=0.5)
    ax.xaxis.grid(False)  # Disable vertical grid lines

    # Display the plot
    st.pyplot(fig_bar)

# Pie chart with matching colors
with col2:
    fig_pie = go.Figure(go.Pie(
        labels=top_sales_by_city['store_city'],
        values=top_sales_by_city['sales_amount'],
        hole=0.4,  # Donut effect
        textinfo='percent+label',  # Show percentage with labels
        marker=dict(colors=city_colors),  # Apply the same color list
        pull=[0.05] * len(top_sales_by_city['sales_amount'])  # Slightly separate each segment
    ))
    fig_pie.update_layout(title_text="Sales Distribution by Location")
    st.plotly_chart(fig_pie)


# Sales Performance by Rental Duration
st.header('Sales Performance by Rental Duration')

# Data for bar chart
rental_duration_sales = film_sales_data.groupby('rental_duration_x')['sales_amount'].sum().reset_index()

# Define a color palette that matches the exact order of rental durations
duration_colors = ['#FF6B6B', '#66B3FF', '#FFCC99', '#99FF99', '#3FB8AF', '#C1C1C1'][:len(rental_duration_sales)]

# Bar chart
col1, col2 = st.columns(2)
with col1:
    fig_bar, ax = plt.subplots(figsize=(8, 6))
    ax.bar(rental_duration_sales['rental_duration_x'], rental_duration_sales['sales_amount'], color=duration_colors)
    ax.set_title("Sales Performance by Rental Duration", fontsize=16)
    ax.set_xlabel("Rental Duration (days)", fontsize=12)
    ax.set_ylabel("Total Sales ($)", fontsize=12)
    plt.xticks(rotation=45)

    # Remove all spines (borders) around the plot
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Add only horizontal grid lines
    ax.yaxis.grid(True, color='lightgray', linestyle='-', linewidth=0.5)
    ax.xaxis.grid(False)  # Disable vertical grid lines

    # Display the plot
    st.pyplot(fig_bar)

# Pie chart with matching colors
with col2:
    fig_pie = go.Figure(go.Pie(
        labels=rental_duration_sales['rental_duration_x'],
        values=rental_duration_sales['sales_amount'],
        hole=0.4,  # Donut effect
        textinfo='percent+label',  # Show percentage with labels
        marker=dict(colors=duration_colors),  # Apply the same color list
        pull=[0.05] * len(rental_duration_sales['sales_amount'])  # Slightly separate each segment
    ))
    fig_pie.update_layout(title_text="Sales Distribution by Rental Duration")
    st.plotly_chart(fig_pie)

# Weekend vs Weekday Sales
sales_with_weekend = pd.merge(filtered_sales, dim_date[['date_id', 'is_weekend']], on='date_id', how='left')
st.header('Weekend vs Weekday Sales')
# Select the correct 'is_weekend' column if duplicated
if 'is_weekend_x' in sales_with_weekend.columns:
    sales_with_weekend['is_weekend'] = sales_with_weekend['is_weekend_x']
elif 'is_weekend_y' in sales_with_weekend.columns:
    sales_with_weekend['is_weekend'] = sales_with_weekend['is_weekend_y']

# Drop unnecessary duplicate columns
sales_with_weekend.drop(columns=['is_weekend_x', 'is_weekend_y'], inplace=True, errors='ignore')

# Group data by 'is_weekend' and calculate total sales
if 'is_weekend' in sales_with_weekend.columns:
    sales_weekend = sales_with_weekend.groupby('is_weekend')['sales_amount'].sum().reset_index()

    # Add Day Type label for display
    sales_weekend['Day Type'] = sales_weekend['is_weekend'].map({True: 'Weekend', False: 'Weekday'})
    day_type_colors = ['#FF6B6B', '#66B3FF']

    col1, col2 = st.columns(2)
    with col1:
        fig_bar, ax = plt.subplots(figsize=(8, 6))
        ax.bar(sales_weekend['Day Type'], sales_weekend['sales_amount'], color=day_type_colors)
        ax.set_title("Weekend vs Weekday Sales", fontsize=16)
        ax.set_xlabel("Day Type", fontsize=12)
        ax.set_ylabel("Total Sales ($)", fontsize=12)

        # Remove all spines (borders) around the plot
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Add only horizontal grid lines
        ax.yaxis.grid(True, color='lightgray', linestyle='-', linewidth=0.5)
        ax.xaxis.grid(False)  # Disable vertical grid lines

        # Display the plot
        st.pyplot(fig_bar)

    with col2:
        fig_pie = go.Figure(go.Pie(
            labels=sales_weekend['Day Type'],
            values=sales_weekend['sales_amount'],
            hole=0.4,  # Donut effect
            textinfo='percent+label',  # Show percentage with labels
            marker=dict(colors=day_type_colors),  # Apply the same color list
            pull=[0.05] * len(sales_weekend['sales_amount'])  # Slightly separate each segment
        ))
        fig_pie.update_layout(title_text="Sales Distribution by Day Type")
        st.plotly_chart(fig_pie)
else:
    st.write("Column 'is_weekend' not found in merged data.")


# Kết hợp dữ liệu bán hàng với thông tin phim để lấy 'sales_amount' và thông tin diễn viên
film_sales_data = pd.merge(filtered_sales, dim_film, on='film_id')

import plotly.graph_objects as go
import plotly.express as px

# Group sales by category
import plotly.graph_objects as go

# Group data by category and calculate cumulative percentage
category_sales = filtered_sales.groupby('category')['sales_amount'].sum().reset_index().sort_values(by='sales_amount', ascending=False)
category_sales['cumulative_percent'] = category_sales['sales_amount'].cumsum() / category_sales['sales_amount'].sum() * 100

# Define pastel colors for the top 5 bars and gray for others
pastel_colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#FFB266']
default_color = '#999999'
colors = pastel_colors[:5] + [default_color] * (len(category_sales) - 5)

# Create the figure
fig = go.Figure()

# Bar chart for total sales with custom colors
fig.add_trace(go.Bar(
    x=category_sales['category'],
    y=category_sales['sales_amount'],
    name='Total Sales',
    marker_color=colors,
    marker_line_width=0,  # Set line width to 0 for no border around bars
    opacity=0.8
))

# Line chart for cumulative percentage with markers and labels
fig.add_trace(go.Scatter(
    x=category_sales['category'],
    y=category_sales['cumulative_percent'],
    name='Cumulative Percentage',
    yaxis='y2',
    mode='lines+markers+text',
    line=dict(color='rgba(255, 160, 122, 1)', width=3),
    marker=dict(size=8, color='rgba(255, 160, 122, 0.7)', symbol='circle'),
    text=[f'{p:.1f}%' for p in category_sales['cumulative_percent']],
    textposition='top center'
))

# Update layout to focus on horizontal grid lines only and remove vertical grid lines
fig.update_layout(
    title=dict(
        text='Sales Amount and Cumulative Percentage by Category',
        font=dict(size=24),
        x=0.5,
        xanchor='center',
        y=0.97
    ),
    xaxis=dict(
        title='Category',
        titlefont=dict(size=16),
        tickfont=dict(size=14)
    ),
    yaxis=dict(
        title='Total Sales ($)',
        titlefont=dict(size=16),
        tickfont=dict(size=14)
    ),
    yaxis2=dict(
        title='Cumulative Percentage (%)',
        titlefont=dict(size=16),
        tickfont=dict(size=14),
        overlaying='y',
        side='right',
        tickmode='array',
        tickvals=[0, 20, 40, 60, 80, 100],
        ticktext=['0%', '20%', '40%', '60%', '80%', '100%']
    ),
    legend=dict(
        title="Category",
        x=1.05,  # Move the legend further to the right
        y=1,
        font=dict(size=14)
        
    ),
    bargap=0.2,
    width=1450,  # Slightly wider width to add more space
    height=700,
    margin=dict(l=50, r=200, t=100, b=100),  # Increase right margin
    plot_bgcolor='white',
    paper_bgcolor='white',
)
# Show plot
st.plotly_chart(fig)

st.header('Top Performing Actors by Sales')
# Nhóm dữ liệu theo tên diễn viên và tính tổng doanh thu
if 'sales_amount' in film_sales_data.columns and 'actor_first_name_x' in film_sales_data.columns and 'actor_last_name_x' in film_sales_data.columns:
    top_actors_sales = film_sales_data.groupby(['actor_first_name_x', 'actor_last_name_x'])['sales_amount'].sum().reset_index()

    # Create full actor name column
    top_actors_sales['actor_name'] = top_actors_sales['actor_first_name_x'] + ' ' + top_actors_sales['actor_last_name_x']
    
    # Sort by sales and select top 5 actors
    top_actors_sales = top_actors_sales.sort_values(by='sales_amount', ascending=False).head(5)
    actor_colors = ['#FF6B6B', '#66B3FF', '#99FF99', '#C1C1C1', '#FFCC99'][:len(top_actors_sales)]
    
    col1, col2 = st.columns(2)
    
    # Bar chart without borders and with only horizontal grid lines
    with col1:
        fig_bar, ax = plt.subplots(figsize=(8, 6))
        ax.bar(top_actors_sales['actor_name'], top_actors_sales['sales_amount'], color=actor_colors)
        ax.set_title("Top Performing Actors by Sales")
        ax.set_xlabel("Actor Name")
        ax.set_ylabel("Total Sales ($)")
        ax.grid(axis='y', color='lightgray', linestyle='--', linewidth=0.5)  # Horizontal grid only
        ax.spines['top'].set_visible(False)    # Remove top border
        ax.spines['right'].set_visible(False)  # Remove right border
        ax.spines['left'].set_visible(False)   # Remove left border
        ax.spines['bottom'].set_visible(False) # Remove bottom border
        plt.xticks(rotation=45)
        st.pyplot(fig_bar)
    
    # Pie chart with matching colors
    with col2:
        fig_pie = go.Figure(go.Pie(
            labels=top_actors_sales['actor_name'],
            values=top_actors_sales['sales_amount'],
            hole=0.4,  # Donut effect
            textinfo='percent+label',
            marker=dict(colors=actor_colors),
            pull=[0.05] * len(top_actors_sales['sales_amount'])
        ))
        fig_pie.update_layout(title_text="Sales Distribution by Actor")
        st.plotly_chart(fig_pie)

else:
    st.write("Columns 'sales_amount' or actor names not found after merging.")


st.markdown(
    """
    <style>
    .main-title {
        font-size: 3em;
        font-weight: bold;
        color: #2C3E50;
        margin-bottom: 30px;
        text-align: center;
    }

    .sub-title {
        font-size: 1.8em;
        color: #7F8C8D;
        text-align: center;
        margin-bottom: 40px;
    }

    .button-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 20px; /* Khoảng cách giữa các nút */
    }

    .stButton button {
        border: 2px solid transparent;
        border-radius: 10px;
        background-color: #FF6B6B; /* Màu đầu tiên */
        color: white;
        padding: 15px 30px; /* Kích thước nút lớn hơn */
        font-size: 1.2em;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s, transform 0.2s;
    }

    .stButton button:nth-child(2) {
        background-color: #66B3FF; /* Màu thứ hai */
    }

    .stButton button:nth-child(3) {
        background-color: #99FF99; /* Màu thứ ba */
    }

    .stButton button:nth-child(4) {
        background-color: #C1C1C1; /* Màu thứ tư */
    }

    .stButton button:nth-child(5) {
        background-color: #FFCC99; /* Màu thứ năm */
    }

    .stButton button:hover {
        transform: scale(1.1); /* Hiệu ứng phóng to khi hover */
        filter: brightness(1.1);
    }

    .stButton button:focus {
        outline: none;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    }

    .link-container {
        text-align: center;
        margin-top: 30px;
        font-size: 1.5em;
    }

    .link-container a {
        color: #2980B9;
        font-weight: bold;
        text-decoration: none;
    }

    .link-container a:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# Title and subtitle
st.markdown("<div class='main-title'>Main Forecasting </div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Welcome to the forecasting dashboard! Choose an algorithm to explore predictions.</div>", unsafe_allow_html=True)

# Navigation buttons
with st.container():
    st.markdown("<div class='button-container'>", unsafe_allow_html=True)

    if st.button("SARIMA Forecasting"):
        os.system("start cmd /k python -m streamlit run sarima_forecasting.py --server.port 8502")
        st.markdown("<div class='link-container'>[Open SARIMA Forecasting](http://localhost:8502)</div>", unsafe_allow_html=True)

    if st.button("ARIMA Forecasting"):
        os.system("start cmd /k python -m streamlit run arima_forecasting.py --server.port 8503")
        st.markdown("<div class='link-container'>[Open ARIMA Forecasting](http://localhost:8503)</div>", unsafe_allow_html=True)

    if st.button("TBATS Forecasting"):
        os.system("start cmd /k python -m streamlit run tbats_forecasting.py --server.port 8504")
        st.markdown("<div class='link-container'>[Open TBATS Forecasting](http://localhost:8504)</div>", unsafe_allow_html=True)

    if st.button("GARCH Forecasting"):
        os.system("start cmd /k python -m streamlit run garch_forecasting.py --server.port 8505")
        st.markdown("<div class='link-container'>[Open GARCH Forecasting](http://localhost:8505)</div>", unsafe_allow_html=True)

    if st.button("RNN Forecasting"):
        os.system("start cmd /k python -m streamlit run rnn_forecasting.py --server.port 8506")
        st.markdown("<div class='link-container'>[Open RNN Forecasting](http://localhost:8506)</div>", unsafe_allow_html=True)

    if st.button("LSTM Forecasting"):
        os.system("start cmd /k python -m streamlit run lstm_forecasting.py --server.port 8507")
        st.markdown("<div class='link-container'>[Open LSTM Forecasting](http://localhost:8507)</div>", unsafe_allow_html=True)

    if st.button("GRU Forecasting"):
        os.system("start cmd /k python -m streamlit run gru_forecasting.py --server.port 8508")
        st.markdown("<div class='link-container'>[Open GRU Forecasting](http://localhost:8508)</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Footer instructions
st.write("Use the buttons above to navigate to the desired forecasting algorithm page.")



