import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
import plotly.graph_objects as go

nutritions_values = ['Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent', 'SodiumContent', 'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent']

st.header('Meal Nutrition Analysis')
st.subheader('Choose your meal composition')

breakfast_recommendations=['Oats', 'Yoghurt with fruits', 'Egg', 'Nuts, seeds and low-fat diary', 'Banana and berries', 'Beans and lentils']
lunch_recommendations=['Dal', 'Vegetable curry', 'Brown rice', 'Fish', 'Green leafy vegetables', 'Chapathi']
dinner_recommendations=['Khichdi', 'Vegetable soup', 'Fish', 'Fruit salad', 'Buttermilk', 'Ragi dosa']

# Create select boxes for meal choices
breakfast_choice, lunch_choice, dinner_choice = st.columns(3)
breakfast_choice = st.selectbox('Choose your breakfast:', breakfast_recommendations)
lunch_choice = st.selectbox('Choose your lunch:', lunch_recommendations)
dinner_choice = st.selectbox('Choose your dinner:', dinner_recommendations)

choices=[breakfast_choice,lunch_choice,dinner_choice] 

#https://www.eatthismuch.com/food/nutrition
#https://www.nutritionix.com/food
def get_nutritional_value(meal_name, nutrition_value):
    # Dictionary containing the nutritional values for each meal
    meal_nutritional_values = {
        'Oats': {'Calories': 153.5, 'FatContent': 2.6, 'SaturatedFatContent': 1.2, 'CholesterolContent': 0, 'SodiumContent': 5, 'CarbohydrateContent': 27.4, 'FiberContent': 4, 'SugarContent': 1, 'ProteinContent': 5.3},
        'Yoghurt with fruits': {'Calories': 162, 'FatContent': 2.6, 'SaturatedFatContent': 0.2, 'CholesterolContent': 5, 'SodiumContent': 1.5, 'CarbohydrateContent': 32, 'FiberContent': 0, 'SugarContent': 23, 'ProteinContent': 5.65},
        'Egg': {'Calories': 155, 'FatContent': 11, 'SaturatedFatContent': 3.3, 'CholesterolContent': 0.3, 'SodiumContent': 0.0012, 'CarbohydrateContent': 1.1, 'FiberContent': 0, 'SugarContent': 1.1, 'ProteinContent': 6},
        'Nuts, seeds and low-fat diary': {'Calories': 170, 'FatContent': 15, 'SaturatedFatContent': 3, 'CholesterolContent': 5, 'SodiumContent': 10, 'CarbohydrateContent': 6, 'FiberContent': 3, 'SugarContent': 2, 'ProteinContent': 17},
        'Banana and berries': {'Calories': 100, 'FatContent': 0.5, 'SaturatedFatContent': 0, 'CholesterolContent': 0, 'SodiumContent': 0, 'CarbohydrateContent': 22, 'FiberContent': 3, 'SugarContent': 12, 'ProteinContent': 1},
        'Beans and lentils': {'Calories': 279.7, 'FatContent': 2, 'SaturatedFatContent': 1, 'CholesterolContent': 0, 'SodiumContent': 1.6, 'CarbohydrateContent': 48, 'FiberContent': 10.1, 'SugarContent': 4, 'ProteinContent': 16},
        'Dal': {'Calories': 198, 'FatContent': 6.32, 'SaturatedFatContent': 5.3, 'CholesterolContent': 0, 'SodiumContent': 0.37, 'CarbohydrateContent': 26.18, 'FiberContent': 6, 'SugarContent': 4.5, 'ProteinContent': 10},
        'Vegetable curry': {'Calories': 188, 'FatContent': 8.8, 'SaturatedFatContent': 4.5, 'CholesterolContent': 0, 'SodiumContent': 0.311, 'CarbohydrateContent': 24, 'FiberContent': 5.5, 'SugarContent': 6.1, 'ProteinContent': 5.6},
        'Brown rice': {'Calories': 109, 'FatContent': 0.8, 'SaturatedFatContent': 0.2, 'CholesterolContent': 0, 'SodiumContent': 0, 'CarbohydrateContent': 23, 'FiberContent': 1.8, 'SugarContent': 0.4, 'ProteinContent': 2.3},
        'Fish': {'Calories': 218, 'FatContent': 4.5, 'SaturatedFatContent': 1.6, 'CholesterolContent': 0.97, 'SodiumContent': 0.1, 'CarbohydrateContent': 0, 'FiberContent': 0, 'SugarContent': 0, 'ProteinContent': 44},
        'Green leafy vegetables': {'Calories': 63, 'FatContent': 1.4, 'SaturatedFatContent': 0.1, 'CholesterolContent': 0, 'SodiumContent': 0.029, 'CarbohydrateContent': 11, 'FiberContent': 7.6, 'SugarContent': 0.8, 'ProteinContent': 5.1},
        'Chapathi': {'Calories': 241, 'FatContent': 17, 'SaturatedFatContent': 9.4, 'CholesterolContent': 0.033, 'SodiumContent': 0.128, 'CarbohydrateContent': 20, 'FiberContent': 4.2, 'SugarContent': 1.3, 'ProteinContent': 3.4},
        'Khichdi': {'Calories': 238, 'FatContent': 3.4, 'SaturatedFatContent': 1.8, 'CholesterolContent': 0, 'SodiumContent': 0.123, 'CarbohydrateContent': 41, 'FiberContent': 11, 'SugarContent': 2.9, 'ProteinContent': 11},
        'Vegetable soup': {'Calories': 159, 'FatContent': 3.8, 'SaturatedFatContent': 0.9, 'CholesterolContent': 0, 'SodiumContent': 1.219, 'CarbohydrateContent': 26, 'FiberContent': 3.4, 'SugarContent': 4, 'ProteinContent': 5.8},
        'Fruit salad': {'Calories': 97, 'FatContent': 0.5, 'SaturatedFatContent': 0.1, 'CholesterolContent': 0, 'SodiumContent': 2.6, 'CarbohydrateContent': 24, 'FiberContent': 3.3, 'SugarContent': 16, 'ProteinContent': 1.4},
        'Buttermilk': {'Calories': 98, 'FatContent': 2.2, 'SaturatedFatContent': 1.3, 'CholesterolContent': 9.8, 'SodiumContent': 0.466, 'CarbohydrateContent': 12, 'FiberContent': 0, 'SugarContent': 12, 'ProteinContent': 8.1},
        'Ragi dosa': {'Calories': 135, 'FatContent': 7.8, 'SaturatedFatContent': 1.2, 'CholesterolContent': 0, 'SodiumContent': 0, 'CarbohydrateContent': 15, 'FiberContent': 0.7, 'SugarContent': 1, 'ProteinContent': 2}
    }

    # Check if the meal_name is in the dictionary
    if meal_name in meal_nutritional_values:
        # If the meal_name is found, return the value of the specified nutrition_value
        return meal_nutritional_values[meal_name].get(nutrition_value, 0)
    else:
        # If the meal_name is not found, return 0 for the specified nutrition_value
        return 0

# Calculating the sum of nutritional values of the choosen recipes
total_nutrition_values = {nutrition_value: 0 for nutrition_value in nutritions_values}
for choice, meals_ in zip(choices, [breakfast_recommendations, lunch_recommendations, dinner_recommendations]):
    for meal in meals_:
        if meal == choice:  # Check if the meal string matches the choice
            # For each nutritional value, add the value of the chosen meal to the total
            for nutrition_value in nutritions_values:
                total_nutrition_values[nutrition_value] += get_nutritional_value(meal, nutrition_value)

st.markdown("&nbsp;", unsafe_allow_html=True)
st.markdown(f'<h5 style="text-align: center;font-family:sans-serif;">Nutritional Values:</h5>', unsafe_allow_html=True)
nutritions_graph_options = {
"tooltip": {"trigger": "item"},
"legend": {"top": "5%", "left": "center"},
"series": [
{
    "name": "Nutritional Values",
    "type": "pie",
    "radius": ["40%", "70%"],
    "avoidLabelOverlap": False,
    "itemStyle": {
        "borderRadius": 10,
        "borderColor": "#fff",
        "borderWidth": 2,
    },
    "label": {"show": False, "position": "center"},
    "emphasis": {
        "label": {"show": True, "fontSize": "40", "fontWeight": "bold"}
    },
    "labelLine": {"show": False},
    "data": [{"value":round(total_nutrition_values[total_nutrition_value]),"name":total_nutrition_value} for total_nutrition_value in total_nutrition_values],
}
],
}       
st_echarts(options=nutritions_graph_options, height="500px",)

# Creating a list of dictionaries to store the nutritional values
nutritional_table_data = []
for nutrition_value in nutritions_values:
    nutritional_table_data.append({'Nutritional Value': nutrition_value, 'Amount per serving': total_nutrition_values[nutrition_value]})

nutritional_df = pd.DataFrame(nutritional_table_data)

# Constructing the HTML table string
table_html = "<table style='margin: 0 auto;'>"
table_html += "<tr><th>Nutritional Value</th><th>Amount per serving</th></tr>"
for _, row in nutritional_df.iterrows():
    table_html += f"<tr><td>{row['Nutritional Value']}</td><td>{row['Amount per serving']}</td></tr>"
table_html += "</table>"

# Displaying the nutritional values table using st.markdown()
st.markdown(table_html, unsafe_allow_html=True)

st.markdown("&nbsp;", unsafe_allow_html=True)
st.markdown("&nbsp;", unsafe_allow_html=True)
# Allow the user to select the nutritional value for the histogram
st.subheader('Distribution of nutritional values across different meals')
selected_nutrition = st.selectbox('Nutritional value:', nutritions_values)

# Get the values for the selected nutritional value across different meals and their corresponding names
selected_meals = breakfast_recommendations + lunch_recommendations + dinner_recommendations
selected_nutrition_values = [get_nutritional_value(meal, selected_nutrition) for meal in selected_meals]

# Create a histogram using Plotly
histogram_fig = go.Figure(data=[go.Bar(x=selected_meals, y=selected_nutrition_values)])
histogram_fig.update_layout(title=f'Distribution of {selected_nutrition} Across Meals', xaxis_title='Meal', yaxis_title=selected_nutrition)
st.plotly_chart(histogram_fig, use_container_width=True)
