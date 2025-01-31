import os  # Импортируем модуль для работы с операционной системой
import pandas as pd  # Импортируем pandas для работы с данными в формате DataFrame
from sklearn.datasets import (
    load_iris,
)  # Импортируем функцию для загрузки набора данных iris_data из sklearn


def download_data(output_path):
    # Функция для загрузки набора данных iris_data и сохранения его в формате CSV
    # output_path — это путь, по которому будет сохранен CSV файл

    # Загружаем набор данных iris_data с помощью sklearn
    iris_data = load_iris()  # Загрузка набора данных iris_data

    # Преобразуем данные в pandas DataFrame для удобной работы
    iris_df = pd.DataFrame(
        data=iris_data.data, columns=iris_data.feature_names
    )  # Создаем DataFrame с данными признаков (features)

    # Добавляем столбец 'species' с целевыми метками (классами)
    iris_df["species"] = (
        iris_data.target
    )  # Добавляем столбец 'species' с целевыми метками, представляющими виды

    # Сохраняем DataFrame в CSV файл по указанному пути
    iris_df.to_csv(output_path, index=False)  # Сохраняем в CSV, без индекса

    # Выводим сообщение, что данные успешно загружены
    print("Данные были загружены")  # Подтверждение загрузки данных


# Загружаем и сохраняем данные в файл 'data/iris_dataset.csv'
download_data(
    "data/iris_dataset.csv"
)  # Вызываем функцию для загрузки данных и их сохранения
