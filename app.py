import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import datetime
import random
import processor
import plotly.io as pio

# Configure default Plotly template for professional corporate look
# Removed to allow Streamlit native theme formatting
pass


# === PAGE CONFIGURATION ===
st.set_page_config(
    page_title="WUZZUF Market Pulse",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# === CORPORATE THEME & SIDEBAR FIX ===
# === CORPORATE THEME & SIDEBAR FIX ===
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* GLOBAL APP FONT */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* CRITICAL: SIDEBAR TOGGLE BUTTON VISIBILITY */
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        background-color: var(--secondary-background-color) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--secondary-background-color);
        border-radius: 6px !important;
        top: 1rem !important;
        left: 1rem !important;
        z-index: 1000000 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    [data-testid="collapsedControl"]:hover {
        background-color: var(--background-color) !important;
        color: var(--primary-color) !important;
    }

    /* HEADER STYLE */
    .header-container {
        background: var(--background-color);
        padding: 2rem 3rem;
        border-bottom: 1px solid var(--secondary-background-color);
        margin: -3rem -5rem 2rem -5rem;
        display: flex;
        align-items: center;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    
    .logo-text {
        color: var(--text-color);
        font-size: 1.8rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: var(--background-color);
        padding: 10px 10px;
        border-radius: 12px;
        border: 1px solid var(--secondary-background-color);
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 8px;
        background-color: transparent;
        color: var(--text-color);
        font-weight: 600;
        border: none;
        padding: 0px 20px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: var(--secondary-background-color);
        color: var(--primary-color);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--primary-color);
        color: white; /* Keep white for contrast on primary color */
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* METRIC CARDS */
    div[data-testid="metric-container"] {
        background-color: var(--secondary-background-color) !important;
        border: 1px solid var(--secondary-background-color);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    
    div[data-testid="stMetricValue"] {
        color: var(--text-color) !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }
    
    div[data-testid="stMetricLabel"] {
        color: var(--text-color) !important;
        opacity: 0.8;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
    }

    /* HEADERS */
    h1, h2, h3 {
        color: var(--text-color) !important;
        letter-spacing: -0.5px;
    }

    /* CHARTS CONTAINER */
    .chart-container {
        background: var(--secondary-background-color);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid var(--secondary-background-color);
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* PERIOD INFO - High Contrast Badge */
    .period-badge {
        background-color: #0f172a; /* Keep dark navy for brand identity */
        color: white;
        padding: 8px 20px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1rem;
        border: 1px solid #1e293b;
        display: inline-block;
        float: right;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Radios/Selectbox Text */
    .stRadio label, .stSelectbox label {
        color: var(--text-color) !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    
    .stRadio div[role="radiogroup"] label p {
        color: var(--text-color) !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
</style>

<div class="header-container">
    <div class="logo-text">WUZZUF <span style="color: #3b82f6;">Market Pulse</span></div>
</div>
""", unsafe_allow_html=True)

# === DATA ENGINE ===
def classify_hiring_speed(days):
    if days < 10: return "Urgent Hiring (<10 Days)"
    elif days <= 30: return "Moderate Hiring (10-30 Days)"
    return "Slow Hiring (>30 Days)"

@st.cache_data(ttl=3600, show_spinner=False)
def generate_realistic_data():
    """Generate data for Oct 2025 - Jan 2026 period"""
    
    roles = [
        "Data Analyst", "Business Analyst", "Cost Analyst", "Credit Analyst",
        "Commercial Specialist (Junior Data Analyst)", "Ads Sales Quality Analyst (QA)",
        "Financial Analyst", "Business Analyst - Customer Solutions",
        "Central Operations Senior Analyst", "Tax Accountant", "Full Stack Developer",
        "Machine Learning Engineer", "DevOps Engineer", "Product Manager"
    ]
    
# === DATA ENGINE ===
@st.cache_data(ttl=3600, show_spinner=False)
def load_real_data():
    """
    Triggers the ETL pipeline (processor.py) to ensure data is clean,
    then loads the clean CSV.
    """
    # 1. Trigger Processing (Ensure Clean CSV is synced with Raw CSV)
    # This runs every time the cache is invalidated or on first run
    df = processor.process_data()
    
    # Alternatively, we could read the file if processor returns nothing, 
    # but processor.process_data() returns the DF directly.
    if df.empty:
         # Fallback try reading file if it exists
         try:
             df = pd.read_csv("data/wuzzuf_jobs_clean.csv")
         except:
             return pd.DataFrame()

    return df

# === MAIN APP ===
def main():
    df = load_real_data()
    
    if df.empty:
        st.error("⚠️ No data available. Please run the scraper or wait for the daily refresh to complete.")
        st.info("Debugging info: `data/wuzzuf_jobs_raw.csv` might be empty or `processor.py` filtering removed all rows.")
        return

    # Get Data Last Modified Date
    import os
    import time
    try:
        mod_time = os.path.getmtime("data/wuzzuf_jobs_raw.csv")
        last_updated = time.strftime('%d %b %Y', time.localtime(mod_time))
        # Since we don't have a "range" in the data, we show the snapshot date
        period_str = f"Data Snapshot: {last_updated}" 
    except:
        period_str = "Data Source: Unknown"

    # === SIDEBAR ===
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0; border-bottom: 2px solid rgba(255,255,255,0.1);'>
            <h3 style='color: var(--text-color); margin: 0; font-style: italic;'>Welcome Hazem Tarek!</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        selected_nav = option_menu(
            menu_title=None,
            options=["Dashboard", "Details"],
            icons=["speedometer2", "table"],
            default_index=0,
            styles={
                "container": {"padding": "0", "background": "transparent"},
                "nav-link": {"font-weight": "500", "font-size": "1rem"},
                "nav-link-selected": {"background": "#3b82f6", "color": "white", "font-weight": "600", "border-radius": "8px"}
            }
        )
        
        st.info(f"ℹ️ **Data Updated**:\n{last_updated}\n\nRun `scraper.py` to refresh.")
    
    # === MAIN CONTENT ===
    
    if selected_nav == "Dashboard":
        st.markdown(f"<div class='period-badge'>📅 {period_str}</div>", unsafe_allow_html=True)
        
        # KPIs
        top_skill = "N/A"
        if not df.empty:
            all_skills = []
            for skills_str in df['Skills']:
                 all_skills.extend([s.strip() for s in str(skills_str).split(',') if s.strip()])
            if all_skills:
                top_skill = pd.Series(all_skills).mode()[0]

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Jobs", len(df))
        k2.metric("Top City", df['City'].mode()[0] if not df.empty else "N/A")
        k3.metric("Top Company", df['Company Name'].mode()[0] if not df.empty else "N/A")
        k4.metric("Top Skill", top_skill)
        
        st.markdown("---")
        
        # TABS
        tab1, tab2, tab3 = st.tabs(["Overview", "Role Analysis", "Experience & details"])
        
        # === TAB 1: OVERVIEW ===
        with tab1:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("Jobs by Job Type")
                type_counts = df['Job Type'].value_counts().reset_index()
                type_counts.columns = ['Type', 'Count']
                
                fig_type = px.pie(type_counts, values='Count', names='Type', hole=0.5,
                                  color_discrete_sequence=px.colors.sequential.Blues_r)
                
                fig_type.update_traces(textposition='inside', textinfo='percent+label', 
                                     textfont=dict(size=14, weight='bold', color='white'))
                fig_type.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#f8fafc', size=12),
                    showlegend=False,
                    margin=dict(t=30, b=10, l=10, r=10)
                )
                st.plotly_chart(fig_type, use_container_width=True)
            
            with col2:
                st.subheader("Job Distribution by City")
                city_counts = df['City'].value_counts().head(7).reset_index()
                city_counts.columns = ['City', 'Count']
                
                fig_city = px.bar(city_counts, x='Count', y='City', orientation='h', text_auto=True)
                fig_city.update_traces(
                    marker=dict(color='#3b82f6', line=dict(color='#1e40af', width=1)),
                    textposition='outside',
                    textfont=dict(color='#f8fafc', weight='bold')
                )
                fig_city.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#f8fafc'),
                    showlegend=False,
                    xaxis=dict(showgrid=True, gridcolor='#334155'),
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                st.plotly_chart(fig_city, use_container_width=True)
            
            st.subheader("Top Hiring Companies")
            comp_counts = df['Company Name'].value_counts().head(10).reset_index()
            comp_counts.columns = ['Company', 'Count']
            
            fig_comp = px.bar(comp_counts, x='Count', y='Company', orientation='h', text_auto=True,
                            color='Count', color_continuous_scale=['#93c5fd', '#1e40af'])
            fig_comp.update_traces(textposition='outside', textfont=dict(weight='bold', color='#f8fafc'))
            fig_comp.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f8fafc', size=12),
                showlegend=False,
                height=500,
                xaxis=dict(showgrid=True, gridcolor='#334155')
            )
            st.plotly_chart(fig_comp, use_container_width=True)

        # === TAB 2: ROLE ANALYSIS ===
        with tab2:
            st.subheader("Most In-Demand Job Titles")
            title_counts = df['Job Title'].value_counts().head(10).reset_index()
            title_counts.columns = ['Title', 'Count']
            
            fig_titles = px.bar(title_counts, x='Count', y='Title', orientation='h', text_auto=True,
                               color='Count', color_continuous_scale=['#bae6fd', '#0284c7'])
            fig_titles.update_traces(textposition='outside', textfont=dict(weight='bold', color='#f8fafc'))
            fig_titles.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f8fafc', size=12),
                height=500,
                showlegend=False,
                xaxis=dict(showgrid=True, gridcolor='#334155')
            )
            st.plotly_chart(fig_titles, use_container_width=True)
            
            st.subheader("Top Required Skills")
            # Parse skills string again for chart
            all_skills = []
            for skills_str in df['Skills']:
                 # Handle cases where scraped skills are clean or messy
                 parts = [s.strip() for s in str(skills_str).split(',') if s.strip()]
                 all_skills.extend(parts)
            
            if all_skills:
                skills_df = pd.Series(all_skills).value_counts().head(15).reset_index()
                skills_df.columns = ['Skill', 'Count']
                
                fig_skills = px.bar(skills_df, x='Count', y='Skill', orientation='h', text_auto=True)
                fig_skills.update_traces(
                    marker=dict(color='#0ea5e9'),
                    textposition='outside',
                    textfont=dict(weight='bold', size=12, color='#f8fafc')
                )
                fig_skills.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#f8fafc'),
                    height=600,
                    xaxis=dict(showgrid=True, gridcolor='#334155')
                )
                st.plotly_chart(fig_skills, use_container_width=True)
            else:
                st.info("No skills data available to analyze.")

        # === TAB 3: EXPERIENCE & DETAILS ===
        with tab3:
            c1, c2 = st.columns(2)
            
            with c1:
                st.subheader("Distribution by Career Level")
                if 'Level' in df.columns:
                    level_counts = df['Level'].value_counts().reset_index()
                    level_counts.columns = ['Level', 'Count']
                    
                    fig_level = px.bar(level_counts, x='Level', y='Count', text_auto=True,
                                      color_discrete_sequence=['#60a5fa'])
                    fig_level.update_traces(textposition='outside', textfont=dict(color='#f8fafc', weight='bold'))
                    fig_level.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#f8fafc'),
                        yaxis=dict(showgrid=True, gridcolor='#334155'),
                        xaxis=dict(tickangle=-45)
                    )
                    st.plotly_chart(fig_level, use_container_width=True)
            
            with c2:
                st.subheader("Years of Experience")
                if 'Years of Experience' in df.columns:
                    # Clean up experience text slightly for better grouping if needed, 
                    # but raw value counts often work for scraped categories
                    clean_exp = df['Years of Experience'].replace('nan', 'Unknown').fillna('Unknown')
                    exp_counts = clean_exp.value_counts().head(8).reset_index()
                    exp_counts.columns = ['Experience', 'Count']
                    
                    fig_exp = px.bar(exp_counts, x='Count', y='Experience', orientation='h', text_auto=True,
                                    color_discrete_sequence=['#818cf8'])
                    fig_exp.update_traces(textposition='outside', textfont=dict(color='#f8fafc', weight='bold'))
                    fig_exp.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#f8fafc'),
                        xaxis=dict(showgrid=True, gridcolor='#334155')
                    )
                    st.plotly_chart(fig_exp, use_container_width=True)

            st.markdown("### Raw Data Sample")
            st.dataframe(df.head(10), use_container_width=True)

    # === DETAILS PAGE ===
    elif selected_nav == "Details":
        st.subheader("Complete Job Listings")
        st.markdown(f"**Total Records:** {len(df)}")
        
        # Search box
        search_term = st.text_input("🔍 Search by Title, Company, or Skill", "")
        
        if search_term:
            mask = df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)
            df_display = df[mask]
        else:
            df_display = df
            
        st.dataframe(
            df_display,
            column_config={
                "Company Name": st.column_config.TextColumn("Company", width="medium"),
                "Job Title": st.column_config.TextColumn("Title", width="large"),
                "Skills": st.column_config.TextColumn("Skills", width="large"),
            },
            height=800,
            use_container_width=True,
            hide_index=True
        )

if __name__ == "__main__":
    main()

