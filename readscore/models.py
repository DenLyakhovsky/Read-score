from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=150, verbose_name='title')
    author = models.CharField(max_length=150, verbose_name='author')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')
    description = models.TextField(blank=True, verbose_name='description')
    date_of_last_reading = models.DurationField(verbose_name='date_of_last_reading', default=0, blank=True)

    def get_absolute_url(self):
        return reverse('book', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.title}, {self.author}'


class ReadingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user}: {self.book}'


class ReadingStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reading_for_7_days = models.DurationField(default=0, verbose_name="reading_for_7_days")
    reading_for_30_days = models.DurationField(default=0, blank=True, verbose_name="reading_for_30_days")
