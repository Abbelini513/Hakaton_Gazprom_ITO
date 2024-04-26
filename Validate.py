import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from st_aggrid import AgGrid

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Команда №1. MICE 👋")

st.markdown(
    """
    ## Валидация данных
"""
)

combined = pd.read_csv('combined.csv')

def plot_well_data(wells):
    """
    Функция построения каротажной кривой для выбранных скважин.

    :param wells: список выбранных скважин
    :return: None
    """
    # Определяем количество скважин для построения соответствующего количества подграфиков
    num_wells = len(wells)

    # Создаем подграфик с нужным количеством осей
    fig, axes = plt.subplots(nrows=1, ncols=num_wells, figsize=(4 * num_wells, 12))

    # Если ключ всего один, оборачиваем axes в список
    if num_wells == 1:
        axes = [axes]

    # Код для построения графика для каждой скважины
    for idx, well in enumerate(wells):
        # Фильтруем данные для каждой скважины
        well_data = combined[combined['WELL'] == well]

        # Получаем данные для ggkp, dept, neu
        ggkp = well_data['GGKP']
        dept = well_data['DEPT']
        neu = well_data['NEU']

        # Определяем текущую ось
        ax1 = axes[idx]

        # Первый график для GGKP
        color = 'tab:red'
        ax1.set_xlabel("GGKP", color=color)
        ax1.plot(ggkp, dept, color=color, label='GGKP')
        ax1.invert_yaxis() # Убедимся, что глубина увеличивается вниз
        ax1.tick_params(axis='x', colors=color, labelbottom=True) # Отображаем метки на оси X

        # Создаем вторую ось X для NEU
        ax2 = ax1.twiny()
        color = 'tab:blue'
        ax2.set_xlabel("NEU, m3/m3", color=color)
        ax2.plot(neu, dept, color=color, label='NEU')
        ax2.tick_params(axis='x', colors=color, labeltop=True) # Отображаем метки на верхней оси X

        # Отключаем метки на оси Y для всех графиков
        ax1.tick_params(labelleft=False)
        ax1.set_yticklabels([]) # Полностью убираем метки с оси Y
        ax1.grid(True) # Включаем сетку для лучшей читаемости графика

    # Автоматическая корректировка расположения подписей
    fig.tight_layout()

    # Используем st.pyplot для отображения графика в Streamlit
    st.pyplot(fig)


# Теперь интегрируем это в Streamlit сайдбар
with st.sidebar:
    st.title('Вывод каротажной кривой')
    wells = list(combined.WELL.unique())
    selected_wells = st.multiselect('Выберите скважины', wells, default=wells[-1])

# При изменении выбора скважин, обновляем графики
if st.button('Показать графики'):
    plot_well_data(selected_wells)