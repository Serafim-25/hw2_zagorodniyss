import os  # Импортируем модуль для работы с операционной системой
import argparse  # Импортируем модуль для обработки аргументов командной строки
# Импортируем логистическую регрессию для обучения модели
from sklearn.linear_model import LogisticRegression
# Импортируем функцию для разделения данных на обучающие и тестовые
from sklearn.model_selection import train_test_split
# Импортируем метрику точности для оценки модели
from sklearn.metrics import accuracy_score
# Импортируем набор данных Iris для примера
from sklearn.datasets import load_iris
import mlflow  # Импортируем MLflow для отслеживания экспериментов
from clearml import Task  # Импортируем Task из ClearML для отслеживания задач


def main():
    # Создаем парсер для аргументов командной строки
    parser = argparse.ArgumentParser(
        description="Train a logistic regression model")

    # Добавляем аргумент для указания типа модели
    parser.add_argument("--model-type", type=str,
        default="model_1", help="Type of model to train")

    # Разбираем аргументы командной строки
    args = parser.parse_args()

    # Устанавливаем трекинг URI для MLflow, указывая директорию
    # для хранения меток и моделей
    mlflow.set_tracking_uri(os.path.join(os.getcwd(), "mlruns"))

    # Загружаем набор данных Iris
    iris = load_iris()
    X, y = iris.data, iris.target

    # Разделяем данные на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # Устанавливаем параметры для модели логистической
    # регрессии в зависимости от типа модели
    if args.model_type == "model_1":
        C = 0.1  # Регуляризационный параметр для модели 1
        solver = "liblinear"  # Метод оптимизации для модели 1
    elif args.model_type == "model_2":
        C = 1.0  # Регуляризационный параметр для модели 2
        solver = "lbfgs"  # Метод оптимизации для модели 2

    # Получаем текущую задачу в ClearML (если она существует)
    task = Task.current_task()
    # Если задача не найдена, используем "local" как имя задачи
    task_name = task.name if task else "local"

    # Запускаем эксперимент в MLflow
    with mlflow.start_run(run_name=f"{task_name}-{args.model_type}"):
        # Логируем параметры модели
        mlflow.log_param("C", C)
        mlflow.log_param("solver", solver)

        # Инициализируем модель логистической
        # регрессии с выбранными параметрами
        model = LogisticRegression(C=C, solver=solver)

        # Обучаем модель
        model.fit(X_train, y_train)

        # Делаем предсказания на тестовой выборке
        y_pred = model.predict(X_test)

        # Рассчитываем точность модели
        accuracy = accuracy_score(y_test, y_pred)

        # Логируем метрику точности в MLflow
        mlflow.log_metric("accuracy", accuracy)

        # Логируем метрику точности в задаче ClearML
        if task:
            task.logger.report_scalar(
                title="Accuracy", series="Accuracy", value=accuracy)

        # Логируем модель в MLflow
        mlflow.sklearn.log_model(model, artifact_path="logistic_regression")

    # Выводим финальное сообщение о завершении обучения
    print(f"Model training completed successfully. Accuracy: {accuracy}")


if __name__ == "__main__":
    main()
