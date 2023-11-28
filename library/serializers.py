from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Book


# Сериализатор для модели Book
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


# Сериализатор для пользовательской модели пользователя
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    # Метод create переопределен для создания пользователя
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user