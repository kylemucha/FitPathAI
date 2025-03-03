import streamlit as st
import pandas as pd
from PIL import Image
import base64
import os

# First, let's verify our pages directory exists and contains our file
pages_dir = os.path.join(os.path.dirname(__file__), "pages")
if not os.path.exists(pages_dir):
    os.makedirs(pages_dir)

# Page configuration
st.set_page_config(
    page_title="FitPathAI - Your Personal AI Fitness Coach",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: white;
    }
    .container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
        text-align: center;
    }
    .welcome {
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
        color: #333333;
        text-align: center;
    }
    .title {
        font-size: 2rem !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
        color: #333333;
        text-align: center;
    }
    .subtitle {
        font-size: 1.5rem !important;
        color: #424242;
        margin-bottom: 2rem !important;
        text-align: center;
        max-width: 800px;
        margin-left: auto; 
        margin-right: auto;
    }
    .feature-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f8f9fa;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .cta-button {
        background-color: #1E88E5;
        color: white;
        padding: 0.8rem 2rem;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin: 1rem 0;
    }
    .cta-button:hover {
        background-color: #1565C0;
    }
    [data-testid="collapsedControl"] {
        display: block;
        color: #333333 !important;
    }
    button[kind="header"] {
        color: #333333 !important;
    }
    .st-emotion-cache-7ym5gk {
        color: #333333 !important;
    }
    .st-emotion-cache-1egp7i3 {
        color: #333333 !important;
    }
    #MainMenu {
        display: none;
    }
    .css-1rs6os {visibility: hidden;}
    .css-17ziqus {visibility: hidden;}
    section[data-testid="stSidebar"] {
        display: block;
    }
    header {
        display: block;
    }
    [data-testid="stAppViewContainer"] {
        background-color: white;
    }
    [data-testid="stHeader"] {
        background-color: white;
    }
    .stApp {
        background-color: white;
    }
    /* Button hover effects */
    button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Hero Section
st.markdown('<div class="container">', unsafe_allow_html=True)
st.markdown("""
    <div style="
        width: 100%;
        padding: 2rem;
        text-align: center;
        margin: 0 auto;
    ">
        <h1 style="
            margin-bottom: 2rem !important;
            line-height: 1.2 !important;
            padding: 0 !important;
        ">
            <span style="
                color: #333333;
                font-size: 12vh !important;
                font-weight: 900 !important;
            ">Welcome to </span>
            <span style="
                background: linear-gradient(45deg, #0099FF, #00E5FF, #FFB74D, #FF9800);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                display: inline-block;
                font-size: 12vh !important;
                font-weight: 900 !important;
            ">FitPathAI</span>
        </h1>
    </div>
""", unsafe_allow_html=True)
st.markdown('<div class="title" style="font-size: 1.8rem !important; color: #333333;">Transform Your Fitness Journey with AI</div>', unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; padding: 1rem 0; color: #444444;">
        FitPathAI combines cutting-edge artificial intelligence with personalized fitness coaching to help you achieve your health goals faster and smarter.
    </div>
""", unsafe_allow_html=True)
st.markdown("""
    <a href="/AI_Workout_Planner" target="_self" style="text-decoration: none;">
        <button style="
            background: linear-gradient(45deg, #0099FF, #00E5FF, #FFB74D, #FF9800);
            color: black;
            padding: 10px 24px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin: 1rem auto;
            display: block;
            font-weight: bold;
            transition: all 0.3s ease;
            ">
            Try our AI Workout Planner!
        </button>
    </a>

    <a href="/AI_Meal_Planner" target="_self" style="text-decoration: none;">
        <button style="
            background: linear-gradient(45deg, #0099FF, #00E5FF, #FFB74D, #FF9800);
            color: black;
            padding: 10px 24px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin: 1rem auto;
            display: block;
            font-weight: bold;
            transition: all 0.3s ease;
            ">
            Try our AI Meal Planner!
        </button>
    </a>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Divider with lighter gray
st.markdown("""
    <hr style="
        height: 1px;
        border: none;
        background-color: #CCCCCC;
        margin: 2rem auto;
    ">
""", unsafe_allow_html=True)

# Call to Action Section
st.markdown("<h2 style='text-align: center; pointer-events: none; color: #333333;'>Ready to Transform Your Fitness Journey?</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #333333;'>Try FitPathAI today and experience the future of personal fitness coaching!</p>", unsafe_allow_html=True)