from django.urls import path
from .views import CSVUploadAPIView, CampaignListAPIView, CampaignDetailAPIView, KPIAPIView, dashboard, KPIByChannelAPIView, CampaignOptionsAPIView

urlpatterns = [
    path("api/upload/", CSVUploadAPIView.as_view(), name="csv-upload"),
    path("api/campaigns/", CampaignListAPIView.as_view(), name="campaign-list"),
    path("api/campaigns/<int:pk>/", CampaignDetailAPIView.as_view(), name="campaign-detail"),
    path("api/kpis/", KPIAPIView.as_view(), name="kpi-summary"),
    path("", dashboard, name="dashboard"),
    path("api/kpis/by-channel/", KPIByChannelAPIView.as_view(), name="kpis-by-channel"),
    path("api/campaign-options/", CampaignOptionsAPIView.as_view(), name="campaign-options"),
    
]

