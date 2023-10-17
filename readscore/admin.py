from django.contrib import admin
from .models import Book, ReadingSession

# happy: 12345qwe

admin.site.register(Book)
admin.site.register(ReadingSession)
