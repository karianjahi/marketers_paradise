from rest_framework import serializers
from .models import CampaignData

class CampaignDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignData
        fields = "__all__"

class CSVUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField