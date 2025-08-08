import streamlit as st

# Page configuration
st.set_page_config(page_title="Nutrition Calculator", layout="wide")
st.title("🍽️ Protein & Calorie Calculator")

# User input fields
st.header("Enter your details:")

age = st.number_input("Age", min_value=10, max_value=100, value=25)
gender = st.selectbox("Gender", ["Male", "Female"])
weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0)
activity_level = st.selectbox("Activity Level", [
    "Sedentary (little or no exercise)",
    "Lightly active (1-3 days/week)",
    "Moderately active (3-5 days/week)",
    "Very active (6-7 days/week)",
    "Super active (twice/day)"
])

# Activity level multipliers
activity_multipliers = {
    "Sedentary (little or no exercise)": 1.2,
    "Lightly active (1-3 days/week)": 1.375,
    "Moderately active (3-5 days/week)": 1.55,
    "Very active (6-7 days/week)": 1.725,
    "Super active (twice/day)": 1.9
}

# Function to calculate BMR using Mifflin-St Jeor formula
def calculate_bmr(weight, height, age, gender):
    if gender == "Male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

# Function to calculate daily calorie and protein needs
def calculate_needs(bmr, activity_multiplier, weight):
    calories = bmr * activity_multiplier
    protein = weight * 2.0  # 2g of protein per kg of body weight
    return calories, protein

# Button to trigger calculation
if st.button("Calculate"):
    bmr = calculate_bmr(weight, height, age, gender)
    calories, protein = calculate_needs(bmr, activity_multipliers[activity_level], weight)

    st.success("✅ Estimated Daily Needs:")
    st.write(f"🔹 Calories: {int(calories)} kcal/day")
    st.write(f"🔹 Protein: {int(protein)} grams/day")

    st.info("💡 These are general estimates. For medical or professional fitness advice, consult a specialist.")
