from celery import shared_task
from datetime import datetime, timedelta
from django.db.models import Sum
from .models import ReadingSession
from django.db.models import F, ExpressionWrapper, fields


@shared_task
def reading_stats_last_7_days():
    today = datetime.now()

    # Отримати дату, яка була 7 днів тому
    seven_days_ago = today - timedelta(days=7)

    # Отримати дату, яка була 30 днів тому
    thirty_days_ago = today - timedelta(days=30)

    # Отримати статистику за останні 7 днів
    last_7_days_statistics = ReadingSession.objects.filter(
        user='happy',
        start_time__gte=seven_days_ago,
        start_time__lte=today,
    ).annotate(
        reading_duration=ExpressionWrapper(F('end_time') - F('start_time'), output_field=fields.DurationField())
    ).aggregate(total_reading_time_7_days=Sum('reading_duration'))['total_reading_time_7_days']

    return last_7_days_statistics


"""
def total_reading_time_last_7_days(user):
    # Отримання поточної дати
    today = timezone.now().date()
    
    # Відніміть 7 днів від поточної дати
    seven_days_ago = today - timezone.timedelta(days=7)
    
    # Запит до бази даних для обчислення загального часу читання за останні 7 днів
    total_time_last_7_days = ReadingTime.objects.filter(user=user, date__gte=seven_days_ago, date__lte=today).aggregate(Sum('time'))['time__sum']
    
    # Перевірка, чи є значення None
    if total_time_last_7_days is None:
        total_time_last_7_days = 0.0
    
    return total_time_last_7_days
"""
