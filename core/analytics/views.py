from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from django.db import IntegrityError
from django.db.models import Sum
from django.shortcuts import render
from django.http import HttpResponse

import csv


from .serializers import (
    CSVUploadSerializer,
    CSVUploadLogSerializer,
    CampaignDataSerializer,
)
from .models import CampaignData, CSVUploadLog

from analytics import utils

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
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        csv_file = serializer.validated_data["file"]

        filename = csv_file.name
        total_rows = 0
        created_rows = 0
        skipped_rows = 0
        invalid_rows = 0

        try:
            df = utils.read_csv(csv_file)
            total_rows = len(df)
            missing_columns = utils.get_missing_columns(df, REQUIRED_COLUMNS)
            if missing_columns:
                CSVUploadLog.objects.create(
                    filename=filename,
                    total_rows=total_rows,
                    created_rows=0,
                    skipped_rows=0,
                    invalid_rows=total_rows,
                    upload_success=False,
                    error_message=f"Missing columns: {missing_columns}",
                )
                return Response(
                    {
                        "error": "Missing required columns",
                        "missing_columns": missing_columns,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            for _, row in df.iterrows():
                try:
                    if not utils.is_row_valid(row, REQUIRED_COLUMNS):
                        invalid_rows += 1
                        continue
                    CampaignData.objects.create(
                        date=row["date"],
                        campaign_name=row["campaign_name"],
                        channel=row["channel"],
                        impressions=int(row["impressions"]),
                        clicks=int(row["clicks"]),
                        conversions=int(row["conversions"]),
                        cost=row["cost"],
                        revenue=row["revenue"],
                    )

                    created_rows += 1

                except IntegrityError:
                    skipped_rows += 1

                except Exception:
                    invalid_rows += 1
            upload_success = created_rows > 0 or skipped_rows > 0

            upload_log = CSVUploadLog.objects.create(
                filename=filename,
                total_rows=total_rows,
                created_rows=created_rows,
                skipped_rows=skipped_rows,
                invalid_rows=invalid_rows,
                upload_success=upload_success,
                error_message=(
                    None if upload_success else "No valid rows were uploaded."
                ),
            )
            return Response(
                {
                    "message": "CSV processed.",
                    "uploaded_log_id": upload_log.id,
                    "filename": filename,
                    "total_rows": total_rows,
                    "created_rows": created_rows,
                    "skipped_rows": skipped_rows,
                    "invalid_rows": invalid_rows,
                    "upload_success": upload_success,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as error:
            CSVUploadLog.objects.create(
                filename=filename,
                total_rows=total_rows,
                created_rows=created_rows,
                skipped_rows=skipped_rows,
                invalid_rows=invalid_rows,
                upload_success=upload_success,
                error_message=str(error),
            )
            return Response(
                {
                    "error": str(error),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )



class CampaignPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100  
    
    
class CampaignListAPIView(generics.ListAPIView):
    serializer_class = CampaignDataSerializer
    pagination_class = CampaignPagination

    def get_queryset(self):
        queryset = CampaignData.objects.all()
        channel = self.request.query_params.get("channel")
        campaign_name = self.request.query_params.get("campaign_name")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if channel:
            queryset = queryset.filter(channel__iexact=channel)

        if campaign_name:
            queryset = queryset.filter(campaign_name__icontains=campaign_name)

        if start_date:
            queryset = queryset.filter(date__gte=start_date)

        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        return queryset


class CampaignDetailAPIView(generics.RetrieveAPIView):
    queryset = CampaignData.objects.all()
    serializer_class = CampaignDataSerializer


class KPIAPIView(APIView):
    def get(self, request):
        queryset = CampaignData.objects.all()

        channel = request.query_params.get("channel")
        campaign_name = request.query_params.get("campaign_name")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if channel:
            queryset = queryset.filter(channel__iexact=channel)

        if campaign_name:
            queryset = queryset.filter(campaign_name__icontains=campaign_name)

        if start_date:
            queryset = queryset.filter(date__gte=start_date)

        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        totals = queryset.aggregate(
            total_impressions=Sum("impressions"),
            total_clicks=Sum("clicks"),
            total_conversions=Sum("conversions"),
            total_cost=Sum("cost"),
            total_revenue=Sum("revenue"),
        )
        total_impressions = totals["total_impressions"] or 0
        total_clicks = totals["total_clicks"] or 0
        total_conversions = totals["total_conversions"] or 0
        total_cost = totals["total_cost"] or 0
        total_revenue = totals["total_revenue"] or 0
        ctr = (total_clicks / total_impressions * 100) if total_impressions else 0
        cpc = (total_cost / total_clicks) if total_clicks else 0
        cpa = (total_cost / total_conversions) if total_conversions else 0
        roas = (total_revenue / total_cost) if total_cost else 0
        conversion_rate = (
            (total_conversions / total_clicks * 100) if total_clicks else 0
        )
        return Response(
            {
                "filters": {
                    "channel": channel,
                    "campaign_name": campaign_name,
                    "start_date": start_date,
                    "end_date": end_date,
                },
                "total_impressions": total_impressions,
                "total_clicks": total_clicks,
                "total_conversions": total_conversions,
                "total_cost": round(float(total_cost), 2),
                "total_revenue": round(float(total_revenue), 2),
                "ctr": round(float(ctr), 2),
                "cpc": round(float(cpc), 2),
                "cpa": round(float(cpa), 2),
                "roas": round(float(roas), 2),
                "conversion_rate": round(float(conversion_rate), 2),
            },
        )


class KPIByChannelAPIView(APIView):
    def get(self, request):
        queryset = CampaignData.objects.all()
        channel = request.query_params.get("channel")
        campaign_name = request.query_params.get("campaign_name")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        
        if channel:
            queryset = queryset.filter(channel__iexact=channel)
        
        if campaign_name:
            queryset = queryset.filter(campaign_name__icontains=campaign_name)
            
        if start_date: 
            queryset = queryset.filter(date__gte=start_date)
            
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        data = (
            queryset
            .values("channel")
            .annotate(
                total_revenue=Sum("revenue"),
                total_conversions=Sum("conversions"),
                )
            .order_by("channel")
        )
        
        results = []
        
        for item in data:
            results.append(
                {
                    "channel": item["channel"],
                    "total_revenue": float(item["total_revenue"] or 0),
                    "total_conversions": item["total_conversions"] or 0,
                }
            )
        return Response(results)
        
# Get unique campaigns to use as options in html page for selecting        
class CampaignOptionsAPIView(APIView):
    def get(self, request):
        campaigns = (
            CampaignData.objects
            .values_list("campaign_name", flat=True)
            .distinct()
            .order_by("campaign_name")
        )
        return Response(list(campaigns))
    
    
# Get unique channel names to use as options in html. page for selecting
class ChannelOptionsAPIView(APIView):
    def get(self, request):
        channels = (
            CampaignData.objects
            .values_list("channel", flat=True)
            .distinct()
            .order_by("channel")
        )
        return Response(list(channels))

# Create a view to upload history page/section using CSVUploadLog
class CSVUploadLogListAPIView(generics.ListAPIView):
    queryset = CSVUploadLog.objects.all().order_by("-uploaded_at")
    serializer_class = CSVUploadLogSerializer
    

class CampaignExportCSVAPIView(APIView):
    def get(self, request):
        query_set = CampaignData.objects.all()
        channel = request.query_params.get("channel")
        campaign_name = request.query_params.get("campaign_name")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        
        if channel:
            query_set = query_set.filter(channel__iexact=channel)
        
        if campaign_name:
            query_set = query_set.filter(campaign_name__icontains=campaign_name)
            
        if start_date:
            query_set = query_set.filter(date__gte=start_date)
        
        if end_date:
            query_set = query_set.filter(date__lte=end_date)
            
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename=campaign_export.csv'
        
        writer = csv.writer(response)
        
        writer.writerow(
            [
                "date",
                "campaign_name",
                "channel",
                "impressions",
                "clicks",
                "conversions",
                "cost",
                "revenue",
            ]
        )
        
        for campaign in query_set:
            writer.writerow(
                [
                    campaign.date,
                    campaign.campaign_name,
                    campaign.channel,
                    campaign.impressions,
                    campaign.clicks,
                    campaign.conversions,
                    campaign.cost,
                    campaign.revenue,
                ]
            )
        return response


def dashboard(request):
    return render(request, "analytics/dashboard.html")

