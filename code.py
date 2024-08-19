import yfinance as yf
import streamlit as st

# Function to fetch net profit data and calculate minimum CSR budget
def get_minimum_csr_budget(ticker):
    try:
        stock = yf.Ticker(ticker)
        # Fetch financial data
        income_statement = stock.financials
        
        # Ensure we have net profit data available
        if 'Net Income' not in income_statement.index:
            st.error("Net Income data is not available.")
            return None

        # Get the most recent 3 years of Net Income data
        net_income = income_statement.loc['Net Income']
        recent_years = net_income.head(3)  # Get the most recent 3 years of data
        
        # Calculate the average net profit
        average_net_profit = recent_years.mean()
        
        # Calculate 2% of the average net profit as minimum CSR budget
        min_csr_budget = 0.02 * average_net_profit

        return average_net_profit, min_csr_budget
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None, None

# Streamlit UI
st.title('CSR Budget Calculator')

ticker = st.text_input('Enter the company ticker:', '')

if ticker:
    average_net_profit, min_csr_budget = get_minimum_csr_budget(ticker)
    
    if average_net_profit is not None:
        st.write(f"Average Net Profit for the last 3 years for {ticker}: ${average_net_profit:,.2f}")
        st.write(f"Minimum CSR Budget (2% of Average Net Profit): ${min_csr_budget:,.2f}")
    else:
        st.write(f"No data available for ticker: {ticker}")
