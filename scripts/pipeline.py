# Импортируем необходимые библиотеки из ClearML для работы с пайплайнами и задачами
from clearml import PipelineDecorator, Task

# Импортируем библиотеку subprocess для выполнения команд в операционной системе
import subprocess

# Импортируем библиотеку os для работы с операционной системой, например, для управления путями или файловыми системами
import os


# Декоратор PipelineDecorator для компонента dvc_pull, который не использует кеширование
# и выполняется в очереди "default". Этот компонент будет отвечать за скачивание данных и зависимостей.
@PipelineDecorator.component(cache=False, execution_queue="default")
def dvc_pull():
    # Выполняем команду "dvc pull", которая обновляет локальную копию данных и моделей
    subprocess.run(["dvc", "pull"], check=True)

# Декоратор PipelineDecorator для компонента download_data, который не использует кеширование
# и выполняется в очереди "default". Этот компонент запускает скрипт для загрузки данных.
@PipelineDecorator.component(cache=False, execution_queue="default")
def download_data():
    # Запускаем Python-скрипт "download.py" для загрузки необходимых данных
    subprocess.run(["python", "scripts/download.py"], check=True)

# Декоратор PipelineDecorator для компонента process_data, который не использует кеширование
# и выполняется в очереди "default". Этот компонент запускает скрипт для обработки данных.
@PipelineDecorator.component(cache=False, execution_queue="default")
def process_data():
    # Запускаем Python-скрипт "process_data.py" для обработки загруженных данных
    subprocess.run(["python", "scripts/process_data.py"], check=True)


# Декоратор PipelineDecorator для компонента train_model_1, который выполняется в очереди "default".
# Этот компонент отвечает за обучение первой модели.
@PipelineDecorator.component(execution_queue="default")
def train_model_1():
    try:
        # Получаем текущую задачу с помощью метода Task.current_task()
        current_task = Task.current_task()
        
        # Если задача существует, продолжаем выполнение
        if current_task:
            # Извлекаем ID текущей задачи и выводим его в консоль для логирования
            task_id = current_task.id
            print(f"Идентификатор текущей задачи в train_model_1: {task_id}")
            
            # Инициализируем новую задачу в проекте "my_mlops_project" для обучения модели
            new_task = Task.init(project_name="my_mlops_project", task_name="train_with_clearml_1")
            
            # Запускаем задачу для выполнения удаленно на очереди 'default'
            new_task.execute_remotely(queue_name='default')  # Запуск задачи на удаленной машине/агенте

            # Логируем начало обучения модели
            print("Начинато обучение модели 1...")
            
            # Используем subprocess для выполнения скрипта "train.py", передавая параметр "--model-type" для выбора модели
            subprocess.run(["python", "scripts/train.py", "--model-type", "model_1"], check=True)

        else:
            # Если текущая задача не существует, выводим ошибку и выбрасываем исключение
            print("Current task is None in train_model_1")
            raise ValueError("Current task is None in train_model_1")
    except Exception as e:
        # Ловим исключения и выводим ошибку, если что-то пошло не так в процессе обучения
        print(f"Ошибка в компоненте train_model_1: {e}")
        raise  # Пробрасываем исключение дальше


# Декоратор PipelineDecorator для компонента train_model_2, который выполняется в очереди "default".
# Этот компонент отвечает за обучение второй модели.
@PipelineDecorator.component(execution_queue="default")
def train_model_2():
    try:
        # Получаем текущую задачу с помощью метода Task.current_task()
        current_task = Task.current_task()
        
        # Если задача существует, продолжаем выполнение
        if current_task:
            # Извлекаем ID текущей задачи и выводим его в консоль для логирования
            task_id = current_task.id
            print(f"Идентификатор текущей задачи в train_model_2: {task_id}")
            
            # Инициализируем новую задачу в проекте "my_mlops_project" для обучения второй модели
            new_task = Task.init(project_name="my_mlops_project", task_name="train_with_clearml_2")
            
            # Запускаем задачу для выполнения удаленно на очереди 'default'
            new_task.execute_remotely(queue_name='default')  # Запуск задачи на удаленной машине/агенте

            # Логируем начало обучения второй модели
            print("Начинато обучение модели 2...")
            
            # Используем subprocess для выполнения скрипта "train.py", передавая параметр "--model-type" для выбора второй модели
            subprocess.run(["python", "scripts/train.py", "--model-type", "model_2"], check=True)

        else:
            # Если текущая задача не существует, выводим ошибку и выбрасываем исключение
            print("Current task is None in train_model_2")
            raise ValueError("Current task is None in train_model_2")
    except Exception as e:
        # Ловим исключения и выводим ошибку, если что-то пошло не так в процессе обучения
        print(f"Ошибка в компоненте train_model_2: {e}")
        raise  # Пробрасываем исключение дальше

# Декоратор PipelineDecorator для компонента dvc_repro, который выполняет команду DVC "repro".
# Эта команда запускает воспроизведение состояния данных в DVC, восстанавливая нужные версии данных и зависимостей.
@PipelineDecorator.component(cache=False, execution_queue="default")
def dvc_repro():
    # Выполняем команду "dvc repro" для воспроизведения данных и состояний в DVC
    subprocess.run(["dvc", "repro"], check=True)

# Декоратор PipelineDecorator для компонента dvc_push, который выполняет команду DVC "push".
# Эта команда отправляет изменения в репозиторий DVC, обновляя удаленные хранилища данными.
@PipelineDecorator.component(cache=False, execution_queue="default")
def dvc_push():
    # Выполняем команду "dvc push" для отправки изменений в DVC хранилище
    subprocess.run(["dvc", "push"], check=True)

# Декоратор PipelineDecorator для определения пайплайна 'mlops_pipeline'.
# Указываем название пайплайна, проект и версию, чтобы управлять различными этапами работы с ClearML.
@PipelineDecorator.pipeline(
    name='mlops_pipeline',
    project='my_mlops_project',
    version='0.1'
)
def mlops_pipeline_logic():
  # Шаги пайплайна, который включает в себя несколько этапов, включая работу с DVC и обработку данных.
  dvc_pull()      # Загружаем данные с помощью DVC (pull).
  download_data()  # Скачиваем необходимые данные с использованием скрипта download.py.
  process_data()   # Обрабатываем данные с помощью скрипта process_data.py.
  train_model_1()  # Обучаем первую модель.
  train_model_2()  # Обучаем вторую модель.
  dvc_repro()      # Воспроизводим данные и зависимости с помощью DVC (repro).
  dvc_push()       # Отправляем обновленные данные в DVC хранилище (push).

# Основной блок для выполнения пайплайна на локальной машине, полезно для отладки.
# Для масштабирования, нужно будет закомментировать следующую строку и настроить очередь 'services' на ClearML.
if __name__ == '__main__':
    # Запуск пайплайна локально, используем для тестирования на текущей машине
    # Для масштабирования можно закомментировать эту строку и использовать очередь 'services' с агентом ClearML
    PipelineDecorator.run_locally()  # Запуск пайплайна локально для отладки
    mlops_pipeline_logic()  # Запуск самого пайплайна