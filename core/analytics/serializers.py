from rest_framework import serializers
from .models import CampaignData, CSVUploadLog

class CampaignDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignData
        fields = "__all__"

class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    
class CSVUploadLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVUploadLog
        fields = "__all__"