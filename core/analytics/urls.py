from django.urls import path
from .views import CSVUploadAPIView, CampaignListAPIView, CampaignDetailAPIView

urlpatterns = [
    path("upload/", CSVUploadAPIView.as_view(), name="csv-upload"),
    path("campaigns/", CampaignListAPIView.as_view(), name="campaign-list"),
    path("campaigns/<int:pk>", CampaignDetailAPIView.as_view(), name="campaign-detail"),
    
]

