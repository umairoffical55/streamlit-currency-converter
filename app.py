import streamlit as st
import requests

# Page Config
st.set_page_config(
    page_title="Currency Converter",
    page_icon="💱",
    layout="centered"
)

# Title
st.title("💱 Currency Converter")
st.write("Convert currencies using live exchange rates.")

# Fetch Exchange Rates
@st.cache_data(ttl=3600)
def get_rates():
    url = "https://open.er-api.com/v6/latest/USD"
    response = requests.get(url)
    data = response.json()

    if data["result"] == "success":
        return data["rates"]
    else:
        return None

rates = get_rates()

if rates:

    currencies = sorted(list(rates.keys()))

    col1, col2 = st.columns(2)

    with col1:
        from_currency = st.selectbox(
            "From Currency",
            currencies,
            index=currencies.index("USD")
        )

    with col2:
        to_currency = st.selectbox(
            "To Currency",
            currencies,
            index=currencies.index("PKR")
        )

    amount = st.number_input(
        "Amount",
        min_value=0.0,
        value=1.0,
        step=1.0
    )

    if st.button("Convert", use_container_width=True):

        usd_amount = amount / rates[from_currency]
        converted_amount = usd_amount * rates[to_currency]

        st.success(
            f"{amount:,.2f} {from_currency} = "
            f"{converted_amount:,.2f} {to_currency}"
        )

        exchange_rate = rates[to_currency] / rates[from_currency]

        st.info(
            f"1 {from_currency} = "
            f"{exchange_rate:.6f} {to_currency}"
        )

else:
    st.error("Unable to fetch exchange rates. Please try again later.")

st.markdown("---")
st.caption("Powered by ExchangeRate API")
