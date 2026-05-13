import pandas as pd

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from django.db import IntegrityError

from .serializers import CSVUploadSerializer, CSVUploadLogSerializer
from .models import CampaignData, CSVUploadLog

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
            df = pd.read_csv(csv_file)
            total_rows = len(df)
            missing_columns = [
                column for column in REQUIRED_COLUMNS if column not in df.columns
            ]
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
                    if row[REQUIRED_COLUMNS].isnull().any():
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
