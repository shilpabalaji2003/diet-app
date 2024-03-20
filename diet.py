import streamlit as st
import pandas as pd
from catboost import CatBoostClassifier
import joblib
import numpy as np

st.set_page_config(page_title="Diet Recommendation", page_icon="💪", layout="wide")

dish_dict=[
    {'name':'Oats', 'image':'oats.jpeg', 'description':'Oats are a fantastic addition to your diet, especially as you age. Packed with fiber, they are great for keeping your digestion in check and your heart healthy. For us seniors, enjoying about half to one cup of cooked oats a day can give our bodies the right amount of nutrition without overwhelming our systems. Plus, oats help lower cholesterol and maintain a healthy weight, keeping us feeling our best as we age. So, consider adding oats to your daily routine for a tasty and nutritious boost!'}, 

    {'name':'Yoghurt with fruits', 'image':'yoghurt.jpeg', 'description':'Yogurt with fruits is a delicious and nutritious choice for your daily diet. Combining the creamy goodness of yogurt with the natural sweetness of fruits creates a tasty treat that is packed with essential nutrients. Rich in protein, calcium, and probiotics, yogurt supports strong bones and a healthy gut. Adding fruits like berries or bananas boosts the vitamin and antioxidant content, promoting overall health. For seniors, enjoying a serving of yogurt with fruits as a snack or meal accompaniment adds a delightful burst of flavor and nutrition to your day, keeping you feeling energized and satisfied.'},

    {'name':'Egg', 'image':'egg.jpeg', 'description':'Lets talk about eggs! they are not just for breakfast anymore! These little powerhouses of nutrition are perfect for seniors looking to stay strong and healthy. With their high-quality protein and essential vitamins, eggs are like a natural multivitamin for your body. Whether you like them scrambled, fried, or poached, eggs are a delicious and versatile addition to any meal. Just crack one open and enjoy a boost of energy and vitality to fuel your day!'}, 

    {'name':'Nuts, seeds and low-fat diary', 'image':'nuts.jpeg', 'description':'Let us dive into the goodness of nuts, seeds, and low-fat dairy they are like a trifecta of health benefits! Packed with protein, healthy fats, and essential vitamins, these nutritious foods are perfect for seniors aiming for a balanced diet. Nuts and seeds provide a satisfying crunch along with heart-healthy fats, while low-fat dairy options like yogurt or cheese offer calcium for strong bones. Incorporating a mix of nuts, seeds, and low-fat dairy into your snacks or meals adds a deliciously nutritious touch that keeps you feeling satisfied and fueled throughout the day!'}, 

    {'name':'Banana and berries', 'image':'banana.jpeg', 'description':"Banana and berries are like a match made in heaven, offering a delicious and nutritious duo that seniors can enjoy for a burst of flavor and health benefits. Bananas are rich in potassium, which supports heart health and helps regulate blood pressure, while berries are packed with antioxidants and vitamins, promoting overall well-being. Together, they create a satisfying and energizing snack that's perfect for any time of day. Whether enjoyed on their own, blended into a smoothie, or added to yogurt or oatmeal, banana and berries offer a deliciously sweet and nourishing option that seniors can savor with every bite."},

    {'name':'Beans and lentils', 'image':'beans.jpeg', 'description':'Beans and lentils are like the superheroes of the food world! Packed with protein, fiber, and essential nutrients, these mighty legumes are perfect for seniors looking to boost their health. Whether you enjoy them in a hearty soup, a flavorful curry, or a zesty salad, beans and lentils provide a satisfying and nutritious punch to any meal. Plus, their low glycemic index helps maintain steady blood sugar levels, keeping you energized and satisfied for longer. So, add some beans and lentils to your plate and get ready to feel like a nutritional superhero!'}, 

    {'name':'Dal', 'image':'dal.jpeg', 'description':'Dal is a nutritional powerhouse that seniors cannot afford to miss out on! Rich in protein, fiber, and essential vitamins, dal is a versatile and delicious addition to any meal. Whether you savor it as a comforting soup, a flavorful curry, or a hearty stew, dal offers a wealth of health benefits. Its high fiber content supports digestion and helps maintain steady blood sugar levels, while its protein content helps keep muscles strong and energy levels up. So, scoop up some dal onto your plate and enjoy a nutritious boost to your day!'}, 

    {'name':'Vegetable curry', 'image':'veg_curry.jpeg', 'description':'Vegetable curry is a delightful dish that brings a burst of flavor and nutrition to your plate! Loaded with colorful veggies, aromatic spices, and hearty legumes, vegetable curry is a perfect choice for seniors aiming for a well-rounded diet. Packed with vitamins, minerals, and antioxidants, this vibrant dish supports overall health and vitality. Plus, its fiber-rich ingredients promote digestion and help keep you feeling satisfied for longer. Whether served with rice, bread, or on its own, vegetable curry is a delicious way to nourish your body and delight your taste buds!'}, 

    {'name':'Brown rice', 'image':'brown_rice.jpeg', 'description':'Brown rice is a wholesome and nutritious staple that seniors can enjoy for both its flavor and health benefits. Unlike white rice, brown rice retains its outer layer, the bran, which is rich in fiber, vitamins, and minerals. This makes brown rice an excellent choice for maintaining a healthy digestive system and regulating blood sugar levels. With its nutty flavor and chewy texture, brown rice adds depth to any meal, whether served alongside vegetables, in soups, or as a base for stir-fries. Including brown rice in your diet provides sustained energy and essential nutrients, supporting your overall well-being.'}, 

    {'name':'Fish', 'image':'fish.jpeg', 'description':'Fish is a delectable and nutritious choice that seniors can savor for its taste and health benefits. Bursting with omega-3 fatty acids, protein, and essential vitamins, fish offers a myriad of advantages for overall health. Regular consumption of fish promotes heart health by lowering cholesterol levels and reducing the risk of cardiovascular diseases. Additionally, its protein content supports muscle strength and aids in tissue repair, vital for seniors well-being. Whether grilled, baked, or steamed, incorporating fish into your diet provides a flavorful and nourishing boost, ensuring you stay vibrant and energized.'}, 

    {'name':'Green leafy vegetables', 'image':'green.jpeg', 'description':"Green leafy vegetables are like nature's multivitamin, offering a bounty of health benefits in every bite. Packed with vitamins, minerals, and antioxidants, these vibrant greens are essential for seniors aiming to maintain optimal health. Rich in fiber, they support digestive health and help regulate blood sugar levels. Additionally, their high vitamin K content promotes bone health, crucial for seniors looking to maintain strength and mobility. Whether enjoyed raw in salads, sautéed as a side dish, or blended into smoothies, green leafy vegetables are a delicious and nutritious addition to any meal, ensuring you feel vibrant and nourished."}, 

    {'name':'Chapathi', 'image':'chapathi.jpeg', 'description':'Chapathi, also known as roti or flatbread, is a versatile and nutritious staple that seniors can enjoy as a wholesome part of their diet. Made from whole wheat flour, chapathi is rich in fiber, vitamins, and minerals, providing sustained energy and promoting digestive health. Its low glycemic index makes it an excellent choice for regulating blood sugar levels, while its protein content supports muscle strength and repair. Whether paired with curries, vegetables, or lentils, chapathi adds a comforting and satisfying element to any meal, ensuring seniors feel nourished and satisfied throughout the day.'}, 

    {'name':'Khichdi', 'image':'khichdi.jpeg', 'description':"Khichdi, a comforting and nutritious dish, is a perfect choice for seniors seeking a hearty and balanced meal. Made with a blend of rice, lentils, and spices, khichdi is gentle on the stomach and easy to digest, making it ideal for seniors with sensitive digestive systems. Packed with protein, fiber, and essential nutrients, khichdi provides sustained energy and supports overall well-being. Its mild flavors and soft texture make it a soothing and comforting option, especially for those looking for a nourishing meal that's easy to prepare and enjoy. Whether served plain or accompanied by yogurt or vegetables, khichdi is a wholesome and satisfying dish that seniors can relish any time of day."}, 

    {'name':'Vegetable soup', 'image':'veg_soup.jpeg', 'description':"Vegetable soup is like a warm hug for the body and soul, especially for seniors looking for a comforting and nourishing meal. Filled with a colorful array of vegetables, herbs, and spices, vegetable soup is bursting with vitamins, minerals, and antioxidants, supporting overall health and vitality. Its hydrating broth and fiber-rich ingredients promote digestion and keep you feeling satisfied. Plus, it's easy to customize based on your preferences and dietary needs. Whether enjoyed as a light lunch, starter, or dinner option, vegetable soup is a delicious and nutritious choice that seniors can savor with every spoonful."},  

    {'name':'Fruit salad', 'image':'fruit.jpeg', 'description':"Fruit salad is like nature's dessert, offering a refreshing and nutritious treat that seniors can enjoy guilt-free. Packed with a variety of colorful fruits like berries, citrus, and melons, fruit salad is bursting with vitamins, antioxidants, and fiber, promoting overall health and well-being. Its natural sweetness satisfies cravings while providing a hydrating and refreshing snack option. Plus, it's incredibly versatile, allowing you to mix and match your favorite fruits based on what's in season or readily available. Whether enjoyed as a snack, side dish, or even dessert, fruit salad adds a burst of flavor and nutrition to any meal, ensuring seniors feel energized and satisfied."}, 

    {'name':'Buttermilk', 'image':'buttermilk.jpeg', 'description':"Buttermilk is a delightful and refreshing beverage that seniors can enjoy for its taste and health benefits. Made from cultured milk, buttermilk is rich in probiotics, which promote gut health and aid digestion, making it a great option for seniors with sensitive stomachs. Its low fat and calorie content make it a lighter alternative to regular milk, perfect for those watching their calorie intake. Additionally, buttermilk is a good source of calcium and vitamin D, essential for maintaining strong bones and overall vitality. Whether enjoyed plain or flavored with herbs and spices, buttermilk is a delicious and nutritious addition to any meal, keeping seniors feeling cool, hydrated, and satisfied."}, 

    {'name':'Ragi dosa', 'image':'ragi.jpeg', 'description':"Ragi dosa, a nutritious and flavorful dish, is a wonderful choice for seniors seeking a tasty and healthful meal option. Made from ragi flour, a nutrient-rich whole grain, ragi dosa is packed with fiber, protein, and essential minerals like calcium and iron. Its low glycemic index makes it suitable for maintaining stable blood sugar levels, while its high fiber content supports digestive health. Plus, ragi dosa is gluten-free, making it an excellent choice for seniors with gluten sensitivities or celiac disease. Whether enjoyed with chutney, sambar, or a dollop of yogurt, ragi dosa offers a delicious and satisfying way to incorporate the goodness of whole grains into your diet, ensuring seniors feel nourished and satisfied."}]

#Streamlit states initialization

if 'person' not in st.session_state:
    st.session_state.generated=False
    st.session_state.recommendations=None
    st.session_state.person=None
    st.session_state.age = None
    st.session_state.height = None
    st.session_state.weight = None
    st.session_state.gender = None
    st.session_state.activity_level = None
    st.session_state.nutritional_preference = None
    st.session_state.disease = None

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
        
        st.subheader("BREAKFAST")
        self.display_dish_card(breakfast)

        st.subheader("LUNCH")
        self.display_dish_card(lunch)

        st.subheader("DINNER")
        self.display_dish_card(dinner)
    
    def display_dish_card(self, dishes):
        for dish_name in dishes:
            for dish in dish_dict:
                if dish['name'] in dish_name:
                    st.write(f"### {dish['name']}")
                    image_col, desc_col = st.columns([1, 2])
                    with image_col:
                        st.image(dish['image'], width=300)
                    with desc_col:
                        st.markdown(f"<div style='display: flex; align-items: center; height: 300px;'>{dish['description']}</div>", unsafe_allow_html=True)
                    st.write('---')

display=Display()
title="<h1 style='text-align: center;'>Automatic Diet Recommendation</h1>"
st.markdown(title, unsafe_allow_html=True)
with st.form("recommendation_from"):
    st.write("Modify the values and click the generate button to view your diet plan")
    age = st.number_input('Age', min_value=40, max_value=100, step=1, value=st.session_state.get('age', None))
    height = st.number_input('Height (in cm)',min_value=140, max_value=200, step=1, value=st.session_state.get('height', None))
    weight = st.number_input('Weight (in kg)',min_value=30, max_value=150, step=1, value=st.session_state.get('weight', None))
    gender = st.radio('Gender',('Male','Female'), index=0 if st.session_state.get('gender', None) == 'Male' else 1)
    activity_levels = ['Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)', 'Very active (6-7 days/wk)', 'Extra active (very active & physical job)']
    activity_index = activity_levels.index(st.session_state.get('activity_level', None)) if st.session_state.get('activity_level', None) in activity_levels else 0
    activity = st.select_slider('Activity', options=activity_levels, value=st.session_state.get('activity_level', None), format_func=lambda x: x)
    nutritional_preference=st.radio('Nutritional Preference', ('Non-veg', 'Veg'), index=0 if st.session_state.get('nutritional_preference', None) == 'Non-veg' else 1)
    disease_options=["Hypertension", "Arthritis", "Diabetes", "Cardiovascular diseases", "Osteoporosis", "Alzheimer's", "Chronic Obstructive Pulmonary Disease (COPD)", 'Cancer', 'Depression and anxiety disorders', 'Visual Impairments', 'No diseases']
    disease=st.multiselect("Select the diseases you suffer from: ", disease_options, default=st.session_state.get('disease', None))
    generated=st.form_submit_button("Generate")

    if generated:
        st.session_state.age = age
        st.session_state.height = height
        st.session_state.weight = weight
        st.session_state.gender = gender
        st.session_state.activity_level = activity
        st.session_state.nutritional_preference = nutritional_preference
        st.session_state.disease = disease

        st.session_state.generated=True
        person = Person(age,height,weight,gender,activity,nutritional_preference, disease)
        with st.container():
            display.display_bmi(person)
        with st.container():
            display.display_calories(person)
        with st.spinner('Generating recommendations...this may take a few seconds'):
            breakfast, lunch, dinner = recommender.generate_recommendation(age, height, weight, gender, activity, nutritional_preference, disease)
            display.display_recommendations(breakfast, lunch, dinner)
