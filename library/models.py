from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Book(models.Model):
    # Модель для создания книги
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    year = models.IntegerField()
    isbn = models.CharField(max_length=13)

    def __str__(self):
        return self.title


class CustomUserManager(BaseUserManager):
    # Создаeт и сохраняет пользователя с указанным электронным адресом, именем пользователя и паролем.
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    # Модель пользователя с электронным адресом в качестве уникального идентификатора.
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

