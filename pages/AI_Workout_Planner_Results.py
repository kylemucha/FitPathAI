import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import io

def generate_pdf(plan, meal_plan):
    # Create PDF object
    pdf = FPDF()
    pdf.add_page()
    
    # Set font
    pdf.set_font("Arial", "B", 16)
    
    # Add title
    pdf.cell(0, 10, "Your Personalized Workout & Nutrition Plan", ln=True, align='C')
    
    # Add date
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%B %d, %Y')}", ln=True, align='C')
    
    # Add workout plan section
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Your Personalized Workout Plan", ln=True)
    pdf.set_font("Arial", "", 12)
    
    # Add workout details
    pdf.cell(0, 10, f"Workout Type: {plan['workout_type']}", ln=True)
    pdf.cell(0, 10, f"Experience Level: {plan['experience_level']}", ln=True)
    pdf.cell(0, 10, f"Sessions per Week: {plan['sessions_per_week']}", ln=True)
    pdf.cell(0, 10, f"Calories per Session: {plan['calories_per_session']}", ln=True)
    pdf.cell(0, 10, f"Session Duration: {plan['session_duration']}", ln=True)
    pdf.cell(0, 10, f"Hydration Recommendation: {plan['hydration']}", ln=True)
    
    # Add weekly schedule
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Weekly Schedule", ln=True)
    pdf.set_font("Arial", "", 12)
    
    for day, details in plan['daily_exercises'].items():
        pdf.cell(0, 10, f"{day}: {details['focus']}", ln=True)
        for exercise in details['exercises']:
            pdf.cell(10, 10, "-", ln=False)
            pdf.cell(0, 10, exercise, ln=True)
    
    # Add nutrition plan section
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Recommended Daily Nutrition Plan", ln=True)
    pdf.set_font("Arial", "", 12)
    
    # Calculate and add total nutrients
    total_calories = sum(details['Calories'] * details['Servings'] for details in meal_plan.values())
    total_protein = sum(details['Protein'] * details['Servings'] for details in meal_plan.values())
    total_carbs = sum(details['Carbs'] * details['Servings'] for details in meal_plan.values())
    total_fiber = sum(details['Fiber'] * details['Servings'] for details in meal_plan.values())
    
    pdf.cell(0, 10, "Total Daily Nutrition:", ln=True)
    pdf.cell(0, 10, f"- Total Calories: {total_calories:.1f}", ln=True)
    pdf.cell(0, 10, f"- Total Protein: {total_protein:.1f}g", ln=True)
    pdf.cell(0, 10, f"- Total Carbs: {total_carbs:.1f}g", ln=True)
    pdf.cell(0, 10, f"- Total Fiber: {total_fiber:.1f}g", ln=True)
    
    # Add food items
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Recommended Foods", ln=True)
    pdf.set_font("Arial", "", 12)
    
    for food, details in meal_plan.items():
        total_calories = details['Calories'] * details['Servings']
        total_protein = details['Protein'] * details['Servings']
        total_carbs = details['Carbs'] * details['Servings']
        total_fiber = details['Fiber'] * details['Servings']
        
        pdf.cell(0, 10, f"{food} (x{details['Servings']})", ln=True)
        pdf.cell(10, 10, "-", ln=False)
        pdf.cell(0, 10, f"Calories: {total_calories:.1f}", ln=True)
        pdf.cell(10, 10, "-", ln=False)
        pdf.cell(0, 10, f"Protein: {total_protein:.1f}g", ln=True)
        pdf.cell(10, 10, "-", ln=False)
        pdf.cell(0, 10, f"Carbs: {total_carbs:.1f}g", ln=True)
        pdf.cell(10, 10, "-", ln=False)
        pdf.cell(0, 10, f"Fiber: {total_fiber:.1f}g", ln=True)
        pdf.ln(5)
    
    # Add notes section
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Important Notes", ln=True)
    pdf.set_font("Arial", "", 12)
    
    notes = [
        "Always warm up for 5-10 minutes before starting your workout",
        "Cool down and stretch for 5-10 minutes after your workout",
        f"Stay hydrated! Drink {plan['hydration']} throughout the day",
        "Listen to your body and adjust intensity as needed",
        "For best results, follow this plan consistently for at least 4-6 weeks",
        "Eat your post-workout meal within 30 minutes of completing your workout",
        "Adjust portion sizes based on your hunger and energy levels"
    ]
    
    for note in notes:
        pdf.cell(10, 10, "-", ln=False)
        pdf.cell(0, 10, note, ln=True)
    
    # Get the PDF as bytes
    return pdf.output(dest='S').encode('latin-1')

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
    /* Make all text black by default */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: black !important;
    }
    /* Allow colored headings with higher specificity */
    div[data-testid="stMarkdown"] h2[style*="color: #2196F3"],
    div[data-testid="stMarkdown"] h2[style*="color: #4CAF50"] {
        color: inherit !important;
    }
    /* Remove conflicting rules */
    .stMarkdown h2, .stMarkdown h3 {
        color: inherit !important;
    }
    div[data-testid="stMarkdown"] h2, div[data-testid="stMarkdown"] h3 {
        color: inherit !important;
    }
    /* Force black text for all content */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6, .stMarkdown strong, .stMarkdown em, [data-testid="stMarkdown"], [data-testid="stMarkdown"] p, [data-testid="stMarkdown"] strong, [data-testid="stMarkdown"] em {
        color: black !important;
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
    /* Target expander content */
    .streamlit-expanderHeader {
        color: black !important;
    }
    .streamlit-expanderContent {
        color: black !important;
    }
    /* Target all text within expanders */
    .streamlit-expanderContent p, 
    .streamlit-expanderContent strong, 
    .streamlit-expanderContent em {
        color: black !important;
    }
    /* Additional targeting for expander content */
    div[data-testid="stExpander"] {
        color: black !important;
    }
    div[data-testid="stExpander"] p {
        color: black !important;
    }
    div[data-testid="stExpander"] strong {
        color: black !important;
    }
    div[data-testid="stExpander"] em {
        color: black !important;
    }
    /* Print button styles */
    .print-button {
        background: linear-gradient(45deg, #FF9800, #FFB74D, #FFA726, #FF8F00) !important;
        color: black !important;
        font-weight: bold !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
        border-radius: 4px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        margin: 1rem 0 !important;
    }
    .print-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }
    
    /* Print-specific styles */
    @media print {
        .no-print {
            display: none !important;
        }
        .print-only {
            display: block !important;
        }
        body {
            padding: 20px !important;
        }
        .stMarkdown {
            color: black !important;
        }
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

# Add print-only header that will only show when printing
st.markdown("""
    <div class="print-only" style="display: none; text-align: center; margin-bottom: 2rem;">
        <h1 style="color: black;">Your Personalized Workout & Nutrition Plan</h1>
        <p style="color: black;">Generated on: {}</p>
    </div>
""".format(pd.Timestamp.now().strftime("%B %d, %Y")), unsafe_allow_html=True)

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
    plan = results['plan']
    
    # Display analysis results
    st.markdown(f"### Analysis Results")
    st.markdown(f"- **Recommended Workout Type:** {plan['workout_type']}")
    st.markdown(f"- **Experience Level:** {results['predicted_experience']} (   1=Beginner, 2=Intermediate, 3=Advanced)")

    # Display workout plan
    st.markdown('<div style="color: #2196F3; font-weight: bold; font-size: 2em; margin-bottom: 1rem;">Your Personalized Workout Plan</div>', unsafe_allow_html=True)
    
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

    # Display meal recommendations
    st.markdown('<div style="color: #4CAF50; font-weight: bold; font-size: 2em; margin-bottom: 1rem;">Recommended Daily Nutrition Plan</div>', unsafe_allow_html=True)
    meal_plan = results['meal_plan']
    
    # Calculate total nutrients
    total_calories = sum(details['Calories'] * details['Servings'] for details in meal_plan.values())
    total_protein = sum(details['Protein'] * details['Servings'] for details in meal_plan.values())
    total_carbs = sum(details['Carbs'] * details['Servings'] for details in meal_plan.values())
    total_fiber = sum(details['Fiber'] * details['Servings'] for details in meal_plan.values())
    
    # Display total nutrients
    st.markdown("### Total Daily Nutrition")
    st.markdown(f"- **Total Calories:** {total_calories:.1f}")
    st.markdown(f"- **Total Protein:** {total_protein:.1f}g")
    st.markdown(f"- **Total Carbs:** {total_carbs:.1f}g")
    st.markdown(f"- **Total Fiber:** {total_fiber:.1f}g")
    
    # Display individual food items
    st.markdown("### Recommended Foods")
    for food, details in meal_plan.items():
        total_calories = details['Calories'] * details['Servings']
        total_protein = details['Protein'] * details['Servings']
        total_carbs = details['Carbs'] * details['Servings']
        total_fiber = details['Fiber'] * details['Servings']
        
        with st.expander(f"**{food}** (x{details['Servings']})"):
            st.markdown(f"- Calories: {total_calories:.1f}")
            st.markdown(f"- Protein: {total_protein:.1f}g")
            st.markdown(f"- Carbs: {total_carbs:.1f}g")
            st.markdown(f"- Fiber: {total_fiber:.1f}g")

    # Additional notes and advice
    st.markdown("### Notes")
    st.markdown("- Always warm up for 5-10 minutes before starting your workout")
    st.markdown("- Cool down and stretch for 5-10 minutes after your workout")
    st.markdown(f"- Stay hydrated! Drink {plan['hydration']} throughout the day")
    st.markdown("- Listen to your body and adjust intensity as needed")
    st.markdown("- For best results, follow this plan consistently for at least 4-6 weeks")
    st.markdown("- Eat your post-workout meal within 30 minutes of completing your workout")
    st.markdown("- Adjust portion sizes based on your hunger and energy levels")

    # Generate PDF and create download button
    pdf_bytes = generate_pdf(plan, meal_plan)
    st.download_button(
        label="📥 Download Workout Plan as PDF",
        data=pdf_bytes,
        file_name=f"workout_plan_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf"
    )
