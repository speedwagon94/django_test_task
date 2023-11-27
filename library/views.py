import logging
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from django.db.utils import IntegrityError

from .tasks import send_welcome_email
from .models import Book
from .serializers import BookSerializer, CustomUserSerializer


logger = logging.getLogger(__name__)


class BaseView(generics.GenericAPIView):
    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        self.log_exception()
        return response

    def log_exception(self):
        logger.exception(f"{self.__class__.__name__}: Error occurred.")


class BookListCreateView(BaseView, generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        try:
            books = self.get_queryset()
            serializer = self.serializer_class(books, many=True)
            logger.info("BookListCreateView: Successfully retrieved book list.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            self.handle_exception(e)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            logger.info("BookListCreateView: Successfully created a new book.")
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            logger.warning(f"BookListCreateView: Validation error - {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.handle_exception(e)


class BookRetrieveUpdateDeleteView(BaseView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        try:
            book = self.get_object()
            serializer = self.serializer_class(book)
            logger.info(f"BookRetrieveUpdateDeleteView: Successfully retrieved details for book {book.pk}.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            self.handle_exception(e)


class CustomUserCreateView(BaseView, generics.CreateAPIView):
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.perform_create(serializer)
            send_welcome_email.delay(user.id)
            headers = self.get_success_headers(serializer.data)
            logger.info(f"CustomUserCreateView: Successfully created a new user with email {user.email}.")
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            logger.warning(f"CustomUserCreateView: Validation error - {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.handle_exception(e)


    def perform_create(self, serializer):
        try:
            return serializer.save()
        except IntegrityError as e:
            if 'unique constraint' in str(e):
                raise ValidationError("This email is already in use.")
            else:
                raise
