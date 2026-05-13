from django.contrib import admin
from .models import CampaignData


@admin.register(CampaignData)
class CampaignDataAdmin(admin.ModelAdmin):
    list_display = (
        "campaign_name",
        "channel",
        "date",
        # "impressions",
        # "clicks",
        # "conversions",
        # "cost",
        # "revenue",
        # "uploaded_at",
    )
    list_filter = (
        "channel",
        "date",
    )
    search_fields = (
        "campaign_name",
        "channel",
    )
