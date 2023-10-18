from datetime import timedelta
from django.utils.dateparse import parse_duration
from .models import Book, ReadingStats


def format_duration(duration_str):
    # Перетворення рядка часу в об'єкт timedelta
    time_obj = timedelta(seconds=duration_str)

    # Видобування годин, хвилин та секунд з об'єкта timedelta
    hours, remainder = divmod(time_obj.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Формування рядка у форматі "HH:MM:SS"
    time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    return time_str


def reading_stats_last_7_days():
    books = Book.objects.all()

    for book in books:
        # Дістаємо час загального читання
        book_read = book.date_of_last_reading

        # Взнаєм скільки в день читав протягом тижня
        average_time = book_read / 7

        # Перетворюємо в timedelta формат
        stats = parse_duration(format_duration(average_time.total_seconds()))

        ReadingStats.objects.create(reading_for_7_days=stats)

    return True
