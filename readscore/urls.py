from .views import *
from django.urls import path


urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('about/<int:pk>', AboutBook.as_view(), name='about'),
    path('start_read/<int:pk>', StartReading.as_view(), name='reading_start'),
    path('end_read/<int:pk>', EndReading.as_view(), name='reading_end'),

    path('api/book-set/', BookViewSet.as_view({'get': 'list'})),
    path('api/book-set/<int:pk>', BookViewSet.as_view({'get': 'retrieve'})),
]
