import streamlit as st
import pandas as pd
from random import uniform as rnd
from streamlit_echarts import st_echarts
import pandas as pd
from catboost import CatBoostClassifier
import numpy as np
import time
import base64

st.set_page_config(page_title="Diet Recommendation", page_icon="💪", layout="wide")

nutritions_values=['Calories','FatContent','SaturatedFatContent','CholesterolContent','SodiumContent','CarbohydrateContent','FiberContent','SugarContent','ProteinContent']

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

    def generate_recommendation(self):
        # Load dataset
        df = pd.read_csv(r'C:\Users\Shilpa\OneDrive - GEMS Education\Desktop\Mini project\Mini project source code\Streamlit Frontend\pages\main.csv')

        X = df[['Age', 'Height (in cm)', 'Weight (in kg)', 'Gender', 'Activity level', 'Nutritional preference', 'Disease']]
        y_breakfast = df['Breakfast']
        y_lunch = df['Lunch']
        y_dinner = df['Dinner']

        clf_breakfast = CatBoostClassifier(iterations=100, cat_features=['Gender', 'Activity level', 'Nutritional preference', 'Disease'])
        clf_lunch = CatBoostClassifier(iterations=100, cat_features=['Gender', 'Activity level', 'Nutritional preference', 'Disease'])
        clf_dinner = CatBoostClassifier(iterations=100, cat_features=['Gender', 'Activity level', 'Nutritional preference', 'Disease'])

        clf_breakfast.fit(X, y_breakfast)
        clf_lunch.fit(X, y_lunch)
        clf_dinner.fit(X, y_dinner)

        diseases_str = ', '.join(self.disease)

        user_input = pd.DataFrame({
        'Age': self.age,
        'Height (in cm)': self.height,
        'Weight (in kg)': self.weight,
        'Gender': self.gender,
        'Activity level': self.activity_level,
        'Nutritional preference': self.nutritional_preference,
        'Disease': diseases_str
        }, index=[0])


        prediction_breakfast = clf_breakfast.predict(user_input)[0]
        prediction_lunch = clf_lunch.predict(user_input)[0]
        prediction_dinner = clf_dinner.predict(user_input)[0]
        
        if self.nutritional_preference == 'Veg':
            replacements = {
                'Breakfast': {'Egg': 'Oats'},
                'Lunch': {'Fish': 'Vegetable curry'},
                'Dinner': {'Fish': 'Vegetable soup'}
            }

            for meal in ['Breakfast', 'Lunch', 'Dinner']:
                for item, replacement in replacements.get(meal, {}).items():
                    if item in locals()[f'prediction_{meal.lower()}']:
                        idx = np.where(locals()[f'prediction_{meal.lower()}'] == item)
                        locals()[f'prediction_{meal.lower()}'][idx] = replacement

        return prediction_breakfast, prediction_lunch, prediction_dinner
    
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
            breakfast, lunch, dinner = person.generate_recommendation()
            display.display_recommendations(breakfast, lunch, dinner)
