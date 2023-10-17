from rest_framework import serializers
from .models import Book


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        # Поля, який будуть показуватись при List ViewSet
        fields = ['id', 'title', 'author', 'created_at', 'description']


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        # Поля, який будуть показуватись при Detail ViewSet
        fields = ['id', 'title', 'author', 'created_at', 'description', 'date_of_last_reading']
