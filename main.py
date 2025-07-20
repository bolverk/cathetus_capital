import streamlit as st
#import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from diversification_suggestion import diversification_suggestion

st.set_page_config(page_title="Portfolio Diversifier", layout="centered")
st.title("📈 Portfolio Diversifier")

st.markdown("Enter your portfolio tickers and weights (in %).")

# Input tickers and weights
portfolio_input = st.text_area("Enter tickers and weights (e.g. spy:80, bnd:20)", value="spy:80, bnd:20")
tickers_weights = [x.strip() for x in portfolio_input.split(",") if ":" in x]

# Parse input
tickers = []
weights = []
for item in tickers_weights:
    try:
        ticker, weight = item.split(":")
        tickers.append(ticker.strip().upper())
        weights.append(float(weight.strip()) / 100)  # convert % to decimal
    except:
        st.error(f"Couldn't parse: {item}")

# Validate weights
if abs(sum(weights) - 1.0) > 0.01:
    st.warning("⚠️ Portfolio weights should sum to 100%. Current total: {:.1f}%".format(sum(weights)*100))

# Diversification candidates
diversifiers = {
    "GLD": "Gold ETF",
    "TLT": "Long-Term Bonds",
    "VNQ": "Real Estate",
    "BTC-USD": "Bitcoin",
    "XLE": "Energy Sector",
    "VEA": "Intl. Developed Markets"
}

all_tickers = tickers + list(diversifiers.keys())

if tickers and len(weights) == len(tickers):
    with st.spinner("Fetching data and analyzing correlations..."):

        # Use diversification_suggestion to get suggestions
        portfolio_dict = dict(zip([t.lower() for t in tickers], weights))
        suggestions = diversification_suggestion(portfolio_dict, n_suggestions=5)
        bests = list(suggestions) if len(suggestions) > 0 else []

        st.subheader("🧠 Suggested Diversifiers")
        if bests:
            for best in bests:
                name = diversifiers.get(best.upper(), best)
                st.markdown(f"- **{best.upper()}**")
        else:
            st.warning("No suitable diversifier found.")
            st.warning("No suitable diversifier found.")
