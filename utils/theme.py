
import streamlit as st


def apply_theme():
    st.markdown("""
    <style>
    /* Main page */
    .stApp {
        background-color: #0b1120;
        color: #f1f5f9;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    /* Keep the sidebar consistent on every page */
   
section[data-testid="stSidebar"] .sidebar-brand {
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
}

section[data-testid="stSidebar"] .sidebar-brand-title {
    font-size: 19px;
    line-height: 1.35;
    white-space: normal;
}


    /* Navigation fills the available sidebar width */
    [data-testid="stSidebarNav"] {
        padding: 0.5rem 0.65rem 1rem 0.65rem;
    }

    [data-testid="stSidebarNav"] ul {
        width: 100%;
    }

    [data-testid="stSidebarNav"] a {
        width: 100%;
        min-height: 42px;
        border-radius: 9px;
        margin-bottom: 5px;
        padding: 0.65rem 0.8rem;
        color: #e2e8f0 !important;
        background-color: transparent;
        box-sizing: border-box;
    }

    [data-testid="stSidebarNav"] a:hover {
        background-color: #243750 !important;
        color: #ffffff !important;
    }

    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: #174e46 !important;
        color: #ffffff !important;
        border-left: 3px solid #5eead4;
        font-weight: 700;
    }

    /* Shared sidebar branding */
    
.sidebar-brand {
    width: 100%;
    box-sizing: border-box;
    display: block;
    padding: 15px 12px;
    margin: 8px 0 16px 0;
    background: linear-gradient(135deg, #123b35, #172554);
    border: 1px solid #28564e;
    border-radius: 12px;
    overflow-wrap: anywhere;
    }


    /* Make normal text readable */
    .stApp p,
    .stApp label,
    .stApp li {
        color: #e2e8f0;
    }

    h1, h2, h3, h4 {
        color: #f8fafc !important;
    }

    /* Input fields */
    .stTextInput input,
    .stNumberInput input,
    .stDateInput input,
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #17243a;
        color: #ffffff;
        border-color: #42536c;
    }

    /* Buttons */
    .stButton button,
    .stFormSubmitButton button {
        border-radius: 9px;
        font-weight: 700;
    }

    /* Tables */
    [data-testid="stDataFrame"] {
        border: 1px solid #293b55;
        border-radius: 12px;
    }

    /* Links */
    a {
        color: #5eead4;
    }

    </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-title">🏏 Cricbuzz LiveStats</div>
        <div class="sidebar-brand-caption">CRICKET ANALYTICS</div>
    </div>
    """, unsafe_allow_html=True)
