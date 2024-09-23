import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.title("bjb Loyalty Points Dashboard")

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
    st.header("bjb Points Monitoring")
    current_date = data['Date'].iloc[0]
    st.write(f"Date: {current_date}")

    # Download buttons at the right
    st.write("")  # Adding an empty line for spacing
    col_download = st.columns([3, 1])  # Creates 8:1 ratio columns to push the button to the right

    # Create CSV data for download
    csv_data = data.to_csv(index=False).encode('utf-8')
    
    with col_download[1]:  # Place the button in the right column
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name=f'bjb_daily_monitoring_{current_date}.csv',
            mime='text/csv'
        )

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

# Historical Monitoring
with tab2:
    st.header("bjb Points Monitoring")

    # Kalender untuk pemilihan tanggal
    selected_date = st.date_input("Select Date", value=pd.to_datetime('2024-08-01'))

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

    selected_date_str = selected_date.strftime('%Y-%m-%d')

    # Load data based on selected date
    selected_date_str = selected_date.strftime('%Y-%m-%d')
    if selected_date_str in file_map:
        historical_data = pd.read_csv(file_map[selected_date_str])
    else:
        historical_data = None

    # Pastikan data tersedia sebelum menampilkan
    if historical_data is not None:
        st.write(f"Selected date: {selected_date.strftime('%B %d, %Y')}")
         # Download buttons at the right for historical monitoring
        csv_data_hist = historical_data.to_csv(index=False).encode('utf-8')
        col_download_hist = st.columns([3, 1])  # Creates 8:1 ratio columns to push the button to the right
    
        with col_download_hist[1]:
            st.download_button(
                label="Download CSV",
                data=csv_data_hist,
                file_name=f'bjb_historical_monitoring_{selected_date_str}.csv',
                mime='text/csv'
            )

        # Menghitung metrik yang sama seperti di Tab 1
        total_points_earned = historical_data['Total Points Earn'].iloc[0]
        total_points_redeemed = historical_data['Total Points Redeemed'].iloc[0]
        total_admin_fees = historical_data['Total Admin'].iloc[0]
        total_vouchers_redeemed = historical_data['Redeemed Vouchers'].iloc[0]
        total_vouchers_not_redeemed = historical_data['Currently Vouchers'].iloc[0]

        # Display metrics
        col1, col2 = st.columns([1, 1])
        col1.metric("**Total Points Earned Today**", "{:,.0f}".format(total_points_earned))
        col2.metric("**Total Points Redeemed Today**", "{:,.0f}".format(total_points_redeemed))
        col3 = st.columns([1, 2, 1])
        col3[1].metric("**Total Admin Fees Collected Today**", "Rp {:,.0f}".format(total_admin_fees))

        # Voucher overview
        col4, col5 = st.columns(2)
        with col4:
            st.image("1.png", use_column_width=True)
            st.write("**Food & Beverages**")
            st.metric("Redeemed Vouchers", "{:,.0f}".format(total_vouchers_redeemed))
            st.metric("Vouchers Not Yet Redeemed", "{:,.0f}".format(total_vouchers_not_redeemed))

        with col5:
            st.image("2.png", use_column_width=True)
            st.write("**Electricity**")
            st.metric("Redeemed Vouchers", "{:,.0f}".format(total_vouchers_redeemed))
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

        # Pie chart for historical data
        if 'Klasifikasi' in historical_data.columns and 'Total' in historical_data.columns:
            df_classification_hist = historical_data[['Klasifikasi', 'Total']].dropna()
            fig_hist = px.pie(df_classification_hist, names='Klasifikasi', values='Total',
                              title='Classification of Point Sources',
                              labels={'Klasifikasi': 'Point Source', 'Total': 'Total Points'},
                              hole=0.3)  # Optional donut chart
            st.plotly_chart(fig_hist)
        else:
            st.warning("No classification data available for pie chart visualization.")
        
        # Insight Harian berdasarkan tanggal yang dipilih
        insights_map = {
            "2024-08-01": """
            - **Buy & Pay** dominates with 38.16% (58 transactions), showing that customers more often use payment services such as credit, bills, or shopping at the beginning of the month.
            - **E-Wallet** came in second with 22.37% (34 transactions), showing the popularity of e-wallet top-up services such as GoPay, OVO, and DANA.
            - **QRIS** accounted for 15.13% (23 transactions), indicating that QR digital payments are increasingly being used.
            - Non BI-Fast transfers were slightly higher than BI-Fast, with 12.50% (19 transactions) and 11.84% (18 transactions) respectively.
            - At the beginning of the month, most transactions came from payments (Buy & Pay) and e-wallets, while bank transfers still had an important role but did not dominate.
            """,
            "2024-08-02": """
            - **Buy & Pay** increased to 40.49% (66 transactions), confirming that payments are still a priority for customers.
            - **E-Wallets** also rose to 24.54% (40 transactions), showing that e-wallet top-ups continue to be used consistently.
            - **QRIS** remained stable at 14.11% (23 transactions).
            - Non BI-Fast transfers rose to 13.50% (22 transactions), more than BI-Fast which dropped to 7.36% (12 transactions).
            - On the second day, e-wallet payments and top-ups dominated, with Buy & Pay becoming increasingly significant. BI-Fast transfers slightly decreased compared to the first day.
            """,
            "2024-08-03": """
            - **Buy & Pay** remained high with 39.74% (62 transactions), despite a slight drop from the previous day.
            - **E-Wallets** dropped to 19.23% (30 transactions), although it remains in an important position.
            - **QRIS** increased to 18.59% (29 transactions), indicating more active usage.
            - Non BI-Fast transfers at 14.74% (23 transactions), while BI-Fast stabilized at 7.69% (12 transactions).
            - Payment transactions (Buy & Pay) remain dominant, but QRIS shows a significant increase, which may be due to promotions or incentives to use digital payments.
            """,
            "2024-08-04": """
            - **Buy & Pay** was consistently high with 41.33% (62 transactions).
            - **E-Wallets** at 20.67% (31 transactions), remained popular.
            - **QRIS** reached 20.00% (30 transactions), making it a day with significant QRIS contribution.
            - Non BI-Fast transfers decreased to 10.67% (16 transactions), while BI-Fast was at 7.33% (11 transactions).
            - Digital payments (Buy & Pay and QRIS) continued to increase, signaling wider adoption of cashless payments. Transfer transactions slightly reduced, while focus shifted to payments and e-wallets.
            """,
            "2024-08-05": """
            - **Buy & Pay** at 40.25% (64 transactions), maintaining its position as the leading transaction.
            - **E-Wallet** increased again to 21.38% (34 transactions).
            - **QRIS** decreased slightly to 15.72% (25 transactions).
            - Non BI-Fast transfers at 13.21% (21 transactions), and BI-Fast at 9.43% (15 transactions).
            - Payments remain the top priority, but e-wallet transactions also showed a significant increase. QRIS slightly decreased compared to the previous day, but remains important.
            """,
            "2024-08-06": """
            - **Buy & Pay** remained strong at 37.50% (57 transactions), slightly down from the previous day.
            - **QRIS** reached its highest peak of the week with 21.71% (33 transactions), indicating peak QR usage on this day.
            - **E-Wallets** dropped to 16.45% (25 transactions).
            - Non BI-Fast transfers increased slightly to 15.79% (24 transactions), and BI-Fast at 8.55% (13 transactions).
            - QRIS reached peak usage, while payments and transfers still play a big role in daily activities. There is a slight shift from e-wallets to QRIS.
            """,
            "2024-08-07": """
            - **Buy & Pay** at 38.06% (59 transactions), still dominates although slightly declining.
            - **E-Wallets** saw a sharp rise to 25.16% (39 transactions), the highest this week.
            - **QRIS** at 14.84% (23 transactions).
            - Non BI-Fast transfers dropped to 12.90% (20 transactions), and BI-Fast at 9.03% (14 transactions).
            - E-wallets saw a sharp rise, indicating that customers were more active in topping up at the end of the week. Meanwhile, Buy & Pay is still the main transaction type. QRIS declined slightly, but remains important.
            """
        }

        # Tampilkan insight harian sesuai tanggal yang dipilih
        if selected_date_str in insights_map:
            st.header(f"Insights for {selected_date.strftime('%B %d, %Y')}")
            st.write(insights_map[selected_date_str])
        else:
            st.warning("No data available for the selected date.")
    else:
        st.warning("No data available for the selected date.")

# Tab 3: Voucher Recommendations
with tab3:
    st.header("Voucher Recommendations for August 2024")

    # Display the data table
    st.subheader("Point Sources and Transactions in July 2024")
    data = {
        "Sumber Poin": ["Transfer BI-Fast", "Transfer Non BI-Fast", "QRIS", "E-Wallet", "Pay & Buy"],
        "Total": [60, 61, 114, 114, 211],
        "Point Earned": [5480422, 0, 0, 0, 0],
        "Point Redeemed": [950254, 0, 0, 0, 0],
    }
    df_july = pd.DataFrame(data)
    
    # Pie chart for point sources
    fig_pie = px.pie(df_july, names='Sumber Poin', values='Total',
                     title='Distribution of Point Sources in July 2024',
                     labels={'Sumber Poin': 'Point Source', 'Total': 'Total Transactions'},
                     hole=0.3)  # Optional donut chart
    st.plotly_chart(fig_pie)

    # Display points earned and redeemed in two columns
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Total Points Earned")
        st.metric("{:,.0f}".format(df_july['Point Earned'].sum()))
    
    with col2:
        st.subheader("Total Points Redeemed")
        st.metric("{:,.0f}".format(df_july['Point Redeemed'].sum()))

    # Insights
    st.subheader("Insights in July 2024")
    insights = """
    1. **Dominant Point Sources**:
        - **Pay & Buy** transactions significantly dominated the point earning, contributing to a total of **211 transactions**. This indicates a strong customer engagement in using payment services for purchases, likely reflecting consumer preferences for convenience and rewards from everyday spending.
        - **QRIS** and **E-Wallet** transactions both had **114 transactions**, showing a balanced interest in digital payment solutions.

    2. **Transfer Activities**:
        - **Transfer BI-Fast** had **60 transactions** with a total of **5,480,422 points earned**, indicating that this method is valued by customers for quick and efficient fund transfers. However, it’s worth noting that the redeemed points from this source are notably lower than earned points.
        - **Transfer Non BI-Fast** had **61 transactions**, but the data does not show any points earned or redeemed, suggesting a need for further promotion or incentives for this transfer method.
    """
    st.write(insights)

    # Recommendations for Voucher Redemption
    st.write("Based on the data from the previous month, here are the recommended vouchers:")
    recommendations = """
    1. **Focus on Everyday Spending**:
        - **Voucher Ideas**: Offer vouchers for popular retail partners (e.g., grocery stores, online shopping platforms) where customers can easily redeem points. This can encourage further spending and loyalty to the bank.

    2. **Incentives for Digital Payments**:
        - **QRIS and E-Wallet Promotions**: Create vouchers or cashback offers specifically for QRIS and E-Wallet transactions. Highlight these in marketing materials to increase engagement with these payment methods.

    3. **Transfer Promotions**:
        - Consider introducing promotions for **Transfer Non BI-Fast** to stimulate point earning and redemption. For example, offering bonus points for every transfer made could motivate customers to use this service more frequently.

    4. **Seasonal or Event-Based Vouchers**:
        - Align vouchers with upcoming holidays or local events in August to encourage point redemption. This could include vouchers for entertainment, dining, or travel, appealing to customers looking to enjoy their points during special occasions.

    5. **Feedback and Surveys**:
        - Engage customers through surveys to determine what types of vouchers they would be most interested in. Tailoring offerings based on customer feedback can enhance satisfaction and loyalty.
    """
    st.write(recommendations)
