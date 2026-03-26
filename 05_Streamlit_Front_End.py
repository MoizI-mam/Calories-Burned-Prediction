import streamlit as st
import joblib
import pandas as pd

# Page Config
st.set_page_config(
    page_title="Calories Burned Prediction",
    layout="centered",
    page_icon="🔥"
)

# Load Model
model = joblib.load("06_Best_Model.pkl")
columns = joblib.load("07_Columns.pkl")

# Header

st.title("🔥 Calories Burned Prediction")
st.markdown("Developed by Moiz Imam | ML Engineer")

st.divider()

# Session States
if "step" not in st.session_state:
    st.session_state.step = 1

# Step Progress
step_labels = {
1: "Step 1: Personal Info",
2: "Step 2: Health Info",
3: "Step 3: Result"
}

progress_value = st.session_state.step / 3

st.progress(progress_value, text=step_labels[st.session_state.step])    
# Step 1
if st.session_state.step == 1:
    st.subheader("👤 Step 1: Personal Information")

    age = st.number_input("Age", 15, 60)
    height = st.number_input("Height (Foot)", 2.0, 8.0)
    weight = st.number_input("Weight (kg)", 30, 150)
    gender = st.selectbox("Gender", ["Male", "Female"])

    if st.button("➡️ Next",use_container_width=True):
        st.session_state.age = age
        st.session_state.height = height
        st.session_state.weight = weight
        st.session_state.gender = gender
        st.session_state.step = 2
        st.rerun()

# Step 2
elif st.session_state.step == 2:
    st.subheader("🏃 Step 2: Health Information")

    duration = st.number_input("Workout Duration (min)", 5, 120)
    heart_rate = st.number_input("Heart Rate", 60, 200)
    body_temp = st.number_input("Body Temperature (°C)", 35.0, 42.0)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Back",use_container_width=True):
            st.session_state.step = 1
            st.rerun()

    with col2:
        if st.button("🔥 Predict Calories",use_container_width=True):

            # Save step 2 inputs
            st.session_state.duration = duration
            st.session_state.heart_rate = heart_rate
            st.session_state.body_temp = body_temp

            # FEATURE ENGINEERING
            age = st.session_state.age
            height = st.session_state.height
            weight = st.session_state.weight
            gender = st.session_state.gender

            bmi = weight / ((height / 100) ** 2)
            gender_male = int(gender == "Male")

            # Duration Category
            if duration <= 10:
                duration_moderate = duration_active = duration_intense = 0
            elif duration <= 20:
                duration_moderate, duration_active, duration_intense = 1, 0, 0
            elif duration <= 30:
                duration_moderate, duration_active, duration_intense = 0, 1, 0
            else:
                duration_moderate, duration_active, duration_intense = 0, 0, 1

            # Body Temp Category
            if body_temp < 37:
                temp_warm = temp_hot = temp_very_hot = 0
            elif body_temp < 38:
                temp_warm, temp_hot, temp_very_hot = 1, 0, 0
            elif body_temp < 39:
                temp_warm, temp_hot, temp_very_hot = 0, 1, 0
            else:
                temp_warm, temp_hot, temp_very_hot = 0, 0, 1

            # Heart Rate Zone
            if heart_rate <= 90:
                hr_fat = hr_cardio = hr_peak = 0
            elif heart_rate <= 130:
                hr_fat, hr_cardio, hr_peak = 1, 0, 0
            elif heart_rate <= 160:
                hr_fat, hr_cardio, hr_peak = 0, 1, 0
            else:
                hr_fat, hr_cardio, hr_peak = 0, 0, 1

            # Dataframe
            input_data = pd.DataFrame([{
                'Age': age,
                'Height': height,
                'Weight': weight,
                'Duration': duration,
                'Heart_Rate': heart_rate,
                'Body_Temp': body_temp,
                'BMI': bmi,
                'Gender_male': gender_male,
                'Duration_Category_Moderate': duration_moderate,
                'Duration_Category_Active': duration_active,
                'Duration_Category_Intense': duration_intense,
                'Body_Temp_Category_Warm': temp_warm,
                'Body_Temp_Category_Hot': temp_hot,
                'Body_Temp_Category_Very Hot': temp_very_hot,
                'HR_Zone_Fat Burn': hr_fat,
                'HR_Zone_Cardio': hr_cardio,
                'HR_Zone_Peak': hr_peak
            }])

            input_data = input_data.reindex(columns=columns, fill_value=0)

            # Prediction 
            prediction = model.predict(input_data)[0]

            try:
                confidence = model.predict_proba(input_data).max() * 100
            except:
                confidence = 0

            # Save results
            st.session_state.prediction = prediction
            st.session_state.confidence = confidence

            # Move to Step 3
            st.session_state.step = 3
            st.rerun()

# Step 3
elif st.session_state.step == 3:
    st.subheader("🎯 Step 3: Prediction Result")

    st.metric("🔥 Calories Burned", f"{st.session_state.prediction:.2f}")

    st.success("Prediction completed successfully!")

    if st.button("🔄 Start Again",use_container_width=True):
        st.session_state.step = 1
        st.rerun()