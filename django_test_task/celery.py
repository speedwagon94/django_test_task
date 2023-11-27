import os
from celery import Celery

# Установка переменной окружения для работы Django внутри Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_test_task.settings')

# Создание экземпляра Celery с явным указанием брокера
app = Celery('django_test_task')

# Загрузка конфигурации из файла settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Hello:')