from django.db import models


class CampaignData(models.Model):
    date = models.DateField()
    campaign_name = models.CharField(max_length=255)
    channel = models.CharField(max_length=100)
    impressions = models.IntegerField()
    clicks = models.IntegerField()
    conversions = models.IntegerField()
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    revenue = models.DecimalField(max_digits=12, decimal_places=2)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.campaign_name} - {self.date}"
    