import streamlit as st

# Page configuration
st.set_page_config(
    page_title="FitPathAI - Workout Results",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add the same CSS styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: white;
        color: black;
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
        color: black;
        text-align: center;
    }
    .title {
        font-size: 2rem !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
        color: black;
        text-align: center;
    }
    .subtitle {
        font-size: 1.5rem !important;
        color: black;
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
    [data-testid="stMarkdown"] {
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

# Add Home button
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

# Title with gradient
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
            ">Your Workout Plan Results</span>
        </h1>
    </div>
""", unsafe_allow_html=True)

# Check if results exist in session state
if 'workout_results' not in st.session_state:
    st.markdown('<p style="color: #8B0000; font-weight: bold;">Please complete the workout planner form first!</p>', unsafe_allow_html=True)
    st.markdown("""
        <a href="/AI_Workout_Planner" target="_self" style="text-decoration: none;">
            <button style="
                background: linear-gradient(45deg, #F5F5F5, #E0E0E0, #EEEEEE, #BDBDBD);
                color: black;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s ease;
                ">
                Go to AI Workout Planner
            </button>
        </a>
    """, unsafe_allow_html=True)
else:
    # Get results from session state
    results = st.session_state.workout_results
    
    # Display analysis results
    st.markdown(f"### Analysis Results")
    st.markdown(f"- **Calories Burned per Session:** {results['predicted_calories']:.2f}")
    st.markdown(f"- **Recommended Workout Type:** {results['predicted_workout']}")
    st.markdown(f"- **Experience Level:** {results['predicted_experience']} (1=Beginner, 2=Intermediate, 3=Advanced)")

    # Display workout plan
    plan = results['plan']
    st.markdown('<h2 style="color: #1E88E5;">Your Personalized Workout Plan</h2>', unsafe_allow_html=True)
    
    # Display workout plan in a structured format
    st.markdown(f"**Workout Type:** {plan['workout_type']}")
    st.markdown(f"**Experience Level:** {plan['experience_level']}")
    st.markdown(f"**Sessions per Week:** {plan['sessions_per_week']}")
    st.markdown(f"**Calories per Session:** {plan['calories_per_session']}")
    st.markdown(f"**Session Duration:** {plan['session_duration']}")
    st.markdown(f"**Hydration Recommendation:** {plan['hydration']}")

    # Display daily exercises
    st.markdown("### Weekly Schedule")
    for day, details in plan['daily_exercises'].items():
        st.markdown(f"**{day}:** {details['focus']}")
        st.markdown("- " + "\n- ".join(details['exercises']))

    # Additional notes and advice
    st.markdown("### Notes")
    st.markdown("- Always warm up for 5-10 minutes before starting your workout")
    st.markdown("- Cool down and stretch for 5-10 minutes after your workout")
    st.markdown(f"- Stay hydrated! Drink {plan['hydration']} throughout the day")
    st.markdown("- Listen to your body and adjust intensity as needed")
    st.markdown("- For best results, follow this plan consistently for at least 4-6 weeks")

    # Add a button to start over
    st.markdown("""
        <a href="/AI_Workout_Planner" target="_self" style="text-decoration: none;">
            <button style="
                background: linear-gradient(45deg, #F5F5F5, #E0E0E0, #EEEEEE, #BDBDBD);
                color: black;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s ease;
                margin-top: 2rem;
                ">
                Create New Workout Plan
            </button>
        </a>
    """, unsafe_allow_html=True)
