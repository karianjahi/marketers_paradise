from rest_framework import serializers
from .models import CampaignData

class CampaignDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignData
        fields = "__all__"
        