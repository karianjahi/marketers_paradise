console.log("dashboard.js loaded");

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

fetch("/api/kpis/")
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
        document.getElementById("total-impressions").textContent = "Error loading data: ";
        document.getElementById("total-clicks").textContent = "Error loading data: "
        document.getElementById("total-conversions").textContent = "Error loading data";
        document.getElementById("total-revenue").textContent = "Error loading data";
        document.getElementById("total-cost").textContent = "Error loading data";
        document.getElementById("ctr").textContent = "Error loading data";
        document.getElementById("cpc").textContent = "Error loading data";
        document.getElementById("cpa").textContent = "Error loading data";
        document.getElementById("roas").textContent = "Error loading data";
        document.getElementById("conversion-rate").textContent = "Error loading data";
    });