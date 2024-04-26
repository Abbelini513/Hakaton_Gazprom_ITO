import streamlit as st
import time
import numpy as np
import pandas as pd
from st_aggrid import AgGrid
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Task 2", page_icon="📈")

st.markdown("# Результаты предсказания")

data = pd.read_csv('facies_predictions.csv')

AgGrid(data, height=400, )
# Виджеты для фильтрации данных
st.sidebar.header('Фильтры')
selected_column = st.sidebar.selectbox('Выберите столбец для фильтрации', data.columns)
selected_value = st.sidebar.text_input(f'Введите значение для фильтрации по столбцу "{selected_column}"')

filtered_data = data[data[selected_column] == selected_value] if selected_value else data

# Отображение таблицы с отфильтрованными данными
st.subheader('Отфильтрованные данные')
st.write(filtered_data)

# Визуализация данных
st.sidebar.header('График')
selected_chart = st.selectbox('Выберите тип графика', ['Гистограмма', 'Круговая диаграмма'])

if selected_chart == 'Гистограмма':
    sns.set_style('whitegrid')
    plt.figure(figsize=(10, 6))
    sns.histplot(data=filtered_data, x=selected_column, bins=20, kde=True)
    st.pyplot()
elif selected_chart == 'Круговая диаграмма':
    plt.figure(figsize=(8, 8))
    filtered_data[selected_column].value_counts().plot.pie(autopct='%1.1f%%')
    st.pyplot()

