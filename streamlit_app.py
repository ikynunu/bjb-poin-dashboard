import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.title("BJB Loyalty Points Dashboard")

@st.cache_resource
def load_data():
    data = pd.read_csv("loyalty_points_log_8.csv")
    return data

data = load_data()

# Ensure the 'Klasifikasi' and 'Total' columns are present
if 'Klasifikasi' in data.columns and 'Total' in data.columns:
    # Extract relevant columns for pie chart
    df_classification = data[['Klasifikasi', 'Total']].dropna()

# Create tabs for navigation
tab1, tab2, tab3 = st.tabs(["Daily Monitoring", "Historical Monitoring", "Voucher Recommendations"])

# Tab 1: Daily Monitoring
with tab1:
    st.header("BJB Points Monitoring")
    current_date = data['Date'].iloc[0]
    st.write(f"Date: {current_date}")

    # Accessing the values directly since the data is already filtered for August 8, 2024
    total_points_earned = data['Total Points Earn'].iloc[0]
    total_points_redeemed = data['Total Points Redeemed'].iloc[0]
    total_admin_fees = data['Total Admin'].iloc[0]
    total_vouchers_redeemed = data['Redeemed Vouchers'].iloc[0]
    total_vouchers_not_redeemed = data['Currently Vouchers'].iloc[0]

    # Top row: Total Points Earned and Total Points Redeemed (side by side)
    col1, col2 = st.columns([1, 1])
    col1.metric("**Total Points Earned Today**", "{:,.0f}".format(total_points_earned))
    col2.metric("**Total Points Redeemed Today**", "{:,.0f}".format(total_points_redeemed))

    # Middle row: Total Admin Fees in the center
    col3 = st.columns([1, 2, 1])  # Creates 3 columns, with the middle one being wider
    col3[1].metric("**Total Admin Fees Collected Today**", "Rp {:,.0f}".format(total_admin_fees))  # Access the middle column (index 1)

    # Display voucher images, names, and metrics for redeemed and not yet redeemed vouchers
    st.header("Vouchers Overview")

    # First voucher - displayed in the left column
    col4, col5 = st.columns(2)
    with col4:
        st.image("1.png", use_column_width=True)  # Manually specify the image path for voucher 1
        st.write("**Food & Beverages**")  # Manually specify the name for voucher 1
        st.metric("Redeemed Vouchers", "{:,.0f}".format(total_vouchers_redeemed))  # Metrics for voucher 1
        st.metric("Vouchers Not Yet Redeemed", "{:,.0f}".format(total_vouchers_not_redeemed))

    # Second voucher - displayed in the right column
    with col5:
        st.image("2.png", use_column_width=True)  # Manually specify the image path for voucher 2
        st.write("**Electricity**")  # Manually specify the name for voucher 2
        st.metric("Redeemed Vouchers", "{:,.0f}".format(total_vouchers_redeemed))  # Metrics for voucher 2
        st.metric("Vouchers Not Yet Redeemed", "{:,.0f}".format(total_vouchers_not_redeemed))

    # Third voucher - create a new row with 2 columns
    col6, col7 = st.columns(2)
    with col6:
        st.image("3.png", use_column_width=True)  # Manually specify the image path for voucher 3
        st.write("**Convenience Store**")  # Manually specify the name for voucher 3
        st.metric("Redeemed Vouchers", "{:,.0f}".format(total_vouchers_redeemed))  # Metrics for voucher 3
        st.metric("Vouchers Not Yet Redeemed", "{:,.0f}".format(total_vouchers_not_redeemed))

    # Fourth voucher - in the right column
    with col7:
        st.image("Rp50000.png", use_column_width=True)  # Manually specify the image path for voucher 4
        st.write("**Entertainment**")  # Manually specify the name for voucher 4
        st.metric("Redeemed Vouchers", "{:,.0f}".format(total_vouchers_redeemed))  # Metrics for voucher 4
        st.metric("Vouchers Not Yet Redeemed", "{:,.0f}".format(total_vouchers_not_redeemed))

    # Transaction Frequencies
    st.header("Transaction Activity Today")

    # Display first 5 rows of specific columns
    st.dataframe(data[['Loyalty Point ID', 'CIF', 'Log ID', 'Tanggal Pemberian', 'Sumber Poin', 'Jumlah Poin']].head(5))

    # Insights
    st.header("Daily Insights")
    # Pie chart visualization with Plotly
    fig = px.pie(df_classification, names='Klasifikasi', values='Total', 
                title='Classification of Point Sources',
                labels={'Klasifikasi': 'Point Source', 'Total': 'Total Points'},
                hole=0.3)  # Add hole for donut chart effect (optional)
        
    st.plotly_chart(fig)

    # Insert insights based on the calculated percentages
    insights = f"""
    - **Buy & Pay** contributes the largest share of points earned at 38.19%, indicating that most customers prefer using the platform for purchases and payments.
    - **E-Wallet** transactions follow, contributing 20.14% of the total points earned, showing significant adoption of digital wallet payments.
    - **QRIS** payments make up 19.44%, which reflects the growing use of QR-based transactions in the customer base.
    - **Transfer Non BI-Fast** represent smaller but still notable shares of transactions, showing that both real-time and regular transfers are important but less dominant compared to purchase/payment activities.
    """
    st.write(insights)

# Tab 2: Historical Monitoring
# Tab 2: Historical Monitoring
with tab2:
    st.header("BJB Points Monitoring")

    # Kalender untuk pemilihan tanggal
    selected_date = st.date_input("Select Date", value=pd.to_datetime('2024-08-01'))

    # Fungsi untuk memuat data berdasarkan tanggal yang dipilih
    def load_data_by_date(selected_date):
        # Pemetaan file CSV untuk tanggal 1-7 Agustus 2024
        file_map = {
            "2024-08-01": 'loyalty_points_log_1.csv',
            "2024-08-02": 'loyalty_points_log_2.csv',
            "2024-08-03": 'loyalty_points_log_3.csv',
            "2024-08-04": 'loyalty_points_log_4.csv',
            "2024-08-05": 'loyalty_points_log_5.csv',
            "2024-08-06": 'loyalty_points_log_6.csv',
            "2024-08-07": 'loyalty_points_log_7.csv'
        }
        
        # Formatkan tanggal yang dipilih
        selected_date_str = selected_date.strftime('%Y-%m-%d')
        
        # Cek apakah tanggal yang dipilih ada dalam rentang yang memiliki CSV
        if selected_date_str in file_map:
            # Jika ada, muat file CSV yang sesuai
            file_path = file_map[selected_date_str]
            return pd.read_csv(file_path)
        else:
            # Jika tidak ada data untuk tanggal yang dipilih
            return None

    # Memuat data berdasarkan tanggal yang dipilih
    historical_data = load_data_by_date(selected_date)

    # Pastikan data tersedia sebelum menampilkan
    if historical_data is not None:
        # Tampilkan tanggal yang dipilih
        st.write(f"Selected date: {selected_date.strftime('%B %d, %Y')}")

        # Menghitung metrik yang sama seperti di Tab 1
        total_points_earned = historical_data['Total Points Earn'].iloc[0]
        total_points_redeemed = historical_data['Total Points Redeemed'].iloc[0]
        total_admin_fees = historical_data['Total Admin'].iloc[0]
        total_vouchers_redeemed = historical_data['Redeemed Vouchers'].iloc[0]
        total_vouchers_not_redeemed = historical_data['Currently Vouchers'].iloc[0]

        # Top row: Total Points Earned and Total Points Redeemed (side by side)
        col1, col2 = st.columns([1, 1])
        col1.metric("**Total Points Earned Today**", "{:,.0f}".format(total_points_earned))
        col2.metric("**Total Points Redeemed Today**", "{:,.0f}".format(total_points_redeemed))

        # Middle row: Total Admin Fees in the center
        col3 = st.columns([1, 2, 1])  # Creates 3 columns, with the middle one being wider
        col3[1].metric("**Total Admin Fees Collected Today**", "Rp {:,.0f}".format(total_admin_fees))  # Access the middle column (index 1)

        # Display voucher images, names, and metrics for redeemed and not yet redeemed vouchers
        st.header("Vouchers Overview")

        # First voucher - displayed in the left column
        col4, col5 = st.columns(2)
        with col4:
            st.image("1.png", use_column_width=True)  # Manually specify the image path for voucher 1
            st.write("**Food & Beverages**")  # Manually specify the name for voucher 1
            st.metric("Redeemed Vouchers", "{:,.0f}".format(total_vouchers_redeemed))  # Metrics for voucher 1
            st.metric("Vouchers Not Yet Redeemed", "{:,.0f}".format(total_vouchers_not_redeemed))

        # Second voucher - displayed in the right column
        with col5:
            st.image("2.png", use_column_width=True)  # Manually specify the image path for voucher 2
            st.write("**Electricity**")  # Manually specify the name for voucher 2
            st.metric("Redeemed Vouchers", "{:,.0f}".format(total_vouchers_redeemed))  # Metrics for voucher 2
            st.metric("Vouchers Not Yet Redeemed", "{:,.0f}".format(total_vouchers_not_redeemed))

        # Third voucher - create a new row with 2 columns
        col6, col7 = st.columns(2)
        with col6:
            st.image("3.png", use_column_width=True)  # Manually specify the image path for voucher 3
            st.write("**Convenience Store**")  # Manually specify the name for voucher 3
            st.metric("Redeemed Vouchers", "{:,.0f}".format(total_vouchers_redeemed))  # Metrics for voucher 3
            st.metric("Vouchers Not Yet Redeemed", "{:,.0f}".format(total_vouchers_not_redeemed))

        # Fourth voucher - in the right column
        with col7:
            st.image("Rp50000.png", use_column_width=True)  # Manually specify the image path for voucher 4
            st.write("**Entertainment**")  # Manually specify the name for voucher 4
            st.metric("Redeemed Vouchers", "{:,.0f}".format(total_vouchers_redeemed))  # Metrics for voucher 4
            st.metric("Vouchers Not Yet Redeemed", "{:,.0f}".format(total_vouchers_not_redeemed))

        # Transaction Frequencies
        st.header("Transaction Activity")
        st.dataframe(historical_data[['Loyalty Point ID', 'CIF', 'Log ID', 'Tanggal Pemberian', 'Sumber Poin', 'Jumlah Poin']].head(5))
    else:
        st.warning("No data available for the selected date.")

# Tab 3: Voucher Recommendations
with tab3:
    st.header("Voucher Recommendations for Next Month")
    st.write("Based on the data from the previous month, here are the recommended vouchers for next month:")
