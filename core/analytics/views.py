import pandas as pd

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import CSVUploadSerializer
from .models import CampaignData

REQUIRED_COLUMNS = [
    "date",
    "campaign_name",
    "channel",
    "impressions",
    "clicks",
    "conversions",
    "cost",
    "revenue",
]

class CSVUploadAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CSVUploadSerializer
    def post(self, request):
        csv_file = request.get("file")
        
        if not csv_file:
            return Response(
                {
                    "error": "No file was uploaded. Please upload a csv file"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            df = pd.read_csv(csv_file)
            missing_columns = [
                column for column in REQUIRED_COLUMNS if column not in df.columns
            ]
            if missing_columns:
                return Response(
                    {
                        "error": "Missing required columns",
                        "missing_columns": missing_columns,
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            created_count = 0
            for _, row in df.iterrows():
                CampaignData.object.create(
                    date = row["date"],
                    campaign_name = row["campaign_name"],
                    channel = row["channel"],
                    impressions = row["impressions"],
                    clicks = row["clicks"],
                    conversions = row["conversions"],
                    cost = row["cost"],
                    revenue = row["revenue"],
                )
                created_count += 1
            return Response(
                {
                    "message": "CSV uploaded successfully.",
                    "records_created": created_count,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as error:
            
            return Response(
                {
                    "error": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
