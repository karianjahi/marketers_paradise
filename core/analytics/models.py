from django.db import models
from datetime import datetime

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
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = [
                    "campaign_name",
                    "date",
                    "channel",
                    "impressions",
                    "clicks",
                    "conversions",
                    "cost",
                    "revenue",
                ],
                name="unique_campaign_record"
            )
        ]
    
    def __str__(self):
        return f"{self.campaign_name} conducted on {self.date}"


class CSVUploadLog(models.Model):
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    total_rows = models.PositiveIntegerField(default=0)
    created_rows = models.PositiveIntegerField(default=0)
    skipped_rows = models.PositiveIntegerField(default=0)
    invalid_rows = models.PositiveBigIntegerField(default=0)
    upload_success= models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"'{self.filename}' uploaded on {datetime.strftime(self.uploaded_at, "%b %d %Y at %H:%M")}"
    
    