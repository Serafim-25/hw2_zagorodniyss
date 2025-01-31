import pandas as pd  # Для работы с данными в таблицах (DataFrame).
# Для стандартизации признаков (среднее = 0, отклонение = 1).
from sklearn.preprocessing import StandardScaler


def load_data(input_path):
    # Загружает данные из CSV файла по указанному пути
    data = pd.read_csv(input_path)
    return data


def clean_data(data):
    # Удаляет строки с пропущенными значениями
    data = data.dropna()
    return data


def scale_features(data):
    # Применяет стандартизацию к признакам (кроме колонки 'species')
    scaler_instance = StandardScaler()  # Инициализация стандартизатора
    # Выбираем все колонки, кроме последней (target)
    scaling_columns = data.columns[:-1]
    # Стандартизация данных
    data[scaling_columns] = scaler_instance.fit_transform(data[scaling_columns])
    return data


def rename_target_column(data):
    # Переименовываем колонку 'species' в 'target'
    # для дальнейшего использования в модели
    data = data.rename(columns={'species': 'target'})
    return data

def export_data(data, output_path):
    # Сохраняет обработанные данные в новый CSV файл по указанному пути
    data.to_csv(output_path, index=False)


def main(input_path, output_path):
    # Главная функция, которая выполняет все этапы обработки данных
    data = load_data(input_path)  # Загружаем исходные данные
    data = clean_data(data)         # Очищаем данные от пропусков
    data = scale_features(data)     # Стандартизируем признаки
    # Создаём колонку 'target' из 'species'
    data = rename_target_column(data)
    export_data(data, output_path)  # Сохраняем обработанные данные в файл


if __name__ == "__main__":
    # Запуск основной функции с указанием путей для входных и выходных данных
    main("data/iris_dataset.csv", "data/proc_iris_dataset.csv")
