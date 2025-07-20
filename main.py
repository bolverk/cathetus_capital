import streamlit as st
#import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from diversification_suggestion import diversification_suggestion

df = pd.read_csv('unified.csv')
supported_tickers = [t.lower() for t in df.columns.tolist()]

st.set_page_config(page_title="Portfolio Diversifier", layout="centered")
st.title("📈 Portfolio Diversifier")

st.markdown("Select your portfolio tickers and adjust their weights (in %).")

# Select tickers using a searchable multiselect dropdown
selected_tickers = st.multiselect(
    "Choose up to 10 tickers",
    options=supported_tickers,
    default=["spy", "bnd"],
    max_selections=10,
    help="Start typing to search for tickers."
)

weights = []
if selected_tickers:
    st.markdown("### Adjust Weights")
    total_weight = 0
    weight_inputs = []
    for ticker in selected_tickers:
        weight = st.slider(
            f"Weight for {ticker}",
            min_value=0,
            max_value=100,
            value=int(100 // len(selected_tickers)),
            step=1,
            key=f"weight_{ticker}"
        )
        weight_inputs.append(weight)
        total_weight += weight

    # Normalize weights to sum to 100%
    if total_weight == 0:
        st.warning("Please assign at least some weight to your tickers.")
        weights = [0 for _ in selected_tickers]
    else:
        weights = [w * 100 / total_weight for w in weight_inputs]

    st.markdown(
        "#### Normalized Weights\n" +
        "\n".join([f"- **{ticker}**: {w:.1f}%" for ticker, w in zip(selected_tickers, weights)])
    )

# Validate weights
if selected_tickers and abs(sum(weights) - 100.0) > 0.01:
    st.warning("⚠️ Portfolio weights should sum to 100%. Current total: {:.1f}%".format(sum(weights)))

if selected_tickers and len(weights) == len(selected_tickers):
    with st.spinner("Fetching data and analyzing correlations..."):

        # Use diversification_suggestion to get suggestions
        portfolio_dict = dict(zip([t.lower() for t in selected_tickers], [w/100 for w in weights]))
        suggestions = diversification_suggestion(portfolio_dict, n_suggestions=5)
        bests = list(suggestions) if len(suggestions) > 0 else []

        st.subheader("🧠 Suggested Diversifiers")
        if bests:
            for best in bests:
                st.markdown(f"- **{best.upper()}**")
            # Plot historic price history for all suggestions using Plotly
            st.subheader("📊 Historic Correlation of Relative Daily Price Changes")
            price_df = df[[b for b in bests if b in df.columns]].copy()
            price_df['ref'] = sum((df[k].values * v for k, v in portfolio_dict.items()))
            if not price_df.empty:
                fig = go.Figure()
                for col in price_df.columns:
                    if col == 'ref':
                        continue
                    fig.add_trace(go.Scatter(
                        x=price_df['ref'],
                        y=price_df[col],
                        mode='markers',
                        name=col.upper()
                    ))
                fig.update_layout(
                    xaxis_title="Portfolio relative daily price diff",
                    yaxis_title="Suggestion relative daily price diff",
                    legend_title="Ticker",
                    template="plotly_white"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No price data available for suggestions.")
        else:
            st.warning("No suitable diversifier found.")
