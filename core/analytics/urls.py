from django.urls import path
from .views import CSVUploadAPIView, CampaignListAPIView, CampaignDetailAPIView, KPIAPIView

urlpatterns = [
    path("api/upload/", CSVUploadAPIView.as_view(), name="csv-upload"),
    path("api/campaigns/", CampaignListAPIView.as_view(), name="campaign-list"),
    path("api/campaigns/<int:pk>", CampaignDetailAPIView.as_view(), name="campaign-detail"),
    path("api/kpis/", KPIAPIView.as_view(), name="kpi-summary"),
]

