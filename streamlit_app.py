import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_carousel import carousel
import base64
from PIL import Image
import time

# Function to convert image to base64
# Function to convert image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Convert the logo image to base64
logo_base64 = image_to_base64("Frame 110.png")  # Adjust the path as necessary
logo_html = f'<img src="data:image/png;base64,{logo_base64}" width="100" />'

# Hardcoded username and password for demonstration
USERNAME = "admin"
PASSWORD = "password123"

# Initialize session state variables if they don't exist
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False  # Default to not logged in

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"  # Default page

if "section" not in st.session_state:
    st.session_state.section = "Dashboard"  # Default section for Dashboard

# Function for handling login
def login():
    # Set background color and style
    st.markdown("""
        <style>
            body {
                background-color: #A4C8E1; /* Hijau */
                color: #005DAA; /* Biru */
            }
            .login-container {
                text-align: center;
                margin-top: 50px;
            }
            .footer {
                text-align: right;
                position: fixed;
                bottom: 10px;
                right: 10px;
                font-size: 12px;
                color: gray;
            }
            .stButton button {
                width: 100%;
                padding: 10px;
                background-color: #005DAA;
                color: white;
                border-radius: 5px;
                font-size: 18px;
                border: none;
                cursor: pointer;
            }
        </style>
    """, unsafe_allow_html=True)

    # Center the logo and text
    st.markdown("""
        <div class="login-container">
            """ + logo_html + """
            <h1 style='font-size: 50px; color: #005DAA;'>BOOST</h1>
            <p style='font-size: 20px; color: #005DAA;'>(bjb Bonus Points)</p>
        </div>
    """, unsafe_allow_html=True)

    # Add login form below BOOST section
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            st.experimental_rerun()  # Refresh the app to go to the dashboard
        else:
            st.error("Invalid username or password!")

    # Add "made by ITDP 2024" at the bottom right
    st.markdown('<div class="footer">ITDP 2024</div>', unsafe_allow_html=True)

# Example placeholder for other pages
def dashboard_page():
    
    # Function to load data (using cache to avoid reloading)
    @st.cache_resource
    def load_data(file):
        return pd.read_csv(file)

    # File for August 8 (default file)
    default_file = 'loyalty_points_log_8.csv'
    data = load_data(default_file)

    # Ensure the 'Klasifikasi' and 'Total' columns are present
    if 'Klasifikasi' in data.columns and 'Total' in data.columns:
        df_classification = data[['Klasifikasi', 'Total']].dropna()

    # Main content area
    if st.session_state.section == "Dashboard":
        st.header("BOOST Dashboard")

        st.markdown("""
        <style>
        .custom-divider {
            border: none;
            border-top: 2px solid #D3D3D3;  /* Customize the color and thickness */
            margin-top: 1px;
            margin-bottom: 1px;
        }
        </style>
        <hr class="custom-divider">
        """, unsafe_allow_html=True)

        # Date picker (default to August 8, 2024)
        selected_date = st.date_input("Select Date", value=pd.to_datetime('2024-08-08'))

        # Mapping of CSV files for August 1-7, 2024
        file_map = {
            "2024-08-01": 'loyalty_points_log_1.csv',
            "2024-08-02": 'loyalty_points_log_2.csv',
            "2024-08-03": 'loyalty_points_log_3.csv',
            "2024-08-04": 'loyalty_points_log_4.csv',
            "2024-08-05": 'loyalty_points_log_5.csv',
            "2024-08-06": 'loyalty_points_log_6.csv',
            "2024-08-07": 'loyalty_points_log_7.csv',
            "2024-08-08": 'loyalty_points_log_8.csv'
        }

        # Convert selected date to string and pick file based on the date
        selected_date_str = selected_date.strftime('%Y-%m-%d')
        selected_file = file_map.get(selected_date_str, default_file)

        # Load data based on the selected date
        data = load_data(selected_file)

        st.write(f"Selected date: {selected_date.strftime('%B %d, %Y')}")

        # Place Download CSV button in the far right
        st.markdown("""
        <style>
        div.stDownloadButton > button {
            width: 100%;
            padding: 10px;
            background-color: #2ECC71;  /* Greenish-blue background color */
            color: white;
            border-radius: 5px;
            font-size: 18px;
            border: none;
            cursor: pointer;
        }
        </style>
        """, unsafe_allow_html=True)

        cols = st.columns([8, 1])  # 9 for empty space, 1 for the button
        with cols[-1]:  # Use the last column
            csv_data = data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="**Download CSV**",
                data=csv_data,
                file_name=f'bjb_monitoring_{selected_date_str}.csv',
                mime='text/csv'
        )

        # Display Metrics
        total_points_earned = data['Total Points Earn'].iloc[0]
        total_points_redeemed = data['Total Points Redeemed'].iloc[0]
        total_admin_fees = data['Total Admin'].iloc[0]
        total_vouchers_redeemed = data['Redeemed Vouchers'].iloc[0]
        total_vouchers_not_redeemed = data['Currently Vouchers'].iloc[0]

        # Custom HTML and CSS for layout
        html_code = f"""
        <style>
        .container {{
            display: flex;               /* Flexbox to arrange boxes side by side */
            justify-content: space-around; /* Space items evenly */
            margin-bottom: 20px;        /* Margin below the container */
        }}

        .box {{
            border: 2px solid #f9f9f9;  /* Green border for each box */
            border-radius: 5px;         /* Rounded corners */
            padding: 20px;              /* Padding inside the box */
            background-color: #f9f9f9;  /* Light background color */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Slight shadow */
            flex: 1;                    /* Allow boxes to grow equally */
            margin: 0 10px;             /* Margin between boxes */
            text-align: center;         /* Centered text */
        }}

        .label {{
            font-size: 20px;            /* Font size for labels */
            font-weight: bold;          /* Bold text for labels */
            color: #000;                /* Black color for text */
        }}

        .value {{
            display: block;             /* Forces values to be on a new line */
            font-size: 28px;            /* Larger font size for values */
            margin-top: 10px;           /* Space between the label and the value */
        }}
        </style>

        <div class="container">
            <div class="box">
                <div class="label">Total Points Earned</div>
                <span class="value">{total_points_earned:,.0f}</span>
            </div>
            <div class="box">
                <div class="label">Total Points Redeemed</div>
                <span class="value">{total_points_redeemed:,.0f}</span>
            </div>
            <div class="box">
                <div class="label">Total Admin Fees Collected</div>
                <span class="value">Rp {total_admin_fees:,.0f}</span>
            </div>
        </div>
        """

        # Render the HTML in Streamlit
        st.markdown(html_code, unsafe_allow_html=True)

        # Voucher Overview with Carousel
        st.markdown("""
        <style>
        .custom-divider {
            border: none;
            border-top: 2px solid #D3D3D3;  /* Customize the color and thickness */
            margin-top: 1px;
            margin-bottom: 1px;
        }
        </style>
        <hr class="custom-divider">
        """, unsafe_allow_html=True)
        
        st.header("Vouchers Overview")

        st.markdown("""
        <style>
        .custom-divider {
            border: none;
            border-top: 2px solid #D3D3D3;  /* Customize the color and thickness */
            margin-top: 1px;
            margin-bottom: 1px;
        }
        </style>
        <hr class="custom-divider">
        """, unsafe_allow_html=True)
    
        # Example voucher images and names (reorganized as per your requirement)
        voucher_images = [
            # Page 1
            {"image": "1.png", "name": "Game Online"},
            {"image": "11.png", "name": "Platform Streaming"},
            {"image": "4.png", "name": "Token Listrik"},
            {"image": "9.png", "name": "Tempat Rekreasi"},
            {"image": "10.png", "name": "Logam Mulia"},
            
            # Page 2
            {"image": "2.png", "name": "Food and Beverages"},
            {"image": "3.png", "name": "Belanja Online"},
            {"image": "5.png", "name": "Pulsa"},
            {"image": "6.png", "name": "Bioskop"},
            {"image": "8.png", "name": "Barang Elektronik"},
            
            # Page 3
            {"image": "7.png", "name": "Aksesoris"},
            {"image": "12.png", "name": "Convinience Store"},
            {"image": "13.png", "name": "Travelling"},
            {"image": "14.png", "name": "Fashion"},
            {"image": "15.png", "name": "Penginapan"},
        ]

    # Initialize session state for carousel index
        if 'voucher_index' not in st.session_state:
            st.session_state.voucher_index = 0

        # Display 5 vouchers on each page
        vouchers_per_page = 5
        total_vouchers = len(voucher_images)
        total_pages = (total_vouchers + vouchers_per_page - 1) // vouchers_per_page

        # Calculate start and end indices for vouchers to be displayed on the current page
        start_idx = st.session_state.voucher_index * vouchers_per_page
        end_idx = min(start_idx + vouchers_per_page, total_vouchers)

        # Display vouchers in a grid
        cols = st.columns(5)  # Create 5 columns for the grid
        for idx, voucher in enumerate(voucher_images[start_idx:end_idx]):
            with cols[idx % 5]:  # Place each voucher in a column
                st.image(voucher['image'], use_column_width=True)
                st.write(f"**{voucher['name']}**")
                # Example metrics (replace with actual values if available)
                st.metric("Redeemed Vouchers", "0")
                st.metric("Vouchers Not Yet Redeemed", "20")

        # Add "Previous" and "Next" buttons for navigation
        st.markdown("""
            <style>
            .stButton button.prev-btn {
                width: 5%;
                padding: 10px;
                background-color: #005DAA;
                color: white;
                border-radius: 5px;
                font-size: 18px;
                border: none;
                cursor: pointer;
            }
            .stButton button.next-btn {
                width: 5%;
                padding: 10px;
                background-color: #005DAA;
                color: white;
                border-radius: 5px;
                font-size: 18px;
                border: none;
                cursor: pointer;
            }
            </style>
        """, unsafe_allow_html=True)

        # Columns for Previous and Next buttons
        col_prev, col_next = st.columns([9, 9])

        with col_prev:
            # Add 'prev-btn' class for the previous button
            if st.button("Previous", key='prev', args=None, kwargs=None):
                if st.session_state.voucher_index > 0:
                    st.session_state.voucher_index -= 1

        with col_next:
            # Add 'next-btn' class for the next button
            if st.button("Next", key='next', args=None, kwargs=None):
                if st.session_state.voucher_index < total_pages - 1:
                    st.session_state.voucher_index += 1

        # Display the current page number and total pages
        st.write(f"Page {st.session_state.voucher_index + 1} of {total_pages}")

        # Transaction Activity
        st.markdown("""
        <style>
        .custom-divider {
            border: none;
            border-top: 2px solid #D3D3D3;  /* Customize the color and thickness */
            margin-top: 1px;
            margin-bottom: 1px;
        }
        </style>
        <hr class="custom-divider">
        """, unsafe_allow_html=True)

        st.header("Transaction Activity")

        st.markdown("""
        <style>
        .custom-divider {
            border: none;
            border-top: 2px solid #D3D3D3;  /* Customize the color and thickness */
            margin-top: 1px;
            margin-bottom: 1px;
        }
        </style>
        <hr class="custom-divider">
        """, unsafe_allow_html=True)

        st.dataframe(data[['Loyalty Point ID', 'CIF', 'Log ID', 'Tanggal Pemberian', 'Sumber Poin', 'Keterangan', 'Jumlah Poin']].head(5))

        # Pie Chart for Point Classification
        st.markdown("""
        <style>
        .custom-divider {
            border: none;
            border-top: 2px solid #D3D3D3;  /* Customize the color and thickness */
            margin-top: 1px;
            margin-bottom: 1px;
        }
        </style>
        <hr class="custom-divider">
        """, unsafe_allow_html=True)

        st.header("Daily Insights")

        st.markdown("""
        <style>
        .custom-divider {
            border: none;
            border-top: 2px solid #D3D3D3;  /* Customize the color and thickness */
            margin-top: 1px;
            margin-bottom: 1px;
        }
        </style>
        <hr class="custom-divider">
        """, unsafe_allow_html=True)

        if 'Klasifikasi' in data.columns and 'Total' in data.columns:
            df_classification = data[['Klasifikasi', 'Total']].dropna()
            fig = px.pie(df_classification, names='Klasifikasi', values='Total',
                         title='Classification of Point Sources', hole=0.3)
            st.plotly_chart(fig)

        # Expanded insights based on selected date
        insights_map = {
            "2024-08-01": [
                "• <strong>Buy & Pay</strong> dominates with <strong>38.16%</strong>, showing that customers more often use payment services such as credit, bills, or shopping at the beginning of the month.",
                "• <strong>E-Wallet</strong> came in second with <strong>22.37%</strong>, showing the popularity of e-wallet top-up services such as <strong>GoPay</strong>, <strong>OVO</strong>, and <strong>DANA</strong>.",
                "• <strong>QRIS</strong> accounted for <strong>15.13%</strong>, indicating that QR digital payments are increasingly being used.",
                "• <strong>Non BI-Fast</strong> transfers were slightly higher than <strong>BI-Fast</strong>, with <strong>12.50%</strong> and <strong>11.84%</strong> respectively.",
                "• At the beginning of the month, most transactions came from <strong>payments (Buy & Pay)</strong> and <strong>e-wallets</strong>, while <strong>bank transfers</strong> still had an important role but did not dominate."
            ],
            "2024-08-02": [
                "• <strong>Buy & Pay</strong> increased to <strong>40.49%</strong>, confirming that payments are still a priority for customers.",
                "• <strong>E-Wallets</strong> also rose to <strong>24.54%</strong>, showing that e-wallet top-ups continue to be used consistently.",
                "• <strong>QRIS</strong> remained stable at <strong>14.11%</strong>.",
                "• <strong>Non BI-Fast</strong> transfers rose to <strong>13.50%</strong>, more than <strong>BI-Fast</strong> which dropped to <strong>7.36%</strong>.",
                "• On the second day, <strong>e-wallet payments</strong> and <strong>top-ups</strong> dominated, with <strong>Buy & Pay</strong> becoming increasingly significant. <strong>BI-Fast</strong> transfers slightly decreased compared to the first day."
            ],
            "2024-08-03": [
                "• <strong>Buy & Pay</strong> remained high with <strong>39.74%</strong>, despite a slight drop from the previous day.",
                "• <strong>E-Wallets</strong> dropped to <strong>19.23%</strong>, although it remains in an important position.",
                "• <strong>QRIS</strong> increased to <strong>18.59%</strong>, indicating more active usage.",
                "• <strong>Non BI-Fast</strong> transfers at <strong>14.74%</strong>, while <strong>BI-Fast</strong> stabilized at <strong>7.69%</strong>.",
                "• Payment transactions <strong>(Buy & Pay)</strong> remain dominant, but <strong>QRIS</strong> shows a significant increase, which may be due to promotions or incentives to use digital payments."
            ],
            "2024-08-04": [
                "• <strong>Buy & Pay</strong> was consistently high with <strong>41.33%</strong>.",
                "• <strong>E-Wallets</strong> at <strong>20.67%</strong>, remained popular.",
                "• <strong>QRIS</strong> reached <strong>20.00%</strong>, making it a day with significant QRIS contribution.",
                "• <strong>Non BI-Fast</strong> transfers decreased to <strong>10.67%</strong>, while <strong>BI-Fast</strong> was at <strong>7.33%</strong>.",
                "• Digital payments <strong>(Buy & Pay and QRIS)</strong> continued to increase, signaling wider adoption of cashless payments. Transfer transactions slightly reduced, while focus shifted to <strong>payments</strong> and <strong>e-wallets</strong>."
            ],
            "2024-08-05": [
                "• <strong>Buy & Pay</strong> at <strong>40.25%</strong>, maintaining its position as the leading transaction.",
                "• <strong>E-Wallet</strong> increased again to <strong>21.38%</strong>.",
                "• <strong>QRIS</strong> decreased slightly to <strong>15.72%</strong>.",
                "• <strong>Non BI-Fast</strong> transfers at <strong>13.21%</strong>, and <strong>BI-Fast</strong> at <strong>9.43%</strong>.",
                "• <strong>Payments</strong> remain the top priority, but <strong>e-wallet</strong> transactions also showed a significant increase. <strong>QRIS</strong> slightly decreased compared to the previous day, but remains important."
            ],
            "2024-08-06": [
                "• <strong>Buy & Pay</strong> remained strong at <strong>37.50%</strong>, slightly down from the previous day.",
                "• <strong>QRIS</strong> reached its highest peak of the week with <strong>21.71%</strong>, indicating peak QR usage on this day.",
                "• <strong>E-Wallets</strong> dropped to <strong>16.45%</strong>.",
                "• <strong>Non BI-Fast</strong> transfers increased slightly to <strong>15.79%</strong> (24 transactions), and <strong>BI-Fast</strong> at <strong>8.55%</strong>.",
                "• <strong>QRIS</strong> reached peak usage, while <strong>payments</strong> and <strong>transfers</strong> still play a big role in daily activities. There is a slight shift from <strong>e-wallets</strong> to <strong>QRIS</strong>."
            ],
            "2024-08-07": [
                "• <strong>Buy & Pay</strong> at <strong>38.06%</strong>, still dominates although slightly declining.",
                "• <strong>E-Wallets</strong> saw a sharp rise to <strong>25.16%</strong>, the highest this week.",
                "• <strong>QRIS</strong> at <strong>14.84%</strong>.",
                "• <strong>Non BI-Fast</strong> transfers dropped to <strong>12.90%</strong>, and <strong>BI-Fast</strong> at <strong>9.03%</strong>.",
                "• <strong>E-wallets</strong> saw a sharp rise, indicating that customers were more active in topping up at the end of the week. Meanwhile, <strong>Buy & Pay</strong> is still the main transaction type. <strong>QRIS</strong> declined slightly, but remains important."
            ],
            "2024-08-08": [
                "• <strong>Buy & Pay</strong> contributes the largest share of points earned at <strong>38.19%</strong>, indicating that most customers prefer using the platform for purchases and payments.",
                "• <strong>E-Wallet</strong> transactions follow, contributing <strong>20.14%</strong> of the total points earned, showing significant adoption of digital wallet payments.",
                "• <strong>QRIS</strong> payments make up <strong>19.44%</strong>, which reflects the growing use of QR-based transactions in the customer base.",
                "• <strong>Transfer Non BI-Fast</strong> represent smaller but still notable shares of transactions, showing that both real-time and regular transfers are important but less dominant compared to purchase/payment activities."
            ]
        }
    
    st.markdown("""
    <style>
    .insight-box {
        border: 2px solid #e0e0e0; /* Border color */
        border-radius: 10px;       /* Rounded corners */
        padding: 15px;              /* Padding inside the box */
        background-color: #f9f9f9; /* Light background color */
        margin-bottom: 20px;        /* Space below each box */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Shadow for depth */
    }
    </style>
    """, unsafe_allow_html=True)

    # Display multiple insights based on the selected date
    if selected_date_str in insights_map:
        insights = insights_map[selected_date_str]
        
        # Group insights in sets of five
        for i in range(0, len(insights), 5):
            # Get the next five insights (or fewer if at the end)
            grouped_insights = insights[i:i + 5]
            insights_content = "<br>".join(grouped_insights)  # Join them with line breaks

            # Wrap the grouped insights in a styled box
            st.markdown(f"""
                <div class="insight-box">
                    {insights_content} <!-- Display the grouped insights -->
                </div>
            """, unsafe_allow_html=True)

    else:
        st.warning("No data available for the selected date.")

def recommendation_page():
    st.header("Voucher Recommendations for August 2024")

    st.markdown("""
        <style>
        .custom-divider {
            border: none;
            border-top: 2px solid #D3D3D3;  /* Customize the color and thickness */
            margin-top: 1px;
            margin-bottom: 1px;
        }
        </style>
        <hr class="custom-divider">
        """, unsafe_allow_html=True)
    
    # Display the data table
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
        st.markdown("""
            <div style="border: 1px solid #ddd; padding: 10px; width: 30%; border-radius: 10px; background-color: #f9f9f9; text-align: center;">
                <strong>Points Earned</strong>
                <div style="font-size: 24px; font-weight: bold;">{points_earned}</div>
            </div>
        """.format(
            points_earned="{:,.0f}".format(df_july['Point Earned'].sum())
        ), unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style="border: 1px solid #ddd; padding: 10px; width: 30%; border-radius: 10px; background-color: #f9f9f9; text-align: center;">
                <strong>Points Redeemed</strong>
                <div style="font-size: 24px; font-weight: bold;">{points_redeemed}</div>
            </div>
        """.format(
            points_redeemed="{:,.0f}".format(df_july['Point Redeemed'].sum())
        ), unsafe_allow_html=True)
    
    st.markdown("""
        <style>
        .custom-divider {
            border: none;
            border-top: 2px solid #D3D3D3;  /* Customize the color and thickness */
            margin-top: 1px;
            margin-bottom: 1px;
        }
        </style>
        <hr class="custom-divider">
        """, unsafe_allow_html=True)
    
    st.subheader("Insights in July 2024")

    st.markdown("""
        <style>
        .custom-divider {
            border: none;
            border-top: 2px solid #D3D3D3;  /* Customize the color and thickness */
            margin-top: 1px;
            margin-bottom: 1px;
        }
        </style>
        <hr class="custom-divider">
        """, unsafe_allow_html=True)
    
    insights = """
    <div style="border: 1px solid #ddd; padding: 15px; border-radius: 10px; background-color: #f9f9f9;">
        <p><strong>1. Dominant Point Sources:</strong></p>
        <ul>
            <li><strong>Pay & Buy</strong> transactions significantly dominated the point earning, contributing to a total of <strong>37.7%</strong>. This indicates a strong customer engagement in using payment services for purchases, likely reflecting consumer preferences for convenience and rewards from everyday spending.</li>
            <li><strong>QRIS</strong> and <strong>E-Wallet</strong> transactions both had <strong>20.4%</strong>, showing a balanced interest in digital payment solutions.</li>
        </ul>
        <p><strong>2. Transfer Activities:</strong></p>
        <ul>
            <li><strong>Transfer BI-Fast</strong> had <strong>10.7%</strong> with a total of <strong>5,480,422 points earned</strong>, indicating that this method is valued by customers for quick and efficient fund transfers. However, it’s worth noting that the redeemed points from this source are notably lower than earned points.</li>
            <li><strong>Transfer Non BI-Fast</strong> had <strong>10.9%</strong>, but the data does not show any points earned or redeemed, suggesting a need for further promotion or incentives for this transfer method.</li>
        </ul>
    </div>
    """
    # Display the insights in a box layout
    st.markdown(insights, unsafe_allow_html=True)

    # Recommendations for Voucher Redemption
    st.write("**Based on the data from the previous month, here are the recommended vouchers for next month:**")
    st.markdown("""
        <style>
        .custom-divider {
            border: none;
            border-top: 2px solid #D3D3D3;  /* Customize the color and thickness */
            margin-top: 1px;
            margin-bottom: 1px;
        }
        </style>
        <hr class="custom-divider">
        """, unsafe_allow_html=True)
    
    st.subheader("Recommendation")
    st.markdown("""
        <style>
        .custom-divider {
            border: none;
            border-top: 2px solid #D3D3D3;  /* Customize the color and thickness */
            margin-top: 1px;
            margin-bottom: 1px;
        }
        </style>
        <hr class="custom-divider">
        """, unsafe_allow_html=True)
    recommendations = """
    <div style="border: 1px solid #ddd; padding: 15px; border-radius: 10px; background-color: #f9f9f9;">
        <h4>Voucher Recommendations</h4>
        <p style="margin-bottom: 1px;"><strong>1. Focus on Everyday Spending:</strong></p>
        <p style="margin-bottom: 20px;"><strong>Voucher Ideas:</strong> Offer vouchers for popular retail partners (e.g., grocery stores, online shopping platforms) where customers can easily redeem points. This can encourage further spending and loyalty to the bank.</p>
        <p style="margin-bottom: 1px;"><strong>2. Incentives for Digital Payments:</strong></p>
        <p style="margin-bottom: 20px;"><strong>QRIS and E-Wallet Promotions:</strong> Create vouchers or cashback offers specifically for QRIS and E-Wallet transactions. Highlight these in marketing materials to increase engagement with these payment methods.</p>
        <p style="margin-bottom: 1px;"><strong>3. Transfer Promotions:</strong></p>
        <p style="margin-bottom: 20px;">Consider introducing promotions for <strong>Transfer Non BI-Fast</strong> to stimulate point earning and redemption. For example, offering bonus points for every transfer made could motivate customers to use this service more frequently.</p>
        <p style="margin-bottom: 1px;"><strong>4. Seasonal or Event-Based Vouchers:</strong></p>
        <p style="margin-bottom: 20px;">Align vouchers with upcoming holidays or local events in August to encourage point redemption. This could include vouchers for entertainment, dining, or travel, appealing to customers looking to enjoy their points during special occasions.</p>
        <p style="margin-bottom: 1px;"><strong>5. Feedback and Surveys:</strong></p>
        <p style="margin-bottom: 20px;">Engage customers through surveys to determine what types of vouchers they would be most interested in. Tailoring offerings based on customer feedback can enhance satisfaction and loyalty.</p>
    </div>
    """

    # Display the recommendations inside a box layout
    st.markdown(recommendations, unsafe_allow_html=True)

def voucher_page():
    # Define voucher prices
    voucher_prices = {
        "Game Online": 50000,
        "Platform Streaming": 50000,
        "Token Listrik": 20000,
        "Tempat Rekreasi": 100000,  # Added new voucher
        "Logam Mulia": 1000000   # Added new voucher
    }

    # Define maximum order value
    MAX_ORDER_VALUE = 10000000

    # Initialize session state for voucher quantities
    if "voucher_quantities" not in st.session_state:
        st.session_state.voucher_quantities = {k: 0 for k in voucher_prices.keys()}
        st.session_state.voucher_order_total = 0
        st.session_state.order_success = False

    st.title("Voucher Order")
    st.markdown("""
        <style>
        .custom-divider {
            border: none;
            border-top: 2px solid #D3D3D3;  /* Customize the color and thickness */
            margin-top: 1px;
            margin-bottom: 1px;
        }
        </style>
        <hr class="custom-divider">
        """, unsafe_allow_html=True)

    # Define image paths or URLs for the vouchers
    voucher_images = {
        "Game Online": "1.png",  # Replace with actual paths or URLs
        "Platform Streaming": "11.png",
        "Token Listrik": "4.png",
        "Tempat Rekreasi": "9.png",  # New images
        "Logam Mulia": "10.png"   # New images
    }

    # Create columns for displaying vouchers
    cols = st.columns(5)  # 5 columns for 5 vouchers

    # Display voucher options with images in columns
    for i, (voucher, price) in enumerate(voucher_prices.items()):
        with cols[i]:
            st.image(voucher_images[voucher], caption=voucher, use_column_width=True)
            st.write(f"Price: {price:,} IDR")  # Display the price of the voucher
            qty = st.number_input(f"Quantity of {voucher}", min_value=0, step=1, key=voucher)
            st.session_state.voucher_quantities[voucher] = qty

    # Calculate total order value
    st.session_state.voucher_order_total = sum(qty * voucher_prices[voucher] for voucher, qty in st.session_state.voucher_quantities.items())

    st.markdown("""
        <div class="total-box">
            <p><strong>Total Order Value:</strong> {:,.0f} IDR</p>
            <p><strong>Maximum Order Value:</strong> {:,.0f} IDR</p>
        </div>
        """.format(st.session_state.voucher_order_total, MAX_ORDER_VALUE), unsafe_allow_html=True)

    # Confirm order button
    if st.button("Submit Order"):
        if st.session_state.voucher_order_total > MAX_ORDER_VALUE:
            st.error(f"Order total cannot exceed {MAX_ORDER_VALUE:,} IDR.")
        else:
            st.success("Your order has been placed! Waiting for vendor confirmation...")
            time.sleep(5)  # Simulate a delay for vendor response
            
            # Notify user about vendor confirmation
            st.success("Vendor has received your voucher request.")
            time.sleep(5)  # Simulate a delay for additional response

            # Show added vouchers
            added_vouchers = [f"{voucher}: {qty}" for voucher, qty in st.session_state.voucher_quantities.items() if qty > 0]
            st.write("The following vouchers have been added by the vendor:")
            for voucher in added_vouchers:
                st.write(voucher)
            
            # Reset quantities after order
            st.session_state.voucher_quantities = {k: 0 for k in voucher_prices.keys()}

# Main logic
if st.session_state.logged_in:
    
    # Load the BOOST logo (ensure you have the image file in the correct path)
    boost_logo = "Frame 110.png"  # Replace with actual path

    # Function to convert image to base64
    def get_base64_image(image_path):
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_image

    # Get base64 string of the logo
    boost_logo_base64 = get_base64_image(boost_logo)

    # Sidebar navigation and logout logic
    st.sidebar.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{boost_logo_base64}" alt="BOOST" style="width:60px; height:30px;">
            <h2 style="margin-left: 10px;">BOOST</h2>
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown("""
        <style>
        .stButton button {
                width: 50%;
                padding: 10px;
                background-color: #005DAA;
                color: white;
                border-radius: 5px;
                font-size: 18px;
                border: none;
                cursor: pointer;
            }
        </style>
        """, unsafe_allow_html=True)
    
    st.sidebar.button("Dashboard", on_click=lambda: st.session_state.update(page="Dashboard"))
    st.sidebar.button("Recommendation", on_click=lambda: st.session_state.update(page="Recommendation"))
    st.sidebar.button("Voucher", on_click=lambda: st.session_state.update(page="Voucher"))

    # Log out button at the bottom
    st.sidebar.markdown(
    """
    <style>
    .sidebar-footer {
        position: absolute;
        bottom: 20px;  /* Distance from the bottom */
        width: 100%;   /* Full width */
        padding: 10px; /* Padding for better spacing */
    }
    .spacer {
        height: 530px; /* Adjust the height as needed for spacing */
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    # Spacer div to push the logout button down
    st.sidebar.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

    # Log out button at the bottom
    st.sidebar.markdown("<div class='sidebar-footer'>", unsafe_allow_html=True)
    if st.sidebar.button("Log out"):
        st.session_state.logged_in = False
        st.experimental_rerun()
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    # Display the appropriate page
    if st.session_state.page == "Dashboard":
        dashboard_page()
    elif st.session_state.page == "Recommendation":
        recommendation_page()
    elif st.session_state.page == "Voucher":
        voucher_page()
else:
    login()
