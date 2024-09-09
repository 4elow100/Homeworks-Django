from django.urls import path
from .views import SensorListView, SensorDetailView, MeasurementCreate

urlpatterns = [
    path('sensors/', SensorListView.as_view()),
    path('sensors/<pk>/', SensorDetailView.as_view()),
    path('measurements/', MeasurementCreate.as_view()),
]
