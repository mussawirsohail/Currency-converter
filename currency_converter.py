import streamlit as st
import requests
import json
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Currency Converter",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for black and yellow theme
st.markdown("""
<style>
    .stApp {
        background-color: #121212;
        color: #FFD700;
    }
    .stButton>button {
        background-color: #FFD700;
        color: black;
        font-weight: bold;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        background-color: #1E1E1E;
        color: #FFD700;
        border: 1px solid #FFD700;
    }
    .stSelectbox>div>div>div {
        background-color: #1E1E1E;
        color: #FFD700;
        border: 1px solid #FFD700;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #FFD700;
    }
    .stDataFrame {
        border: 1px solid #FFD700;
    }
    div[data-baseweb="select"] > div {
        background-color: #1E1E1E;
        color: #FFD700;
        border: 1px solid #FFD700;
    }
    div[data-baseweb="select"] > div > div > div {
        color: #FFD700;
    }
    div[data-baseweb="select"] svg {
        color: #FFD700;
    }
    div[role="listbox"] ul {
        background-color: #1E1E1E;
    }
    div[role="listbox"] li {
        color: #FFD700;
    }
    div[role="listbox"] li:hover {
        background-color: #2A2A2A;
    }
    .stNumberInput>div>div>input {
        background-color: #1E1E1E;
        color: #FFD700;
        border: 1px solid #FFD700;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.title("💰 Currency Converter")
st.markdown("Convert between currencies with real-time exchange rates")

# Currency names dictionary - only include currencies we know
currency_names = {
    "USD": "US Dollar",
    "EUR": "Euro",
    "GBP": "British Pound",
    "JPY": "Japanese Yen",
    "AUD": "Australian Dollar",
    "CAD": "Canadian Dollar",
    "CHF": "Swiss Franc",
    "CNY": "Chinese Yuan",
    "HKD": "Hong Kong Dollar",
    "NZD": "New Zealand Dollar",
    "SEK": "Swedish Krona",
    "KRW": "South Korean Won",
    "SGD": "Singapore Dollar",
    "NOK": "Norwegian Krone",
    "MXN": "Mexican Peso",
    "INR": "Indian Rupee",
    "RUB": "Russian Ruble",
    "ZAR": "South African Rand",
    "TRY": "Turkish Lira",
    "BRL": "Brazilian Real",
    "TWD": "Taiwan Dollar",
    "DKK": "Danish Krone",
    "PLN": "Polish Zloty",
    "THB": "Thai Baht",
    "IDR": "Indonesian Rupiah",
    "HUF": "Hungarian Forint",
    "CZK": "Czech Koruna",
    "ILS": "Israeli Shekel",
    "CLP": "Chilean Peso",
    "PHP": "Philippine Peso",
    "AED": "UAE Dirham",
    "COP": "Colombian Peso",
    "SAR": "Saudi Riyal",
    "MYR": "Malaysian Ringgit",
    "RON": "Romanian Leu",
    "ARS": "Argentine Peso",
    "PKR": "Pakistani Rupee",
    "QAR": "Qatari Riyal",
    "KWD": "Kuwaiti Dinar",
    "VND": "Vietnamese Dong",
    "EGP": "Egyptian Pound",
    "NGN": "Nigerian Naira",
    "BDT": "Bangladeshi Taka",
    "PEN": "Peruvian Sol",
    "LKR": "Sri Lankan Rupee",
    "MAD": "Moroccan Dirham",
    "JOD": "Jordanian Dinar",
    "OMR": "Omani Rial",
    "BHD": "Bahraini Dinar",
    "KES": "Kenyan Shilling",
    "DZD": "Algerian Dinar",
    "TND": "Tunisian Dinar",
    "UGX": "Ugandan Shilling",
    "GHS": "Ghanaian Cedi",
    "UAH": "Ukrainian Hryvnia",
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    "XRP": "Ripple",
    "LTC": "Litecoin",
    "BCH": "Bitcoin Cash",
    "BNB": "Binance Coin",
    "EOS": "EOS",
    "XLM": "Stellar",
    "ADA": "Cardano",
    "TRX": "TRON",
    "DOT": "Polkadot",
    "LINK": "Chainlink",
    "XMR": "Monero",
    "DOGE": "Dogecoin"
}

# Function to fetch exchange rates
def get_exchange_rates(base_currency="USD"):
    try:
        # Using ExchangeRate-API (free tier)
        url = f"https://open.er-api.com/v6/latest/{base_currency}"
        response = requests.get(url)
        data = response.json()
        
        if data["result"] == "success":
            return data["rates"], data["time_last_update_utc"]
        else:
            st.error("Failed to fetch exchange rates")
            return None, None
    except Exception as e:
        st.error(f"Error fetching exchange rates: {e}")
        return None, None

# Get exchange rates
rates, last_updated = get_exchange_rates()

if rates:
    # Filter to only include currencies we know the names of
    known_currencies = [code for code in sorted(rates.keys()) if code in currency_names]
    
    # Create two columns for input and output
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("From")
        from_currency = st.selectbox(
            "Source Currency", 
            options=known_currencies,
            format_func=lambda x: f"{x} ({currency_names[x]})",
            index=known_currencies.index("USD") if "USD" in known_currencies else 0
        )
        amount = st.number_input("Amount", min_value=0.01, value=1.0, step=0.01)
    
    with col2:
        st.subheader("To")
        to_currency = st.selectbox(
            "Target Currency", 
            options=known_currencies,
            format_func=lambda x: f"{x} ({currency_names[x]})",
            index=known_currencies.index("EUR") if "EUR" in known_currencies else 0
        )
    
    # Convert button
    if st.button("Convert", key="convert_button"):
        # If base currency is not USD, we need to normalize
        if from_currency != "USD":
            # Get rates with the from_currency as base
            new_rates, _ = get_exchange_rates(from_currency)
            if new_rates:
                converted_amount = amount * new_rates[to_currency]
            else:
                st.error("Failed to convert with selected base currency")
                converted_amount = None
        else:
            # Direct conversion from USD
            converted_amount = amount * rates[to_currency]
        
        # Display result
        if converted_amount is not None:
            # Calculate exchange rate
            exchange_rate = rates[to_currency] / rates[from_currency] if from_currency != "USD" else rates[to_currency]
            
            # Get full currency names
            from_currency_name = currency_names[from_currency]
            to_currency_name = currency_names[to_currency]
            
            # Display in a highlighted box
            st.markdown(f"""
            <div style="background-color: #2A2A2A; padding: 20px; border-radius: 10px; border: 2px solid #FFD700; margin-top: 20px;">
                <h3 style="color: #FFD700; margin-bottom: 10px;">Conversion Result</h3>
                <p style="font-size: 24px; font-weight: bold; color: #FFD700;">
                    {amount:.2f} {from_currency} ({from_currency_name}) = {converted_amount:.2f} {to_currency} ({to_currency_name})
                </p>
                <p style="color: #FFD700;">
                    Exchange Rate: 1 {from_currency} = {exchange_rate:.6f} {to_currency}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Display last updated time
    st.markdown(f"""
    <div style="margin-top: 30px; font-size: 12px; color: #888888;">
        Last updated: {last_updated}
    </div>
    """, unsafe_allow_html=True)
    
    # Add information about the app
    with st.expander("About this app"):
        st.markdown("""
        This currency converter uses real-time exchange rates from the ExchangeRate-API.
        
        Features:
        - Convert between major world currencies
        - Real-time exchange rates
        - Full currency names displayed in parentheses
        - Simple and intuitive interface with black and yellow theme
        
        Note: This app only includes currencies with known full names to ensure accuracy.
        """)
else:
    st.error("Unable to load exchange rates. Please try again later.")

# Footer
st.markdown("""
<div style="position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; background-color: #121212; border-top: 1px solid #FFD700;">
    <p style="color: #FFD700; margin: 0;">Made by Mussawir Sohail</p>
</div>
""", unsafe_allow_html=True)

# Add a sample of popular currencies in the sidebar
st.sidebar.header("Popular Currencies")
if rates:
    sample_currencies = {
        "USD": "US Dollar",
        "EUR": "Euro",
        "GBP": "British Pound",
        "JPY": "Japanese Yen",
        "CAD": "Canadian Dollar",
        "AUD": "Australian Dollar",
        "CNY": "Chinese Yuan",
        "INR": "Indian Rupee",
        "BTC": "Bitcoin"
    }
    
    for code, name in sample_currencies.items():
        if code in rates and code in currency_names:
            st.sidebar.markdown(f"**{code}**: {name}")

print("Currency Converter app is running!")