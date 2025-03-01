import streamlit as st
import pandas as pd
from gym_chatbot import GymChatbot

# Initialize chatbot
chatbot = GymChatbot()

# Streamlit app title
st.title("🏋️ Gym Recommendation Chatbot")

# Step 1: Collect user information through Streamlit inputs
st.header("Enter your details to get personalized workout recommendations:")

# Collect user inputs
age = st.number_input("What is your age?", min_value=18, max_value=80, value=25)
gender = st.selectbox("What is your gender?", ["Male", "Female"])
weight = st.number_input("What is your weight (in lbs)?", min_value=88, max_value=330)
height_feet = st.number_input("What is your height (feet)?", min_value=4, max_value=7)
height_inches = st.number_input("Inches:", min_value=0, max_value=11)

# Calculate BMI
weight_kg = weight / 2.20462
height_m = ((height_feet * 12) + height_inches) * 0.0254
bmi = weight_kg / (height_m ** 2)
st.write(f"**Your BMI is:** {bmi:.2f}")

# Heart rate information
max_bpm = st.number_input("What is your maximum heart rate during exercise?", min_value=120, max_value=220, value=220-age)
avg_bpm = st.number_input("What is your average heart rate during exercise?", min_value=100, max_value=200, value=int((220-age) * 0.7))
resting_bpm = st.number_input("What is your resting heart rate?", min_value=40, max_value=100, value=70)

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
if st.button("Get Recommendations"):
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

    # Display analysis results
    st.markdown(f"### Analysis Results")
    st.markdown(f"- **Calories Burned per Session:** {predicted_calories:.2f}")
    st.markdown(f"- **Recommended Workout Type:** {predicted_workout}")
    st.markdown(f"- **Experience Level:** {predicted_experience} (1=Beginner, 2=Intermediate, 3=Advanced)")

    # Get workout recommendations
    recommendations = chatbot.get_exercise_recommendations(user_info, predicted_workout, predicted_experience)

    # Generate and display workout plan
    plan = chatbot.get_workout_plan(user_info, predicted_workout, predicted_calories, predicted_experience, recommendations)
    st.subheader("Your Personalized Workout Plan")
    
    # Display workout plan in a more structured format
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
