from django.urls import path
from .views import BookListCreateView, BookRetrieveUpdateDeleteView, CustomUserCreateView


urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDeleteView.as_view(), name='book-retrieve-update-delete'),
    path('register/', CustomUserCreateView.as_view(), name='user-register'),
]