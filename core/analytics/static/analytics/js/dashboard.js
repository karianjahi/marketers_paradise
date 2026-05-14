console.log("dashboard.js loaded");
console.log("Chart.js:", Chart);

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

function loadKPIs(channel = "") {
    let url = "/api/kpis/";

    if (channel) {
        url += "?channel=" + encodeURIComponent(channel);
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            document.getElementById("total-impressions").textContent = formatNumber(data.total_impressions);
            document.getElementById("total-clicks").textContent = formatNumber(data.total_clicks);
            document.getElementById("total-conversions").textContent = formatNumber(data.total_conversions);
            document.getElementById("total-cost").textContent = formatCurrency(data.total_cost);
            document.getElementById("total-revenue").textContent = formatCurrency(data.total_revenue);
            document.getElementById("ctr").textContent = formatPercent(data.ctr);
            document.getElementById("cpc").textContent = formatCurrency(data.cpc);
            document.getElementById("cpa").textContent = formatCurrency(data.cpa);
            document.getElementById("roas").textContent = formatRatio(data.roas);
            document.getElementById("conversion-rate").textContent = formatPercent(data.conversion_rate);
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

// Apply filter when the button is clicked
document.getElementById("apply-filter").addEventListener("click", function() {
        const selectedChannel = document.getElementById("channel-filter").value;
        loadKPIs(selectedChannel)
    });

// Load all KPIs when the page first opens
loadKPIs();


const channelCanvas = document.getElementById("channelChart");
const conversionsCanvas = document.getElementById("conversionsChart");


fetch("/api/kpis/by-channel/")
    .then(response => response.json())
    .then(data => {
        const labels = data.map(item => item.channel);
        const revenues = data.map(item => item.total_revenue);

        new Chart(channelCanvas, {
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
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return "Revenue €" + Number(context.raw).toLocaleString(undefined, {
                                    minimumFractionDigits: 2,
                                    maximumFractionDigits: 2
                                });
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
            }
        });

        const conversions = data.map(item => item.total_conversions);
        const conversionsCanvas = document.getElementById("conversionsChart")
        new Chart(conversionsCanvas, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "Conversions by Channel",
                        data: conversions,
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
        })
    })
    .catch(error => {
        console.error("Error loading channel chart data:", error)
    });

