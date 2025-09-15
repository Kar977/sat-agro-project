from django.urls import path
from .views import get_teryt

urlpatterns = [
    path('get-teryt/', get_teryt, name='find-teryt'),
]
