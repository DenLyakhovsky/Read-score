from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .forms import StartReadingSessionForm, EndReadingSessionForm
from .models import Book, ReadingSession
from .serializers import BookListSerializer, BookDetailSerializer
from django.utils.dateparse import parse_duration
from .tasks import reading_stats_last_7_days


class BookViewSet(viewsets.ViewSet):
    """
    Клас, який створює RestApi сторінку з усіма книгами та по ID
    """

    permission_classes = [AllowAny]

    def list(self, request):
        queryset = Book.objects.all()
        serializer = BookListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Book.objects.all()
        book = get_object_or_404(queryset, pk=pk)
        serializer = BookDetailSerializer(book)
        return Response(serializer.data)


class HomePage(ListView):
    """
    Клас, який створює сторінку з усіма книгами
    """

    reading_stats_last_7_days.delay()

    model = Book
    template_name = 'readscore/home_page.html'
    context_object_name = 'book'


class AboutBook(DetailView):
    """
    Клас, який створює сторінку з деталями книги
    """

    model = Book
    template_name = 'readscore/info_book_page.html'
    context_object_name = 'about_book'


class StartReading(View):
    """
    Клас, яка починає відлік читання
    """

    template_name = 'readscore/start_reading.html'
    form_class = StartReadingSessionForm

    # Знаходить книгу по pk
    def get(self, request, pk):
        book = Book.objects.get(pk=pk)

        # Записує початок читання в БД та зберігає
        start_time = timezone.now()
        reading_session = ReadingSession(user=request.user, book=book, start_time=start_time)
        reading_session.save()

        # Одразу перенаправляє на EndReading
        return redirect('reading_end', pk=book.pk)


def seconds_to_hhmmss(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


class EndReading(View):
    """
    Клас, який закінчує час відліку, розраховує час та додає в БД
    """

    template_name = 'readscore/end_reading.html'
    form_class = EndReadingSessionForm

    # Знаходить книгу по pk
    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        form = self.form_class
        return render(request, self.template_name, {'form': form, 'book': book})

    def post(self, request, pk):
        book = Book.objects.get(pk=pk)
        form = self.form_class(request.POST)

        if form.is_valid():
            # Записує кінцеву дату читання
            end_time = timezone.now()
            reading_session = ReadingSession.objects.filter(user=request.user, book=book, end_time__isnull=True).first()

            if reading_session:
                reading_session.end_time = end_time
                reading_session.save()

                # Визначає кінцевий час
                reading_sessions = ReadingSession.objects.filter(book=book)
                total_reading_time = sum(
                    (session.end_time - session.start_time).total_seconds() for session in reading_sessions)

                total = parse_duration(seconds_to_hhmmss(int(total_reading_time)))

                # Додає кінцевий час у секундах до БД та зберігає
                book.date_of_last_reading = total
                book.save()

            return redirect('about', pk=book.pk)
        return render(request, self.template_name, {'form': form, 'book': book})
