import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder  

st.set_page_config(page_title="Task 1", page_icon="📈")

st.markdown("# Task 1. Кластеризация скважин по набору кривых ГИС в пределах целевого пласта.")

# Use image
st.markdown('## Визуализация распределения среднего значения GGKP по скважинам')
st.image('diff_GGKP.png')


st.markdown('## Метод "локтя" для определения оптимального количества кластеров')
st.image('elbow.png')


st.write(
    """ Для решения данной задачи мы применили ансамблемый метод для выбора устойчивых значений кластера.

Мы использовали следующие алгоритмы кластеризации:
1. K-mean;
2. Gausinn Mixture Model;
3. Agglomerative Clustering."""
)

# Read the DataFrame from the CSV file
agg_data = pd.read_csv('agg_data.csv')

st.markdown('## Результирующая таблица')
# Use agg_data as needed




AgGrid(agg_data, height=400)



st.markdown('## Графики распределения кластеров')

import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('combined.csv')

# Создаем словарь для хранения данных
clusters_dict3 = {cluster: [] for cluster in agg_data['Cluster_agg'].unique()}

# Проходим по каждой строке в agg_data
for _, row in agg_data.iterrows():
    well = row['WELL']
    cluster = row['Cluster_agg']
    
    # Получаем все значения DEPT и GGKP для данной скважины из df
    well_data = df[df['WELL'] == well]
    well_dept_list = well_data['DEPT'].tolist()
    well_ggkp_list = well_data['GGKP'].tolist()
    
    # Создаем словарь для текущей скважины с отдельными списками для DEPT и GGKP
    well_dict = {
        'DEPT': well_dept_list,
        'GGKP': well_ggkp_list
    }
    
    # Добавляем словарь скважины в соответствующий список кластера
    clusters_dict3[cluster].append({well: well_dict})

# Функция для вычисления центроида кластера
def calculate_centroid(wells_data):
    all_depts = np.concatenate([list(data['DEPT']) for well_dict in wells_data for data in well_dict.values()])
    return np.mean(all_depts)

# Функция для сдвига DEPT к центроиду кластера
def align_to_centroid(well_data, centroid_dept_value):
    dept_diff = np.mean(well_data['DEPT']) - centroid_dept_value
    well_data['DEPT'] = [dept - dept_diff for dept in well_data['DEPT']]
    return well_data

# Функция для вычисления центроида кластера
def calculate_centroid(wells_data):
    all_depts = []
    all_ggkps = []
    for well_dict in wells_data:
        for data in well_dict.values():
            all_depts.extend(data['DEPT'])
            all_ggkps.extend(data['GGKP'])
    centroid_well = min(wells_data, key=lambda wd: np.abs(np.mean(list(wd.values())[0]['DEPT']) - np.mean(all_depts)))
    well_name = list(centroid_well.keys())[0]
    centroid_well_data = list(centroid_well.values())[0]
    return {
        'WELL': well_name,
        'DEPT': centroid_well_data['DEPT'],
        'GGKP': centroid_well_data['GGKP']
    }

# Функция для сдвига DEPT к центроиду кластера
def align_to_centroid(well_data, centroid_dept_value):
    dept_diff = np.mean(well_data['DEPT']) - centroid_dept_value
    well_data['DEPT'] = [dept - dept_diff for dept in well_data['DEPT']]
    return well_data

# Вычисляем центроиды для каждого кластера
centroids = {cluster: calculate_centroid(wells) for cluster, wells in clusters_dict3.items()}

# Создаем субплоты
num_clusters = len(clusters_dict3)
fig, axes = plt.subplots(num_clusters, 1, figsize=(7, num_clusters * 12), sharey='row')
if num_clusters == 1:
    axes = [axes]

# Проходим по каждому кластеру и строим графики
for ax, (cluster, wells_data) in zip(axes, clusters_dict3.items()):
    # Получаем данные центроида для текущего кластера
    centroid = centroids[cluster]
    # Вычисляем среднее значение DEPT для центроида
    centroid_dept_value = np.mean(centroid['DEPT'])
    
    for well_dict in wells_data:
        for well, data in well_dict.items():
            # Сдвигаем DEPT скважины к центроиду
            aligned_data = align_to_centroid(data, centroid_dept_value)            
            # Рисуем кривую GGKP скважины
            ax.plot(aligned_data['GGKP'], aligned_data['DEPT'], label=well, color='gray', alpha=0.3)

    # Рисуем центроид красным жирным цветом поверх всех остальных
    ax.plot(centroid['GGKP'], centroid['DEPT'], 'r-', linewidth=2, label=f"Centroid: {centroid['WELL']}")

    ax.set_title(f'Cluster {cluster}')
    ax.invert_yaxis()  # Для геологических данных обычно ось Y инвертируется
    ax.set_xlabel('GGKP')
    ax.set_ylabel('DEPT')
    ax.legend()

# Display the plot using Streamlit
st.pyplot(fig)