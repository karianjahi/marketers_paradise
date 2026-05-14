from django.urls import path
from .views import CSVUploadAPIView, CampaignListAPIView, CampaignDetailAPIView, KPIAPIView

urlpatterns = [
    path("upload/", CSVUploadAPIView.as_view(), name="csv-upload"),
    path("campaigns/", CampaignListAPIView.as_view(), name="campaign-list"),
    path("campaigns/<int:pk>", CampaignDetailAPIView.as_view(), name="campaign-detail"),
    path("kpis/", KPIAPIView.as_view(), name="kpi-summary"),
]

