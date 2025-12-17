import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from statistics import SPRT
from dotenv import load_dotenv
import os


def main():
    st.set_page_config(page_title="A/B Test Dashboard", layout="wide")

    st.title("Sequential A/B Test Dashboard")
    st.markdown("**Stop peeking at your A/B tests the wrong way!**")

    with st.sidebar:
        st.header("⚙️ Test Parameters")
        alpha = st.slider("Significance Level (α)", 0.01, .90, 0.05, 0.01)
        power = st.slider("Statistical Power (1-β)", 0.70, 0.95, 0.80, 0.05)
        mde = st.slider("Minimum Detectable Effect (%)", 1.0, 10.0, 2.0, 0.5)

        st.markdown("---")
        st.header("💰 Business Context")
        avg_order_value = st.number_input("Average Order Value ($)", value=45.0, step=1.0)
        monthly_visitors = st.number_input("Monthly Visitors", value=50000, step=1000)

    load_dotenv()
    file_path = os.getenv('DATA_PATH')

    user_data = load_and_process_data(file_path)

    st.subheader("Data Loaded Successfully!")
    st.write(f"Total Users: {len(user_data):,}")
    st.write(f"Converted Users: {user_data['converted'].sum():,}")
    st.write(f"Overall Conversion Rate: {user_data['converted'].mean():.2%}")
    st.write(f"Date Range: {user_data['first_date'].min()} to {user_data['first_date'].max()}")

    group_a, group_b = create_ab_split(user_data, group_size=30000)

    #Force artificial win to see Business Impact
    if st.sidebar.checkbox("🧪 Simulate Artificial Lift (Force Win To See Business Impact)"):
        # Create a copy to avoid SettingWithCopy warnings
        group_b = group_b.copy()
        
        np.random.seed(42)
        group_b['converted'] = np.random.binomial(1, 0.15, len(group_b))
        
        st.sidebar.warning("⚠️ Artificial lift enabled! Group B is now ~15%.")

    st.markdown("---")
    st.subheader("🔀 A/B Test Groups")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Group A**")
        st.write(f"Users: {len(group_a):,}")
        st.write(f"Conversions: {group_a['converted'].sum():,}")
        st.write(f"Conversion Rate: {group_a['converted'].mean():.2%}")

    with col2:
        st.write("**Group B**")
        st.write(f"Users: {len(group_b):,}")
        st.write(f"Conversions: {group_b['converted'].sum():,}")
        st.write(f"Conversion Rate: {group_b['converted'].mean():.2%}")

    beta = 1 - power
    sprt = SPRT(alpha = alpha, beta = beta,  mde = mde/100)

    st.markdown("---")
    st.subheader("📈 Sequential SPRT Analysis")
    sprt_results = calculate_sequential_sprt(group_a, group_b, sprt, step_size=100)

    st.write(f"Total steps analyzed: {len(sprt_results)}")
    st.write("Sample of SPRT results:")
    st.dataframe(sprt_results.head(10))

    fig = plot_sprt_chart(sprt_results, sprt)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("🎯 Test Decision")

    latest_decision = sprt_results.iloc[-1]['decision']
    latest_llr = sprt_results.iloc[-1]['llr']

    if latest_decision == "STOP_B_WINS":
        st.success("✅ **STOP THE TEST - B is the Winner!**")
        st.write("The test has crossed the upper boundary. Variant B has a statistically significant improvement.")

        st.markdown("### 💸 Revenue Impact Analysis")
        
        conv_rate_a = group_a['converted'].mean()
        conv_rate_b = group_b['converted'].mean()
        
        monthly_gain, annual_gain = calculate_business_impact(
            conv_rate_a, 
            conv_rate_b, 
            monthly_visitors, 
            avg_order_value
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Conversion Lift", f"+{(conv_rate_b - conv_rate_a):.2%}")
        with col2:
            st.metric("Proj. Monthly Revenue", f"+${monthly_gain:,.2f}")
        with col3:
            st.metric("Proj. Annual Revenue", f"+${annual_gain:,.2f}")
            
        st.info(f"**Business Insight:** By stopping this test at step {len(sprt_results)} (instead of waiting for a fixed sample size), you can deploy Variant B immediately and capture an extra **${(monthly_gain/30) * 10:,.0f}** in revenue over the next 10 days.")

    elif latest_decision == "STOP_NO_EFFECT":
        st.info("⏹️ **STOP THE TEST - No Significant Effect**")
        st.write("The test has crossed the lower boundary. There is no significant difference between A and B.")
    else:
        st.warning("⏳ **CONTINUE TESTING**")
        st.write("Not enough evidence yet. Keep collecting data.")
        st.write(f"Current LLR: {latest_llr:.4f}")
        st.write(f"Upper boundary: {sprt.upper_boundary:.4f}")
        st.write(f"Lower boundary: {sprt.lower_boundary:.4f}")

    st.markdown("---")
    st.subheader("💾 Export Results")

    col1, col2 = st.columns(2)

    with col1:
        # Download SPRT results as CSV
        csv = sprt_results.to_csv(index=False)
        st.download_button(
            label="📥 Download SPRT Data (CSV)",
            data=csv,
            file_name="sprt_results.csv",
            mime="text/csv"
        )

    with col2:
        # Download summary report
        summary = f"""Sequential A/B Test Summary Report

Test Parameters:
- Significance Level (α): {alpha}
- Statistical Power: {power}
- Minimum Detectable Effect: {mde}%

Group Statistics:
- Group A: {len(group_a):,} users, {group_a['converted'].sum()} conversions ({group_a['converted'].mean():.2%})
- Group B: {len(group_b):,} users, {group_b['converted'].sum()} conversions ({group_b['converted'].mean():.2%})

Test Results:
- Total Steps: {len(sprt_results)}
- Final Decision: {latest_decision}
- Final LLR: {latest_llr:.4f}
- Upper Boundary: {sprt.upper_boundary:.4f}
- Lower Boundary: {sprt.lower_boundary:.4f}

Recommendation: {
    "Stop testing - B is significantly better than A" if latest_decision == "STOP_B_WINS" else
    "Stop testing - No significant difference detected" if latest_decision == "STOP_NO_EFFECT" else
    "Continue collecting data"
}
"""

        st.download_button(
            label="📄 Download Summary Report (TXT)",
            data=summary,
            file_name="ab_test_summary.txt",
            mime="text/plain"
        )

    


def load_and_process_data(file_path, conversion_event='purchase'):
    """
    Load CSV and convert to user-level conversions
      
    Args:
        file_path: Path to the CSV file
        conversion_event: Event name that counts as conversion
          
    Returns:
        DataFrame with columns: user_pseudo_id, converted, first_date
    """
    load_dotenv()

    df = pd.read_csv(file_path)

    #Date/Time
    df['event_timestamp'] = pd.to_datetime(df['event_timestamp'], unit='us')
    df['date'] = df['event_timestamp'].dt.date  

    #Determining if user has purchased something
    user_conversions = df.groupby('user_pseudo_id').agg({
        'event_name': lambda x: 1 if conversion_event in x.values else 0,
        'date': 'min'  
    }).rename(columns={'event_name': 'converted', 'date': 'first_date'})

    user_conversions.index = user_conversions.index.astype(int)

    return user_conversions


def create_ab_split(user_data, group_size=30000, random_seed=42):
    """
    Randomly split users into groups A and B

    Args:
        user_data: DataFrame with user conversion data
        group_size: Number of users per group
        random_seed: Random seed for reproducibility

    Returns: 
        tuple: (group_a, group_b) DataFrames
    """
    np.random.seed(random_seed)
    shuffled_data = user_data.sample(frac=1).reset_index()

    group_a = shuffled_data.iloc[:group_size]
    group_b = shuffled_data.iloc[group_size : group_size * 2]

    return group_a, group_b

def calculate_sequential_sprt(group_a, group_b, sprt_instance, step_size = 100):
    """
    Calculate SPRT statistics over time (sequential analysis)
    
    Args:
        group_a: DataFrame for group_a
        group_b: DataFrame for group_b
        sprt_instance: SPRT object with alpha, beta, mde
    
    Returns:
        DataFrame with columns: step, users_a, users_b, conversions_a, conversions_b, llr, decision
    """
    results = []
    max_steps = len(group_a) // step_size

    sorted_group_a = group_a.sort_values('first_date')
    sorted_group_b = group_b.sort_values('first_date')

    for i in range(1, max_steps + 1):
        n = i * step_size
        a_cumulative = sorted_group_a['converted'].iloc[:n].sum()
        b_cumulative = sorted_group_b['converted'].iloc[:n].sum()

        llr = sprt_instance.calculate_log_likelihood_ratio(a_cumulative, n, b_cumulative, n)
        decision = sprt_instance.get_decision(llr)

        dict = {
            'step' : i,
            'users_a' : n,
            'users_b' : n, 
            'conversions_a' : a_cumulative, 
            'conversions_b' : b_cumulative, 
            'llr' : llr, 
            'decision' : decision
        }

        results.append(dict)
    return pd.DataFrame(results)


def plot_sprt_chart(sprt_results, sprt):
    """
    Create Plotly chart showing SPRT progress

    Args:
        sprt_results: DataFrame from calculate_sequential_sprt
        sprt: SPRT instance with boundaries
    
    Returns:
        Plotly figure object
    """
    fig = go.Figure()

    # LLR Line
    fig.add_trace(go.Scatter(
        x = sprt_results['step'], 
        y = sprt_results['llr'], 
        mode = 'lines', 
        name = 'Log Likelihood Ratio', 
        line = dict(color = 'blue', width = 2)
    ))

    # Upper Boundary (B wins if crossed)
    fig.add_trace(go.Scatter(
        x = sprt_results['step'], 
        y = [sprt.upper_boundary] * len(sprt_results),
        mode = 'lines', 
        name = 'Upper Boundary', 
        line = dict(color = 'red', width = 2)
    ))

    #Lower Boundary (No effect if crossed)
    fig.add_trace(go.Scatter(
        x = sprt_results['step'], 
        y = [sprt.lower_boundary] * len(sprt_results), 
        mode = 'lines', 
        name = 'Lower Bound', 
        line = dict(color = 'yellow', width = 2)
    ))

    fig.update_layout(
        title='Sequential Probability Ratio Test',
        xaxis_title='Step (every 100 users)',
        yaxis_title='Log Likelihood Ratio',
        hovermode='x unified'
    )

    return fig


def calculate_business_impact(conversion_rate_a, conversion_rate_b, visitors, aov):
    """
    Calculate the potential revenue impact of the test result

    Args:
        conversion_rate_a (float): Conversion rate of the control group (0.0 to 1.0).
        conversion_rate_b (float): Conversion rate of the test group (0.0 to 1.0).
        visitors (int): Number of monthly visitors to the tested page/flow.
        aov (float): Average Order Value in dollars.

    Returns:
        Tuple: (monthly gain, annual gain) float
    """
    lift = conversion_rate_b - conversion_rate_a
    
    # If B is worse or equal, no gain
    if lift <= 0:
        return 0.0, 0.0
        
    incremental_conversions = visitors * lift
    monthly_gain = incremental_conversions * aov
    annual_gain = monthly_gain * 12
    
    return monthly_gain, annual_gain

if __name__ == "__main__":
    main()

