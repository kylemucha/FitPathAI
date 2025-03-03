import streamlit as st

# Page configuration
st.set_page_config(
    page_title="FitPathAI - Workout Results",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Copy the same CSS from AI_Workout_Planner.py
st.markdown("""
    <style>
    # ... (copy all the CSS from AI_Workout_Planner.py) ...
    </style>
""", unsafe_allow_html=True)

# Add Home button
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    st.markdown("""
        <a href="/" target="_self" style="text-decoration: none;">
            <button style="
                background: linear-gradient(45deg, #0099FF, #00E5FF, #FFB74D, #FF9800);
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
            ">Your Workout Results</span>
        </h1>
    </div>
""", unsafe_allow_html=True)

# Check if results exist in session state
if 'workout_results' not in st.session_state:
    st.warning("Please complete the workout planner form first!")
    st.markdown("""
        <a href="/AI_Workout_Planner" target="_self" style="text-decoration: none;">
            <button style="
                background: linear-gradient(45deg, #0099FF, #00E5FF, #FFB74D, #FF9800);
                color: black;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s ease;
                ">
                Go to Workout Planner
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
    st.subheader("Your Personalized Workout Plan")
    
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
                background: linear-gradient(45deg, #0099FF, #00E5FF, #FFB74D, #FF9800);
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
