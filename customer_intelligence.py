import streamlit as st
import pandas as pd
import plotly.express as px
import re

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Prism Experience Hub", layout="wide")
st.title("📊 PRISM ANALYTICS: Experience Intelligence Hub")
st.markdown("### Student Project: Analysis of Customer Feedback Trends")

# --- 2. DATA LOADING ---
try:
    # Loading your specific CSV file
    df_data = pd.read_csv('customer_reviews (1).csv')
    
    # --- 3. STUDENT-MADE ANALYSIS ENGINE ---
    # We use simple keyword matching to categorize the voice of the customer
    positive_list = ['great', 'excellent', 'love', 'fast', 'perfect', 'good', 'best', 'happy', 'amazing', 'nice']
    negative_list = ['late', 'crack', 'cheap', 'worst', 'broke', 'waste', 'bad', 'terrible', 'broken', 'slow']

    def get_user_status(text):
        text = str(text).lower()
        score = 0
        for word in positive_list:
            if word in text: score += 1
        for word in negative_list:
            if word in text: score -= 1
        
        if score > 0: return 'Satisfied'
        elif score < 0: return 'Dissatisfied'
        else: return 'Neutral'

    # Create the new status column
    df_data['Status'] = df_data['review'].apply(get_user_status)

    # --- 4. TOP KPI METRICS ---
    total_reviews = len(df_data)
    average_stars = df_data['rating'].mean()
    success_rate = (len(df_data[df_data['Status'] == 'Satisfied']) / total_reviews) * 100

    # High-impact metrics shown at the very top
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Reviews Analyzed", total_reviews)
    m2.metric("Average Star Rating", f"{average_stars:.1f} / 5")
    m3.metric("Customer Success Rate", f"{success_rate:.1f}%")

    st.divider()

    # --- 5. VISUAL CHARTS ---
    col_left, col_right = st.columns(2)

    with col_left:
        # Pie Chart for Overall Distribution
        fig_pie = px.pie(df_data, names='Status', title='Overall Market Mood Share',
                        color='Status', color_discrete_map={'Satisfied':'#27ae60', 'Dissatisfied':'#c0392b', 'Neutral':'#95a5a6'})
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        # Bar Chart for Product Performance
        product_perf = df_data.groupby('product')['rating'].mean().reset_index()
        fig_bar = px.bar(product_perf, x='product', y='rating', title='Average Rating by Product Category',
                        color='rating', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- 6. AGE DEMOGRAPHIC ANALYSIS ---
    st.subheader("Demographic Trends: How Age Impacts Feedback")
    fig_age = px.histogram(df_data, x='age', color='Status', barmode='group',
                          title="Feedback Volume by Age Group",
                          color_discrete_map={'Satisfied':'#27ae60', 'Dissatisfied':'#c0392b', 'Neutral':'#95a5a6'})
    st.plotly_chart(fig_age, use_container_width=True)

    # --- 7. KEYWORDS (REPLACING WORDCLOUD) ---
    st.subheader("💡 Experience Highlights")
    st.info("The AI engine prioritized these keywords for analysis:")
    
    k_col1, k_col2 = st.columns(2)
    with k_col1:
        st.success("**Top Satisfaction Drivers:** " + ", ".join(positive_list[:6]))
    with k_col2:
        st.error("**Top Pain Points Detected:** " + ", ".join(negative_list[:6]))

except Exception as e:
    st.error("Error: Please make sure 'customer_reviews (1).csv' is uploaded correctly to GitHub.")
    st.write(e)
