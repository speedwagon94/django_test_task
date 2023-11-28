from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

# Функция для отправки писем
@shared_task
def send_welcome_email(user_id):
    try:
        user = get_user_model().objects.get(pk=user_id)
        subject = 'Добро пожаловать!'
        message = f'Привет, {user.username}! Спасибо за регистрацию.'
        from_email = 'test@example.com'
        to_email = [user.email]
        send_mail(subject, message, from_email, to_email)
        print(f"Приветственное письмо отправлено пользователю {user.username} на адрес {user.email}")
    except get_user_model().DoesNotExist:
        print(f"Пользователь с id {user_id} не найден")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
