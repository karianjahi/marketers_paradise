console.log("dashboard.js loaded");
console.log("Chart.js:", Chart);

let currentCampaignPage = 1;
let hasNextCampaignPage = false;
let hasPreviousCampaignPage = false;

function formatNumber(value) {
    return Number(value).toLocaleString();
}

function formatCurrency(value) {
    return "€" + Number(value).toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

function formatPercent(value) {
    return Number(value).toFixed(2) + "%";
}

function formatRatio(value) {
    return Number(value).toFixed(2);
}


function loadKPIs(channel = "", campaignName = "", startDate = "", endDate = "") {
    let url = "/api/kpis/";
    let params = new URLSearchParams();
    if (channel) {
        // url += "?channel=" + encodeURIComponent(channel);
        params.append("channel", channel);
    }

    if (startDate) {
        params.append("start_date", startDate);
    }

    if (endDate) {
        params.append("end_date", endDate);
    }

    if (campaignName) {
        params.append("campaign_name", campaignName);
    }

    if (params.toString()) {
        url += "?" + params.toString();
    }



    fetch(url)
        .then(response => response.json())
        .then(data => {
            document.getElementById("total-impressions").textContent =
                formatNumber(data.total_impressions);

            document.getElementById("total-clicks").textContent =
                formatNumber(data.total_clicks);

            document.getElementById("total-conversions").textContent =
                formatNumber(data.total_conversions);

            document.getElementById("total-cost").textContent =
                formatCurrency(data.total_cost);

            document.getElementById("total-revenue").textContent =
                formatCurrency(data.total_revenue);

            document.getElementById("ctr").textContent =
                formatPercent(data.ctr);

            document.getElementById("cpc").textContent =
                formatCurrency(data.cpc);

            document.getElementById("cpa").textContent =
                formatCurrency(data.cpa);

            document.getElementById("roas").textContent =
                formatRatio(data.roas);

            document.getElementById("conversion-rate").textContent =
                formatPercent(data.conversion_rate);
        })
        .catch(error => {
            console.error("Error loading KPI data:", error);
            const errorMessage = "Error loading data";

            document.getElementById("total-impressions").textContent =
                errorMessage;

            document.getElementById("total-clicks").textContent =
                errorMessage;

            document.getElementById("total-conversions").textContent =
                errorMessage;

            document.getElementById("total-cost").textContent =
                errorMessage;

            document.getElementById("total-revenue").textContent =
                errorMessage;

            document.getElementById("ctr").textContent =
                errorMessage;

            document.getElementById("conversion-rate").textContent =
                errorMessage;

            document.getElementById("cpc").textContent =
                errorMessage;

            document.getElementById("cpa").textContent =
                errorMessage;

            document.getElementById("roas").textContent =
                errorMessage;
        });
}



let revenueChart = null;
let conversionChart = null;

function loadCharts(channel = "", campaignName = "", startDate = "", endDate = "") {
    let url = "/api/kpis/by-channel/";
    let params = new URLSearchParams();

    if (channel) {
        params.append("channel", channel);
    }

    if (campaignName) {
        params.append("campaign_name", campaignName);
    }

    if (startDate) {
        params.append("start_date", startDate);
    }

    if (endDate) {
        params.append("end_date", endDate);
    }

    if (params.toString()) {
        url += "?" + params.toString();
    }


    fetch(url)
        .then(response => response.json())
        .then(data => {
            const labels = data.map(item => item.channel);
            const revenues = data.map(item => item.total_revenue);
            const conversions = data.map(item => item.total_conversions);

            const revenueCanvas = document.getElementById("channelChart");
            const conversionCanvas = document.getElementById("conversionsChart");

            if (revenueChart) {
                revenueChart.destroy();
            }

            if (conversionChart) {
                conversionChart.destroy();
            }

            revenueChart = new Chart(revenueCanvas, {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: "Revenue by Channel",
                            data: revenues
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: true
                        },
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    return "Revenue €" + Number(context.raw).toLocaleString(undefined, {
                                        minimumFractionDigits: 2,
                                        maximumFractionDigits: 2
                                    }
                                    );
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function (value) {
                                    return "€" + Number(value).toLocaleString();
                                }
                            }
                        }
                    }
                },
            });

            conversionChart = new Chart(conversionCanvas, {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: "Conversions by Channel",
                            data: conversions
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    return "Conversions: " + Number(context.raw).toLocaleString();
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function (value) {
                                    return Number(value).toLocaleString();
                                }
                            }
                        }
                    }
                }


            });
        });
}

// populate the table function with (un)filtered data
function loadCampaigns(channel = "", campaignName = "", startDate = "", endDate = "", page = 1) {
    let url = "/api/campaigns/";
    let params = new URLSearchParams();

    if (channel) {
        params.append("channel", channel);
    }

    if (campaignName) {
        params.append("campaign_name", campaignName);
    }

    if (startDate) {
        params.append("start_date", startDate);
    }

    if (endDate) {
        params.append("end_date", endDate);
    }
    params.append("page", page);
    if (params.toString()) {
        url += "?" + params.toString();
    }




    // now that we have constructed the url required, we can fetch the data from django endpoint
    fetch(url)
        .then(response => response.json())
        .then(data => {

            const pageSize = 10;
            const nPages = Math.max(1, Math.ceil(data.count / pageSize));
            document.getElementById("page-info").textContent = `Page ${currentCampaignPage} of ${nPages}`
            hasNextCampaignPage = Boolean(data.next);
            hasPreviousCampaignPage = Boolean(data.previous);

            // document.getElementById("page-info").textContent = "Page " + page;

            document.getElementById("next-page").disabled = !hasNextCampaignPage;

            document.getElementById("previous-page").disabled = !hasPreviousCampaignPage;

            const tableBody = document.getElementById("campaign-table-body");
            tableBody.innerHTML = "";
            campaigns = data.results || data;
            for (const item of campaigns) {
                const row = `
                    <tr>
                        <td>${item.date}</td>
                        <td>${item.campaign_name}</td>
                        <td>${item.channel}</td>
                        <td>${formatNumber(item.impressions)}</td>
                        <td>${formatNumber(item.clicks)}</td>
                        <td>${formatNumber(item.conversions)}</td>
                        <td>${formatCurrency(item.cost)}</td>
                        <td>${formatCurrency(item.revenue)}</td>
                    </tr>
                `;
                tableBody.innerHTML += row;
            }


        })
        .catch(error => {
            console.error("Error loading campaign records:", error);
        });
}


// Apply filter when the apply filter button is clicked
document.getElementById("apply-filter").addEventListener("click", function () {
    const selectedChannel = document.getElementById("channel-filter").value;
    const startDate = document.getElementById("start-date").value;
    const endDate = document.getElementById("end-date").value;
    const campaignName = document.getElementById("campaign-name-filter").value;
    loadKPIs(selectedChannel, campaignName, startDate, endDate);
    loadCharts(selectedChannel, campaignName, startDate, endDate);
    loadCampaigns(selectedChannel, campaignName, startDate, endDate);
});

// Navigate campaign pages
document.getElementById("next-page").addEventListener("click", function () {
    if (hasNextCampaignPage) {
        currentCampaignPage += 1

        const selectedChannel = document.getElementById("channel-filter").value;
        const campaignName = document.getElementById("campaign-name-filter").value;
        const startDate = document.getElementById("start-date").value;
        const endDate = document.getElementById("end-date").value;

        loadCampaigns(selectedChannel, campaignName, startDate, endDate, currentCampaignPage);

    }
});


document.getElementById("previous-page").addEventListener("click", function () {
    if (hasPreviousCampaignPage && currentCampaignPage > 1) {
        currentCampaignPage -= 1;
        const selectedChannel = document.getElementById("channel-filter").value;
        const campaignName = document.getElementById("campaign-name-filter").value;
        const startDate = document.getElementById("start-date").value;
        const endDate = document.getElementById("end-date").value;

        loadCampaigns(selectedChannel, campaignName, startDate, endDate, currentCampaignPage);
    }
});


// load campaign names in javascript
function loadCampaignOptions() {
    fetch("/api/campaign-options/")
        .then(response => response.json())
        .then(data => {
            const campaignSelect = document.getElementById("campaign-name-filter");

            for (const campaignName of data) {
                const option = document.createElement("option");
                option.value = campaignName;
                option.textContent = campaignName;
                campaignSelect.appendChild(option);
            }
        })
        .catch(error => {
            console.error("Error loading campaign options:", error);
        });
}

// Populate csv upload logs table with data
function PopulateCSVLogsTableBody() {
    const uploadLogTableBody = document.getElementById("upload-log-table-body");
    const url = "/api/upload-logs/";
    uploadLogTableBody.innerHTML = "";
    fetch(url)
        .then(response => response.json())
        .then(data => {
            let innerTableBodyHTML = ""

            for (const item of data) {
                innerTableBodyHTML +=
                    `
                    <tr>
                        <td>${item.filename}</td>
                        <td>${item.total_rows}</td>
                        <td>${item.created_rows}</td>
                        <td>${item.skipped_rows}</td>
                        <td>${item.invalid_rows}</td>
                        <td>${item.upload_success ? "Yes" : "No"}</td>
                        <td>${new Date(item.uploaded_at).toLocaleString("en-GB", {
                        day: "2-digit",
                        month: "short",
                        year: "numeric",
                        hour: "2-digit",
                        minute: "2-digit",
                        second: "2-digit",
                    })} hrs</td>
                    </tr>
                    `
            }
            uploadLogTableBody.innerHTML = innerTableBodyHTML;
        })
        .catch(error => {
            console.error("Error loading upload logs:", error);
        });
}




// Load all KPIs and create the charts and the campaign table when the page first opens
loadCampaignOptions()
loadKPIs();
loadCharts();
PopulateCSVLogsTableBody()
loadCampaigns();
