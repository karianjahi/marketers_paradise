from django.urls import path
from .views import CSVUploadAPIView

urlpatterns = [
    path("upload/", CSVUploadAPIView.as_view(), name="csv-upload"),
]

