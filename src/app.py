import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from statistics import SPRT


def main():
    st.set_page_config(page_title="A/B Test Dashboard", layout="wide")

    st.title("🧪 Sequential A/B Test Dashboard")
    st.markdown("**Stop peeking at your A/B tests the wrong way!**")

    with st.sidebar:
        st.header("⚙️ Test Parameters")
        alpha = st.slider("Significance Level (α)", 0.01, 0.10, 0.05, 0.01)
        power = st.slider("Statistical Power (1-β)", 0.70, 0.95, 0.80, 0.05)
        mde = st.slider("Minimum Detectable Effect (%)", 1.0, 10.0, 2.0, 0.5)

        st.markdown("---")
        st.info("Upload your A/B test data to get started!")

    st.info("📊 Dashboard will be implemented in Phase 4")


if __name__ == "__main__":
    main()
