import pandas as pd
import numpy as np
import pickle
import os
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import gym_ml_model  # Import our ML model script

class GymChatbot:
    def __init__(self):
        """Initialize the chatbot with trained models."""
        print("Initializing Gym Recommendation Chatbot...")
        
        # Check if models exist, if not train them
        if not os.path.exists('models'):
            os.makedirs('models')
            self.train_models()
        else:
            try:
                self.load_models()
            except:
                print("Could not load models, training new ones...")
                self.train_models()
        
        # Load the dataset for reference
        self.dataset = pd.read_csv('members_with_exercise_recommendations.csv')
        
        # Extract unique workout types and experience levels
        self.workout_types = self.dataset['Workout_Type'].unique()
        self.experience_levels = sorted(self.dataset['Experience_Level'].unique())
        
        print("Chatbot ready! Let's help you find the perfect workout.")
    
    def train_models(self):
        """Train the machine learning models."""
        print("Training machine learning models...")
        
        # Load and preprocess data
        df = gym_ml_model.load_and_explore_data()
        df_ml = gym_ml_model.preprocess_data(df)
        
        # Train models
        self.calories_model = gym_ml_model.calories_burned_prediction(df_ml)
        self.workout_model = gym_ml_model.workout_type_prediction(df_ml)
        self.experience_model = gym_ml_model.experience_level_prediction(df_ml)
        
        # Save models
        self.save_models()
        
        print("Models trained successfully!")
    
    def save_models(self):
        """Save the trained models to disk."""
        with open('models/calories_model.pkl', 'wb') as f:
            pickle.dump(self.calories_model, f)
        
        with open('models/workout_model.pkl', 'wb') as f:
            pickle.dump(self.workout_model, f)
        
        with open('models/experience_model.pkl', 'wb') as f:
            pickle.dump(self.experience_model, f)
    
    def load_models(self):
        """Load the trained models from disk."""
        with open('models/calories_model.pkl', 'rb') as f:
            self.calories_model = pickle.load(f)
        
        with open('models/workout_model.pkl', 'rb') as f:
            self.workout_model = pickle.load(f)
        
        with open('models/experience_model.pkl', 'rb') as f:
            self.experience_model = pickle.load(f)
    
    def get_user_info(self):
        """Collect user information through a conversational interface."""
        print("\n--- Let's get to know you better to provide personalized recommendations ---")
        
        user_info = {}
        
        # Collect basic information
        user_info['Age'] = self.get_numeric_input("What is your age? ", 18, 80)
        
        gender = input("What is your gender? (m/f): ").strip().lower()
        while gender not in ['m', 'f', 'male', 'female']:
            print("Please enter 'm' for male or 'f' for female.")
            gender = input("What is your gender? (m/f): ").strip().lower()
        
        # Convert short form to full gender name
        if gender == 'm' or gender == 'male':
            user_info['Gender'] = 'Male'
        else:
            user_info['Gender'] = 'Female'
        
        # Get weight in pounds and convert to kg
        weight_lbs = self.get_numeric_input("What is your weight in pounds? ", 88, 330)  # 40kg ~ 88lbs, 150kg ~ 330lbs
        user_info['Weight (kg)'] = weight_lbs / 2.20462  # Convert pounds to kg
        
        # Get height in feet and inches
        feet = self.get_numeric_input("What is your height? (feet): ", 4, 7)
        inches = self.get_numeric_input("Inches: ", 0, 11)
        total_inches = (feet * 12) + inches
        user_info['Height (m)'] = total_inches * 0.0254  # Convert inches to meters
        
        # Calculate BMI
        user_info['BMI'] = user_info['Weight (kg)'] / (user_info['Height (m)'] ** 2)
        print(f"Your BMI is: {user_info['BMI']:.2f}")
        
        # Display converted measurements for user reference
        print(f"For reference: Your weight is {user_info['Weight (kg)']:.1f} kg and height is {user_info['Height (m)']:.2f} meters")
        
        # Heart rate information with defaults
        print("\nFor heart rate information, you can press Enter to use default values based on your age")
        
        # Calculate default heart rates based on age
        default_max_bpm = 220 - user_info['Age']
        default_avg_bpm = int(default_max_bpm * 0.7)
        default_resting_bpm = 70
        
        # Max BPM with default
        max_bpm_input = input(f"What is your maximum heart rate during exercise? (press Enter for {default_max_bpm}): ").strip()
        if max_bpm_input:
            user_info['Max_BPM'] = self.validate_numeric_range(max_bpm_input, 120, 220)
        else:
            user_info['Max_BPM'] = default_max_bpm
            print(f"Using default maximum heart rate: {default_max_bpm}")
        
        # Avg BPM with default
        avg_bpm_input = input(f"What is your average heart rate during exercise? (press Enter for {default_avg_bpm}): ").strip()
        if avg_bpm_input:
            user_info['Avg_BPM'] = self.validate_numeric_range(avg_bpm_input, 100, 200)
        else:
            user_info['Avg_BPM'] = default_avg_bpm
            print(f"Using default average heart rate: {default_avg_bpm}")
        
        # Resting BPM with default
        resting_bpm_input = input(f"What is your resting heart rate? (press Enter for {default_resting_bpm}): ").strip()
        if resting_bpm_input:
            user_info['Resting_BPM'] = self.validate_numeric_range(resting_bpm_input, 40, 100)
        else:
            user_info['Resting_BPM'] = default_resting_bpm
            print(f"Using default resting heart rate: {default_resting_bpm}")
        
        # Workout information
        user_info['Session_Duration (hours)'] = self.get_numeric_input("How long are your typical workout sessions in hours? (e.g., 1.0): ", 0.25, 3)
        
        # Body fat percentage with default based on gender
        default_fat = 15 if user_info['Gender'] == 'Male' else 25
        fat_input = input(f"What is your body fat percentage? (press Enter for {default_fat}%): ").strip()
        if fat_input:
            user_info['Fat_Percentage'] = self.validate_numeric_range(fat_input, 5, 50)
        else:
            user_info['Fat_Percentage'] = default_fat
            print(f"Using default body fat percentage: {default_fat}%")
        
        # Get water intake in cups and convert to liters (1 cup ≈ 0.236588 liters)
        cups = self.get_numeric_input("How many cups of water do you drink per day? (1 cup = 8 oz): ", 2, 20)
        user_info['Water_Intake (liters)'] = cups * 0.236588
        
        user_info['Workout_Frequency (days/week)'] = self.get_numeric_input("How many days per week do you work out? ", 1, 7)
        
        # Goals
        print("\nWhat are your fitness goals? (select one)")
        print("1. Lose weight")
        print("2. Build muscle")
        print("3. Improve cardiovascular health")
        print("4. Increase flexibility")
        print("5. General fitness")
        
        goal_choice = int(self.get_numeric_input("Enter the number of your primary goal: ", 1, 5))
        goals = ["Weight Loss", "Muscle Building", "Cardiovascular Health", "Flexibility", "General Fitness"]
        user_info['Goal'] = goals[goal_choice - 1]
        
        return user_info
    
    def get_numeric_input(self, prompt, min_val, max_val):
        """Get numeric input from the user within a specified range."""
        while True:
            try:
                value = float(input(prompt))
                if min_val <= value <= max_val:
                    return value
                else:
                    print(f"Please enter a value between {min_val} and {max_val}.")
            except ValueError:
                print("Please enter a valid number.")
    
    def prepare_prediction_data(self, user_info):
        """Prepare the user data for model prediction."""
        # Create a DataFrame with the user info
        user_df = pd.DataFrame({
            'Age': [user_info['Age']],
            'Gender': [user_info['Gender']],
            'Weight (kg)': [user_info['Weight (kg)']],
            'Height (m)': [user_info['Height (m)']],
            'Max_BPM': [user_info['Max_BPM']],
            'Avg_BPM': [user_info['Avg_BPM']],
            'Resting_BPM': [user_info['Resting_BPM']],
            'Session_Duration (hours)': [user_info['Session_Duration (hours)']],
            'Fat_Percentage': [user_info['Fat_Percentage']],
            'Water_Intake (liters)': [user_info['Water_Intake (liters)']],
            'Workout_Frequency (days/week)': [user_info['Workout_Frequency (days/week)']],
            'BMI': [user_info['BMI']],
            # Dummy values needed for the model pipeline
            'Workout_Type': ['Strength'],
            'Experience_Level': [2],
            'Calories_Burned': [0]
        })
        
        # Create specific DataFrames for each model
        user_calories = user_df.drop(['Calories_Burned'], axis=1)
        user_workout = user_df.drop(['Workout_Type'], axis=1)
        user_experience = user_df.drop(['Experience_Level', 'Workout_Type'], axis=1)
        
        return user_calories, user_workout, user_experience
    
    def get_exercise_recommendations(self, user_info, predicted_workout, predicted_experience):
        """Get personalized exercise recommendations based on user profile and predictions."""
        # Filter the dataset based on predicted workout type and experience level
        filtered_df = self.dataset[
            (self.dataset['Workout_Type'] == predicted_workout) & 
            (self.dataset['Experience_Level'] == predicted_experience)
        ]
        
        # If we don't have enough matches, relax the experience level constraint
        if len(filtered_df) < 5:
            filtered_df = self.dataset[self.dataset['Workout_Type'] == predicted_workout]
        
        # If we still don't have enough matches, use the whole dataset
        if len(filtered_df) < 5:
            filtered_df = self.dataset
        
        # Find similar users based on BMI and age
        filtered_df['BMI_diff'] = abs(filtered_df['BMI'] - user_info['BMI'])
        filtered_df['Age_diff'] = abs(filtered_df['Age'] - user_info['Age'])
        
        # Normalize differences
        if filtered_df['BMI_diff'].max() > 0:
            filtered_df['BMI_diff'] = filtered_df['BMI_diff'] / filtered_df['BMI_diff'].max()
        if filtered_df['Age_diff'].max() > 0:
            filtered_df['Age_diff'] = filtered_df['Age_diff'] / filtered_df['Age_diff'].max()
        
        # Calculate similarity score (lower is better)
        filtered_df['similarity'] = filtered_df['BMI_diff'] + filtered_df['Age_diff']
        
        # Get top 10 most similar users to have more exercise options
        similar_users = filtered_df.sort_values('similarity').head(10)
        
        # Extract their recommended exercises
        all_exercises = []
        for _, user in similar_users.iterrows():
            if pd.notna(user['Recommended_Exercises']):
                exercises = user['Recommended_Exercises'].split(', ')
                all_exercises.extend(exercises)
        
        # Remove duplicates
        unique_exercises = list(dict.fromkeys(all_exercises))
        
        # If we don't have enough exercises, add some generic ones based on workout type
        generic_exercises = {
            'Strength': [
                'Bench Press', 'Squats', 'Deadlifts', 'Shoulder Press', 
                'Bicep Curls', 'Tricep Extensions', 'Lat Pulldowns', 'Lunges',
                'Push-ups', 'Pull-ups', 'Dumbbell Rows', 'Leg Press'
            ],
            'Cardio': [
                'Running', 'Cycling', 'Jumping Jacks', 'Burpees',
                'Mountain Climbers', 'High Knees', 'Jump Rope', 'Stair Climbing',
                'Elliptical Training', 'Swimming', 'Rowing', 'Boxing'
            ],
            'HIIT': [
                'Burpees', 'Mountain Climbers', 'Jump Squats', 'Plank Jacks',
                'High Knees', 'Kettlebell Swings', 'Box Jumps', 'Battle Ropes',
                'Jumping Lunges', 'Push-up Variations', 'Sprints', 'Medicine Ball Slams'
            ],
            'Yoga': [
                'Downward Dog', 'Warrior Pose', 'Tree Pose', 'Child\'s Pose',
                'Cobra Pose', 'Triangle Pose', 'Bridge Pose', 'Plank Pose',
                'Chair Pose', 'Cat-Cow Stretch', 'Sun Salutation', 'Corpse Pose'
            ]
        }
        
        # Add generic exercises if needed
        if len(unique_exercises) < 20 and predicted_workout in generic_exercises:
            for exercise in generic_exercises[predicted_workout]:
                if exercise not in unique_exercises:
                    unique_exercises.append(exercise)
        
        # Return at least 20 exercises (or all if less than 20 are available)
        return unique_exercises[:min(28, len(unique_exercises))]
    
    def get_workout_plan(self, user_info, predicted_workout, predicted_calories, predicted_experience, recommendations):
        """Create a personalized workout plan based on user info and predictions."""
        experience_descriptions = {
            1: "Beginner",
            2: "Intermediate",
            3: "Advanced"
        }
        
        goal_workout_mapping = {
            "Weight Loss": ["HIIT", "Cardio"],
            "Muscle Building": ["Strength"],
            "Cardiovascular Health": ["Cardio", "HIIT"],
            "Flexibility": ["Yoga"],
            "General Fitness": ["HIIT", "Strength", "Cardio", "Yoga"]
        }
        
        # Check if predicted workout aligns with user's goal
        goal_workouts = goal_workout_mapping[user_info['Goal']]
        if predicted_workout in goal_workouts:
            recommended_workout = predicted_workout
        else:
            # If not, recommend the first workout type that matches their goal
            recommended_workout = goal_workouts[0]
        
        # Determine workout days
        sessions_per_week = min(int(user_info['Workout_Frequency (days/week)']), 5)
        
        # Create a weekly schedule with workout days and rest days
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        workout_days = []
        rest_days = []
        
        # Distribute workouts with rest days if possible
        for i, day in enumerate(days):
            if len(workout_days) < sessions_per_week:
                if i % 2 == 0 or sessions_per_week > 3:
                    workout_days.append(day)
                else:
                    rest_days.append(day)
            else:
                rest_days.append(day)
        
        # Organize exercises by workout day (4 exercises per day)
        daily_exercises = {}
        exercise_index = 0
        
        # Different exercise focus for each day if it's a strength workout
        strength_focus = {
            0: "Upper Body",
            1: "Lower Body",
            2: "Core",
            3: "Full Body",
            4: "Arms and Back"
        }
        
        for i, day in enumerate(workout_days):
            # Get 4 exercises for this day
            day_exercises = []
            for j in range(4):
                if exercise_index < len(recommendations):
                    day_exercises.append(recommendations[exercise_index])
                    exercise_index += 1
                else:
                    # If we run out of recommendations, start over
                    exercise_index = 0
                    if exercise_index < len(recommendations):
                        day_exercises.append(recommendations[exercise_index])
                        exercise_index += 1
            
            # Add focus area for strength workouts
            if recommended_workout == "Strength":
                focus = strength_focus.get(i % len(strength_focus), "Full Body")
                daily_exercises[day] = {"focus": focus, "exercises": day_exercises}
            else:
                daily_exercises[day] = {"focus": recommended_workout, "exercises": day_exercises}
        
        # Create the workout plan
        plan = {
            "workout_type": recommended_workout,
            "experience_level": experience_descriptions.get(predicted_experience, "Beginner"),
            "sessions_per_week": sessions_per_week,
            "calories_per_session": int(predicted_calories),
            "session_duration": f"{user_info['Session_Duration (hours)']:.2f} hours",
            "daily_exercises": daily_exercises,
            "workout_days": workout_days,
            "rest_days": rest_days,
            "hydration": f"{user_info['Weight (kg)'] * 0.03:.1f} liters of water per day"
        }
        
        return plan
    
    def display_workout_plan(self, plan):
        """Display the workout plan in a user-friendly format."""
        print("\n" + "="*60)
        print(f"YOUR PERSONALIZED {plan['workout_type'].upper()} WORKOUT PLAN")
        print("="*60)
        
        print(f"\nExperience Level: {plan['experience_level']}")
        print(f"Recommended Sessions: {plan['sessions_per_week']} days per week")
        print(f"Estimated Calories Burned: {plan['calories_per_session']} per session")
        print(f"Recommended Session Duration: {plan['session_duration']}")
        
        # Convert liters to cups (1 liter ≈ 4.22675 cups)
        cups = float(plan['hydration'].split()[0]) * 4.22675
        print(f"Hydration Recommendation: {plan['hydration']} (approximately {cups:.1f} cups per day)")
        
        print("\nWEEKLY SCHEDULE:")
        print("-"*60)
        
        # Display workout days with exercises
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            if day in plan['workout_days']:
                day_plan = plan['daily_exercises'][day]
                print(f"\n{day}: {plan['workout_type']} Workout - {day_plan['focus']}")
                print("  Exercises:")
                for i, exercise in enumerate(day_plan['exercises'], 1):
                    print(f"  {i}. {exercise}")
                
                # Add sets and reps recommendations based on experience level and workout type
                if plan['workout_type'] == "Strength":
                    if plan['experience_level'] == "Beginner":
                        print("  Sets/Reps: 2-3 sets of 10-12 reps, moderate weight")
                    elif plan['experience_level'] == "Intermediate":
                        print("  Sets/Reps: 3-4 sets of 8-10 reps, challenging weight")
                    else:  # Advanced
                        print("  Sets/Reps: 4-5 sets of 6-8 reps, heavy weight")
                elif plan['workout_type'] == "HIIT":
                    print("  Format: 30 seconds work, 15 seconds rest, 3-4 rounds")
                elif plan['workout_type'] == "Cardio":
                    print(f"  Duration: {int(float(plan['session_duration'].split()[0]) * 60)} minutes at moderate intensity")
                elif plan['workout_type'] == "Yoga":
                    print("  Hold each pose for 30-60 seconds, focus on breathing")
            else:
                print(f"\n{day}: Rest Day")
                print("  Focus on recovery, light stretching, and staying hydrated")
        
        print("\nNOTES:")
        print("- Always warm up for 5-10 minutes before starting your workout")
        print("- Cool down and stretch for 5-10 minutes after your workout")
        print(f"- Stay hydrated! Drink {plan['hydration']} throughout the day")
        print("- Listen to your body and adjust intensity as needed")
        print("- For best results, follow this plan consistently for at least 4-6 weeks")
        print("="*60)
    
    def run(self):
        """Run the chatbot conversation."""
        print("Welcome to the Gym Recommendation Chatbot!")
        print("I'll help you find the perfect workout plan based on your profile.")
        
        # Get user information
        user_info = self.get_user_info()
        
        # Prepare data for prediction
        user_calories, user_workout, user_experience = self.prepare_prediction_data(user_info)
        
        # Make predictions
        predicted_calories = self.calories_model.predict(user_calories)[0]
        predicted_workout = self.workout_model.predict(user_workout)[0]
        predicted_experience = self.experience_model.predict(user_experience)[0]
        
        print("\nAnalyzing your profile...")
        print(f"Based on your profile, you would typically burn {predicted_calories:.2f} calories per session.")
        print(f"Your workout style matches with: {predicted_workout}")
        print(f"Your experience level appears to be: {predicted_experience} (1=Beginner, 2=Intermediate, 3=Advanced)")
        
        # Get exercise recommendations
        recommendations = self.get_exercise_recommendations(user_info, predicted_workout, predicted_experience)
        
        # Create and display workout plan
        plan = self.get_workout_plan(user_info, predicted_workout, predicted_calories, predicted_experience, recommendations)
        self.display_workout_plan(plan)
        
        print("\nWould you like to ask any questions about your workout plan? (yes/no)")
        if input().lower().startswith('y'):
            self.answer_questions(user_info, plan)
        
        print("\nThank you for using the Gym Recommendation Chatbot!")
        print("Good luck with your fitness journey!")
    
    def answer_questions(self, user_info, plan):
        """Answer user questions about their workout plan."""
        print("\nYou can ask me questions about your workout plan. Type 'exit' to finish.")
        
        while True:
            question = input("\nYour question: ").strip().lower()
            
            if question == 'exit':
                break
            
            if 'calories' in question:
                print(f"Based on your profile, you'll burn approximately {plan['calories_per_session']} calories per {plan['workout_type']} session.")
                print(f"This is influenced by your session duration ({plan['session_duration']}), heart rate, and body metrics.")
            
            elif 'workout type' in question or 'exercise type' in question:
                print(f"I've recommended {plan['workout_type']} based on your profile and fitness goals ({user_info['Goal']}).")
                print(f"This type of workout is effective for your experience level ({plan['experience_level']}) and aligns with your goals.")
            
            elif any(day.lower() in question for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]):
                # Extract the day from the question
                for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                    if day.lower() in question:
                        if day in plan['workout_days']:
                            day_plan = plan['daily_exercises'][day]
                            print(f"{day} is a workout day with focus on {day_plan['focus']}.")
                            print("Exercises for this day:")
                            for i, exercise in enumerate(day_plan['exercises'], 1):
                                print(f"{i}. {exercise}")
                            
                            # Add sets and reps recommendations
                            if plan['workout_type'] == "Strength":
                                if plan['experience_level'] == "Beginner":
                                    print("Do 2-3 sets of 10-12 reps with moderate weight.")
                                elif plan['experience_level'] == "Intermediate":
                                    print("Do 3-4 sets of 8-10 reps with challenging weight.")
                                else:  # Advanced
                                    print("Do 4-5 sets of 6-8 reps with heavy weight.")
                            elif plan['workout_type'] == "HIIT":
                                print("Format: 30 seconds work, 15 seconds rest, 3-4 rounds")
                            elif plan['workout_type'] == "Cardio":
                                print(f"Duration: {int(float(plan['session_duration'].split()[0]) * 60)} minutes at moderate intensity")
                            elif plan['workout_type'] == "Yoga":
                                print("Hold each pose for 30-60 seconds, focus on breathing")
                        else:
                            print(f"{day} is a rest day. Focus on recovery, light stretching, and staying hydrated.")
                        break
            
            elif 'exercises' in question or 'specific' in question:
                print("I've recommended specific exercises for each workout day:")
                for day in plan['workout_days']:
                    day_plan = plan['daily_exercises'][day]
                    print(f"\n{day} - {day_plan['focus']}:")
                    for i, exercise in enumerate(day_plan['exercises'], 1):
                        print(f"  {i}. {exercise}")
            
            elif 'schedule' in question or 'frequency' in question:
                print(f"I recommend working out {plan['sessions_per_week']} days per week based on your input.")
                print("Your workout days are: " + ", ".join(plan['workout_days']))
                print("Your rest days are: " + ", ".join(plan['rest_days']))
                print("It's important to include rest days to allow your body to recover and build strength.")
            
            elif 'water' in question or 'hydration' in question:
                liters = float(plan['hydration'].split()[0])
                cups = liters * 4.22675
                print(f"You should drink approximately {liters:.1f} liters ({cups:.1f} cups) of water daily.")
                print("Proper hydration is crucial for workout performance and recovery.")
            
            elif 'goal' in question:
                print(f"Your primary goal is {user_info['Goal']}.")
                print(f"The {plan['workout_type']} workout plan I've recommended is aligned with this goal.")
                
                # Add goal-specific advice
                if user_info['Goal'] == "Weight Loss":
                    print("For weight loss, focus on maintaining a calorie deficit through diet and exercise.")
                    print("The combination of cardio and strength training will help maximize fat burning.")
                elif user_info['Goal'] == "Muscle Building":
                    print("For muscle building, ensure you're consuming enough protein and calories.")
                    print("Progressive overload (gradually increasing weight) is key to muscle growth.")
                elif user_info['Goal'] == "Cardiovascular Health":
                    print("For cardiovascular health, consistency is key. Aim to keep your heart rate elevated during workouts.")
                    print("Mix high and low intensity training for optimal heart health benefits.")
                elif user_info['Goal'] == "Flexibility":
                    print("For flexibility, hold stretches for at least 30 seconds and breathe deeply.")
                    print("Consistency is more important than intensity - daily practice yields the best results.")
                elif user_info['Goal'] == "General Fitness":
                    print("For general fitness, this balanced approach will improve all aspects of your physical health.")
                    print("Consider tracking your progress to stay motivated and see improvements over time.")
            
            elif 'weight' in question:
                kg = user_info['Weight (kg)']
                lbs = kg * 2.20462
                print(f"Your weight is {kg:.1f} kg ({lbs:.1f} pounds).")
                print("This was used to calculate your BMI and determine appropriate exercise recommendations.")
            
            elif 'height' in question:
                meters = user_info['Height (m)']
                total_inches = meters / 0.0254
                feet = int(total_inches // 12)
                inches = int(total_inches % 12)
                print(f"Your height is {meters:.2f} meters ({feet}'{inches}\").")
                print("This was used to calculate your BMI and determine appropriate exercise recommendations.")
            
            elif 'bmi' in question:
                print(f"Your BMI is {user_info['BMI']:.2f}.")
                if user_info['BMI'] < 18.5:
                    print("This is considered underweight. Focus on building muscle and increasing caloric intake.")
                elif user_info['BMI'] < 25:
                    print("This is in the normal range. Your workout plan is designed to maintain and improve overall fitness.")
                elif user_info['BMI'] < 30:
                    print("This is in the overweight range. Your workout plan will help with weight management.")
                else:
                    print("This is in the obese range. Your workout plan focuses on cardiovascular health and gradual weight loss.")
            
            elif 'rest' in question:
                print(f"Your rest days are: {', '.join(plan['rest_days'])}")
                print("Rest days are crucial for muscle recovery and growth.")
                print("On rest days, you can do light activities like walking or gentle stretching.")
                print("Make sure to stay hydrated and get adequate sleep for optimal recovery.")
            
            elif 'sets' in question or 'reps' in question:
                if plan['workout_type'] == "Strength":
                    if plan['experience_level'] == "Beginner":
                        print("As a beginner, aim for 2-3 sets of 10-12 reps with moderate weight.")
                        print("Focus on proper form rather than lifting heavy weights.")
                    elif plan['experience_level'] == "Intermediate":
                        print("As an intermediate lifter, aim for 3-4 sets of 8-10 reps with challenging weight.")
                        print("You should be struggling with the last 1-2 reps of each set.")
                    else:  # Advanced
                        print("As an advanced lifter, aim for 4-5 sets of 6-8 reps with heavy weight.")
                        print("Consider periodizing your training for optimal results.")
                elif plan['workout_type'] == "HIIT":
                    print("For HIIT workouts, do each exercise for 30 seconds at maximum effort, followed by 15 seconds of rest.")
                    print("Complete 3-4 rounds of the circuit with minimal rest between rounds.")
                elif plan['workout_type'] == "Cardio":
                    print(f"For cardio workouts, maintain a moderate intensity for {int(float(plan['session_duration'].split()[0]) * 60)} minutes.")
                    print("You should be able to talk but not sing during your cardio sessions.")
                elif plan['workout_type'] == "Yoga":
                    print("For yoga, hold each pose for 30-60 seconds while focusing on your breathing.")
                    print("Move slowly between poses and listen to your body to avoid strain.")
            
            else:
                print("I'm not sure how to answer that question. You can ask about:")
                print("- Calories burned")
                print("- Workout type recommendation")
                print("- Specific exercises for each day")
                print("- Workout schedule/frequency")
                print("- Specific days (e.g., 'What's my Monday workout?')")
                print("- Sets and reps recommendations")
                print("- Rest days")
                print("- Hydration recommendations")
                print("- Your fitness goals")
                print("- Your weight and height")
                print("- Your BMI and what it means")

    def validate_numeric_range(self, value_str, min_val, max_val):
        """Validate that a string input is a number within the specified range."""
        try:
            value = float(value_str)
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Value must be between {min_val} and {max_val}. Using {min_val}.")
                return min_val
        except ValueError:
            print(f"Invalid input. Using {min_val}.")
            return min_val

if __name__ == "__main__":
    chatbot = GymChatbot()
    chatbot.run() 