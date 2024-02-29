import streamlit as st
import pandas as pd
from catboost import CatBoostClassifier
import time
import joblib
import numpy as np

st.set_page_config(page_title="Diet Recommendation", page_icon="💪", layout="wide")

#Streamlit states initialization

if 'person' not in st.session_state:
    st.session_state.generated=False
    st.session_state.recommendations=None
    st.session_state.person=None

class Person:
    def __init__(self, age, height, weight, gender, activity_level, nutritional_preference, disease):
        self.age=age
        self.height=height
        self.weight=weight
        self.gender=gender
        self.activity_level=activity_level
        self.nutritional_preference=nutritional_preference
        self.disease=disease
    
    def calculate_bmi(self,):
        bmi=round(self.weight/((self.height/100)**2), 2)
        return bmi
    
    def display_result(self,):
        bmi=self.calculate_bmi()
        bmi_string=f'{bmi} kg/m²'
        if bmi<18.5:
            category='Underweight'
            color='Red'
        elif 18.5<=bmi<25:
            category='Normal'
            color='Green'
        elif 25<=bmi<30:
            category='Overweight'
            color='Yellow'
        else:
            category='Obesity'    
            color='Red'
        return bmi_string,category,color
    
    def calculate_bmr(self):
        if self.gender=='Male':
            bmr=10*self.weight+6.25*self.height-5*self.age+5
        else:
            bmr=10*self.weight+6.25*self.height-5*self.age-161
        return bmr
    
    #https://www.diabetes.co.uk/bmr-calculator.html
    def calories_calculator(self):
        activites=['Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)', 'Very active (6-7 days/wk)', 'Extra active (very active & physical job)']
        weights=[1.2,1.375,1.55,1.725,1.9]
        weight = weights[activites.index(self.activity_level)]
        maintain_calories = self.calculate_bmr()*weight
        return maintain_calories

class RecommendationGenerator:
    def __init__(self):
        self.load_models()

    def load_models(self):
        # Load or train models if not already loaded
        self.clf_breakfast = self.load_model('clf_breakfast.joblib')
        self.clf_lunch = self.load_model('clf_lunch.joblib')
        self.clf_dinner = self.load_model('clf_dinner.joblib')

    def load_model(self, filename):
        try:
            return joblib.load(filename)
        except FileNotFoundError:
            # Train the model if the file is not found
            df = pd.read_csv("C:/Users/Shilpa/OneDrive - GEMS Education/Desktop/Mini project/Mini project source code/Streamlit Frontend/pages/main1_modified.csv")
            X = df[['Age', 'Height (in cm)', 'Weight (in kg)', 'Gender', 'Activity level', 'Nutritional preference', 'Disease']]
            y_breakfast = df['Breakfast']
            y_lunch = df['Lunch']
            y_dinner = df['Dinner']

            clf = CatBoostClassifier(iterations=100, cat_features=['Gender', 'Activity level', 'Nutritional preference', 'Disease'])
            if filename == 'clf_breakfast.joblib':
                clf.fit(X, y_breakfast)
            elif filename == 'clf_lunch.joblib':
                clf.fit(X, y_lunch)
            elif filename == 'clf_dinner.joblib':
                clf.fit(X, y_dinner)

            joblib.dump(clf, filename)
            return clf
        
    #71, 166, 55, Female, Light excercise, Veg, diabetes
    def generate_recommendation(self, age, height, weight, gender, activity_level, nutritional_preference, disease):
        diseases_str = ', '.join(disease)

        user_input = pd.DataFrame({
            'Age': age,
            'Height (in cm)': height,
            'Weight (in kg)': weight,
            'Gender': gender,
            'Activity level': activity_level,
            'Nutritional preference': nutritional_preference,
            'Disease': diseases_str
        }, index=[0])

        prediction_breakfast = self.clf_breakfast.predict(user_input)[0]
        prediction_lunch = self.clf_lunch.predict(user_input)[0]
        prediction_dinner = self.clf_dinner.predict(user_input)[0]

        if nutritional_preference=='Veg':
            prediction_lunch_str = ', '.join(prediction_lunch)
            prediction_breakfast_str=','.join(prediction_breakfast)
            prediction_dinner_str=','.join(prediction_dinner)

            breakfast_options=prediction_breakfast_str.split(',')
            if 'Egg' in breakfast_options:
                breakfast_options[breakfast_options.index('Egg')] = 'Beans and Lentils'
                prediction_breakfast_str = ', '.join(breakfast_options)
                prediction_breakfast_orig = np.array(breakfast_options)
            else:
                prediction_breakfast_orig=prediction_breakfast

            lunch_options = prediction_lunch_str.split(', ')
            if 'Fish' in lunch_options:
                lunch_options[lunch_options.index('Fish')] = 'Chapathi'
                prediction_lunch_str = ', '.join(lunch_options)
                prediction_lunch_orig = np.array(lunch_options)
            else:
                prediction_lunch_orig=prediction_lunch

            dinner_options = prediction_dinner_str.split(', ')
            if 'Fish' in dinner_options:
                dinner_options[dinner_options.index('Fish')] = 'Ragi Dosa'
                prediction_dinner_str = ', '.join(dinner_options)
                prediction_dinner_orig = np.array(dinner_options)
            else:
                prediction_dinner_orig=prediction_dinner

        
            return prediction_breakfast_orig, prediction_lunch_orig, prediction_dinner_orig
        
        return prediction_breakfast, prediction_lunch, prediction_dinner

recommender = RecommendationGenerator()

class Display:
    def display_bmi(self, person):
        st.header('BMI CALCULATOR')
        bmi_string,category,color = person.display_result()
        st.metric(label="Body Mass Index (BMI)", value=bmi_string)
        new_title = f'<p style="font-family:sans-serif; color:{color}; font-size: 25px;">{category}</p>'
        st.markdown(new_title, unsafe_allow_html=True)
        st.markdown(
            """
            Healthy BMI range: 18.5 kg/m² - 25 kg/m².
            """)
        
    def display_calories(self, person):
        st.header("CALORIES CALCULATOR")
        maintain_calories=person.calories_calculator()
        st.write('The result shows the amount of daily calorie estimate that can be used as a guideline for how many calories to consume each day to maintain good health')
        st.metric(label="Optimum calorie", value=f'{round(maintain_calories)} Calories/day')

    def display_recommendations(self, breakfast, lunch, dinner):
        st.header("RECOMMENDATIONS")
        with st.spinner('Generating recommendations...'):
            st.text("")
            # Add a delay to ensure the spinner is displayed
            time.sleep(1)
            st.subheader("Breakfast Recommendation")
            st.info(f"🍳 **Breakfast**: {', '.join(breakfast)}")

            st.subheader("Lunch Recommendation")
            st.info(f"🥗 **Lunch**: {', '.join(lunch)}")

            st.subheader("Dinner Recommendation")
            st.info(f"🍲 **Dinner**: {', '.join(dinner)}")

display=Display()
title="<h1 style='text-align: center;'>Automatic Diet Recommendation</h1>"
st.markdown(title, unsafe_allow_html=True)
with st.form("recommendation_from"):
    st.write("Modify the values and click the generate button to view your diet plan")
    age=st.number_input('Age', min_value=40, max_value=100, step=1)
    height = st.number_input('Height (in cm)',min_value=140, max_value=200, step=1)
    weight = st.number_input('Weight (in kg)',min_value=30, max_value=150, step=1)
    gender = st.radio('Gender',('Male','Female'))
    activity = st.select_slider('Activity',options=['Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)', 'Very active (6-7 days/wk)', 
    'Extra active (very active & physical job)'])
    nutritional_preference=st.radio('Nutritional Preference', ('Non-veg', 'Veg'))
    disease_options=["Hypertension", "Arthritis", "Diabetes", "Cardiovascular diseases", "Osteoporosis", "Alzheimer's", "Chronic Obstructive Pulmonary Disease (COPD)", 'Cancer', 'Depression and anxiety disorders', 'Visual Impairments', 'No diseases']
    disease=st.multiselect("Select the diseases you suffer from: ", disease_options)
    generated=st.form_submit_button("Generate")

    if generated:
        st.session_state.generated=True
        person = Person(age,height,weight,gender,activity,nutritional_preference, disease)
        with st.container():
            display.display_bmi(person)
        with st.container():
            display.display_calories(person)
        with st.spinner('Generating recommendations...this may take a few seconds'):
            breakfast, lunch, dinner = recommender.generate_recommendation(age, height, weight, gender, activity, nutritional_preference, disease)
            st.write("Recommendations:")
            display.display_recommendations(breakfast, lunch, dinner)
