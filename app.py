import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Personalized Meal Planner", page_icon="🥗", layout="centered")

# -------------------------------
# TITLE
# -------------------------------
st.title("🥗 Personalized Meal Plan & Progress Tracker")
st.write("Generate your custom meal plan and track your health goals over time!")

# -------------------------------
# USER INPUT SECTION
# -------------------------------
st.header("👤 Personal Information")

col1, col2 = st.columns(2)
with col1:
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=60.0)
    age = st.number_input("Age (years)", min_value=10, max_value=100, value=25)
with col2:
    height = st.number_input("Height (cm)", min_value=120.0, max_value=220.0, value=165.0)
    gender = st.selectbox("Gender", ["Female", "Male"])

goal = st.selectbox("🎯 Goal", ["Lose Weight", "Gain Weight", "Maintain Healthy Lifestyle"])

st.header("⚕️ Health Conditions / Intolerances")
conditions = st.multiselect(
    "Select any that apply:",
    [
        "Diabetes",
        "Hypertension",
        "Lactose Intolerance",
        "Gluten Intolerance",
        "PCOS/PCOD",
        "High Cholesterol",
        "None"
    ]
)

# -------------------------------
# BMI CALCULATION
# -------------------------------
height_m = height / 100
bmi = weight / (height_m ** 2)

if bmi < 18.5:
    bmi_status = "Underweight"
elif 18.5 <= bmi < 24.9:
    bmi_status = "Normal weight"
elif 25 <= bmi < 29.9:
    bmi_status = "Overweight"
else:
    bmi_status = "Obese"

st.markdown("---")
st.subheader("📊 Body Mass Index (BMI)")
st.write(f"**BMI:** {bmi:.1f} ({bmi_status})")

# -------------------------------
# CALORIE ESTIMATION (Mifflin–St Jeor)
# -------------------------------
if gender == "Male":
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
else:
    bmr = 10 * weight + 6.25 * height - 5 * age - 161

# Assume light activity (1.2x)
calories_needed = bmr * 1.2

if goal == "Lose Weight":
    calories_needed -= 400
elif goal == "Gain Weight":
    calories_needed += 400

st.subheader("🔥 Estimated Daily Calorie Requirement")
st.write(f"**{calories_needed:.0f} kcal/day**")

# -------------------------------
# MEAL PLAN SUGGESTIONS
# -------------------------------
st.markdown("---")
st.header("🍽️ Personalized Meal Plan Suggestion")

meals = {
    "Breakfast": [
        "Oatmeal with fruits",
        "Boiled eggs with brown bread",
        "Greek yogurt with nuts and honey"
    ],
    "Lunch": [
        "Grilled chicken with brown rice",
        "Vegetable salad with olive oil dressing",
        "Lentil soup with whole wheat bread"
    ],
    "Dinner": [
        "Baked fish with vegetables",
        "Stir-fried tofu with rice",
        "Vegetable curry with roti"
    ],
    "Snacks": [
        "Mixed nuts",
        "Fruit smoothie",
        "Roasted chickpeas"
    ]
}

# Adjust meals for intolerances
if "Lactose Intolerance" in conditions:
    meals["Breakfast"] = [m for m in meals["Breakfast"] if "yogurt" not in m]
if "Gluten Intolerance" in conditions:
    for key in meals:
        meals[key] = [m for m in meals[key] if "bread" not in m and "roti" not in m]
if "Diabetes" in conditions:
    meals["Snacks"] = ["Boiled egg", "Apple slices with peanut butter", "Vegetable sticks with hummus"]

meal_plan = pd.DataFrame({
    "Meal": ["Breakfast", "Lunch", "Dinner", "Snacks"],
    "Calories (approx)": [
        round(calories_needed * 0.25),
        round(calories_needed * 0.35),
        round(calories_needed * 0.30),
        round(calories_needed * 0.10)
    ],
    "Suggestions": [
        ", ".join(meals["Breakfast"]),
        ", ".join(meals["Lunch"]),
        ", ".join(meals["Dinner"]),
        ", ".join(meals["Snacks"])
    ]
})

st.table(meal_plan)

# -------------------------------
# PROGRESS TRACKER
# -------------------------------
st.markdown("---")
st.header("📅 Progress Tracker")

st.write("Log your current weight and track your progress over time!")

# Initialize session state
if "progress" not in st.session_state:
    st.session_state.progress = pd.DataFrame(columns=["Date", "Weight (kg)", "BMI"])

# Input form
with st.form("progress_form"):
    log_date = st.date_input("Select Date", date.today())
    log_weight = st.number_input("Enter Current Weight (kg)", min_value=30.0, max_value=200.0, value=weight)
    submitted = st.form_submit_button("Add Entry")
    if submitted:
        log_bmi = log_weight / (height_m ** 2)
        new_entry = pd.DataFrame({
            "Date": [log_date],
            "Weight (kg)": [log_weight],
            "BMI": [round(log_bmi, 1)]
        })
        st.session_state.progress = pd.concat([st.session_state.progress, new_entry], ignore_index=True)
        st.success("✅ Entry added successfully!")

# Display log
if not st.session_state.progress.empty:
    st.subheader("📈 Your Progress History")
    st.dataframe(st.session_state.progress)

    st.line_chart(st.session_state.progress.set_index("Date")[["Weight (kg)", "BMI"]])
else:
    st.info("No progress data yet — add your first entry above!")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.caption("Made with ❤️ using Streamlit | Personalized Meal Planner by Fizzah")
