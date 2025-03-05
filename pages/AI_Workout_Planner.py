import streamlit as st
import pandas as pd
from gym_chatbot_new import GymChatbot
import gym_ml_model_new  # Add this import

# Page configuration
st.set_page_config(
    page_title="FitPathAI - Workout Planner",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed"  # This ensures sidebar starts collapsed
)

# Update CSS to match landing page and set all text colors
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: white;
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
    #MainMenu {
        display: none;
    }
    /* Make all text black by default */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: black !important;
    }
    /* Target input labels and questions */
    .css-qrbaxs {
        color: #333333 !important;
    }
    .css-1qg05tj {
        color: #333333 !important;
    }
    .css-81oif8 {
        color: #333333 !important;
    }
    .css-1x8cf1d {
        color: #333333 !important;
    }
    label.css-1p2iens {
        color: #333333 !important;
    }
    .css-1oyc9oj {
        color: #333333 !important;
    }
    /* Additional selectors for questions */
    div[data-baseweb="select"] label {
        color: #333333 !important;
    }
    .stNumberInput label, .stSelectbox label, .stSlider label {
        color: #333333 !important;
    }
    p {
        color: #333333 !important;
    }
    /* Style the sidebar button and its icon */
    [data-testid="collapsedControl"] {
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
    /* Style the Get Recommendations button */
    .stButton > button {
        background: linear-gradient(45deg, #0099FF, #00E5FF, #FFB74D, #FF9800) !important;
        color: black !important;
        font-weight: bold !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }
    /* Style the Home button */
    .home-button {
        position: fixed !important;
        top: 1rem !important;
        left: 1rem !important;
        z-index: 1000 !important;
    }
    .home-button a {
        text-decoration: none !important;
    }
    .home-button button {
        background: linear-gradient(45deg, #0099FF, #00E5FF, #FFB74D, #FF9800) !important;
        color: black !important;
        font-weight: bold !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        border-radius: 4px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }
    .home-button button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }
    /* Force black text for results */
    .analysis-results, .workout-plan, .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6, .stMarkdown strong, .stMarkdown em {
        color: black !important;
    }
    /* Target specific Streamlit elements */
    [data-testid="stMarkdown"] {
        color: black !important;
    }
    [data-testid="stMarkdown"] p {
        color: black !important;
    }
    [data-testid="stMarkdown"] strong {
        color: black !important;
    }
    [data-testid="stMarkdown"] em {
        color: black !important;
    }
    /* Target subheader specifically */
    .stMarkdown h2, .stMarkdown h3 {
        color: black !important;
    }
    /* Additional subheader targeting */
    div[data-testid="stMarkdown"] h2, div[data-testid="stMarkdown"] h3 {
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

# Add Home button using Streamlit
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    st.markdown("""
        <a href="/" target="_self" style="text-decoration: none;">
            <button style="
                background: linear-gradient(45deg, #F5F5F5, #E0E0E0, #EEEEEE, #BDBDBD);
                color: black;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s ease;
                margin-top: 1rem;
                ">
                ⬅️ Back to Home
            </button>
        </a>
    """, unsafe_allow_html=True)

# Initialize chatbot
chatbot = GymChatbot()

# Update title with gradient
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
                background: linear-gradient(45deg, #0099FF, #00E5FF, #FFB74D, #FF9800);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                display: inline-block;
                font-size: 8vh !important;
                font-weight: 900 !important;
            ">AI Workout Planner</span>
        </h1>
    </div>
""", unsafe_allow_html=True)

# Update subtitle styling
st.markdown("""
    <div style="
        text-align: center;
        color: #333333;
        font-size: 1.5rem;
        margin-bottom: 2rem;
        pointer-events: none;
    ">
        Enter your details to get personalized workout recommendations:
    </div>
""", unsafe_allow_html=True)

# Collect user inputs
age = st.number_input("What is your age?", min_value=18, max_value=100, value=25)
gender = st.selectbox("What is your gender?", ["Male", "Female"])
weight = st.number_input("What is your weight (in lbs)?", min_value=75, max_value=330)
height_feet = st.number_input("What is your height (feet)?", min_value=4, max_value=7)
height_inches = st.number_input("Inches:", min_value=0, max_value=11)

# Calculate BMI
weight_kg = weight / 2.20462
height_m = ((height_feet * 12) + height_inches) * 0.0254
bmi = weight_kg / (height_m ** 2)

# Calculate heart rates based on user characteristics
def calculate_heart_rates(age, gender, bmi):
    # Calculate maximum heart rate using the Tanaka formula (more accurate than 220-age)
    max_bpm = 208 - (0.7 * age)
    
    # Adjust max heart rate based on BMI
    if bmi > 30:  # Obese
        max_bpm *= 0.95
    elif bmi > 25:  # Overweight
        max_bpm *= 0.97
    
    # Calculate average heart rate during exercise (70% of max for moderate intensity)
    avg_bpm = int(max_bpm * 0.7)
    
    # Calculate resting heart rate based on age and gender
    if gender == 'Male':
        resting_bpm = 70 - (0.3 * (age - 20))  # Decreases with age
    else:
        resting_bpm = 72 - (0.3 * (age - 20))  # Slightly higher for females
    
    # Adjust resting heart rate based on BMI
    if bmi > 30:  # Obese
        resting_bpm += 5
    elif bmi > 25:  # Overweight
        resting_bpm += 3
    
    return int(max_bpm), avg_bpm, int(resting_bpm)

# Calculate heart rates
max_bpm, avg_bpm, resting_bpm = calculate_heart_rates(age, gender, bmi)

# Workout session details
session_duration = st.number_input("Typical workout session duration (hours):", min_value=0.25, max_value=3.0, value=1.0)
workout_freq = st.slider("How many days per week do you work out?", min_value=1, max_value=7)

# Body fat percentage
default_fat = 15 if gender == 'Male' else 25
fat_percentage = st.number_input("What is your body fat percentage?", min_value=5, max_value=50, value=default_fat)

# Water intake
cups = st.number_input("How many cups of water do you drink per day? (1 cup = 8 oz)", min_value=2, max_value=20)
water_intake_liters = cups * 0.236588

# Fitness goals
goals = st.selectbox("What is your fitness goal?", ["Weight Loss", "Muscle Building", "Cardiovascular Health", "Flexibility", "General Fitness"])

# Step 2: Process the inputs
if st.button("**Get AI Calculated Workout and Meal Plan!**"):
    # Prepare user information for chatbot
    user_info = {
        'Age': age,
        'Gender': gender,
        'Weight (kg)': weight_kg,
        'Height (m)': height_m,
        'Max_BPM': max_bpm,
        'Avg_BPM': avg_bpm,
        'Resting_BPM': resting_bpm,
        'Session_Duration (hours)': session_duration,
        'Fat_Percentage': fat_percentage,
        'Water_Intake (liters)': water_intake_liters,
        'Workout_Frequency (days/week)': workout_freq,
        'BMI': bmi,
        'Goal': goals,
    }

    # Call chatbot methods to generate predictions
    user_calories, user_workout, user_experience = chatbot.prepare_prediction_data(user_info)
    predicted_calories = chatbot.calories_model.predict(user_calories)[0]
    predicted_workout = chatbot.workout_model.predict(user_workout)[0]
    predicted_experience = chatbot.experience_model.predict(user_experience)[0]

    # Get workout recommendations
    recommendations = chatbot.get_exercise_recommendations(user_info, predicted_workout, predicted_experience)

    # Generate and display workout plan
    plan = chatbot.get_workout_plan(user_info, predicted_workout, predicted_calories, predicted_experience, recommendations)

    # Generate meal recommendations
    nutrient_file = "nutrients_csvfile.csv"
    meal_plan = gym_ml_model_new.generate_meal_recommendations(predicted_calories, nutrient_file, goals)

    # Store results in session state
    st.session_state.workout_results = {
        'predicted_calories': predicted_calories,
        'predicted_workout': predicted_workout,
        'predicted_experience': predicted_experience,
        'plan': plan,
        'meal_plan': meal_plan
    }

    # Redirect to results page
    st.switch_page("pages/AI_Workout_Planner_Results.py")
