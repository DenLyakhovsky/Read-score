from django.contrib import admin
from .models import Book, ReadingSession, ReadingStats

# happy: 12345qwe

admin.site.register(Book)
admin.site.register(ReadingSession)
admin.site.register(ReadingStats)
