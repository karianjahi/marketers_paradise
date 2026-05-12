from django.shortcuts import render

import pandas as pd

from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import CSVUploadForm
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


def upload_csv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)

        if form.is_valid():
            csv_file = request.FILES["file"]

            try:
                df = pd.read_csv(csv_file)

                missing_columns = [
                    col for col in REQUIRED_COLUMNS if col not in df.columns
                ]

                if missing_columns:
                    messages.error(
                        request,
                        f"Missing columns: {', '.join(missing_columns)}"
                    )
                    return redirect("upload_csv")

                for _, row in df.iterrows():
                    CampaignData.objects.create(
                        date=row["date"],
                        campaign_name=row["campaign_name"],
                        channel=row["channel"],
                        impressions=row["impressions"],
                        clicks=row["clicks"],
                        conversions=row["conversions"],
                        cost=row["cost"],
                        revenue=row["revenue"],
                    )

                messages.success(request, "CSV uploaded successfully.")
                return redirect("dashboard")

            except Exception as e:
                messages.error(request, f"Error processing file: {e}")
                return redirect("upload_csv")

    else:
        form = CSVUploadForm() # what to create in the upload html once it hits there

    return render(request, "analytics/upload.html", {"form": form})