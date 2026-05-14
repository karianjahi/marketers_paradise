console.log("dashboard.js loaded");
fetch("/api/kpis/")
    .then(response => response.json())
    .then(data => {
        document.getElementById("total-impressions").textContent = data.total_impressions
        document.getElementById("total-clicks").textContent = data.total_clicks
        document.getElementById("total-conversions").textContent = data.total_conversions
        document.getElementById("total-cost").textContent = data.total_cost
        document.getElementById("total-revenue").textContent = "€ " + data.total_revenue
    })
    .catch(error => {
        document.getElementById("total-impressions").textContent = "Error loading data: ";
        document.getElementById("total-clicks").textContent = "Error loading data: "
        document.getElementById("total-conversions").textContent = "Error loading data";
        document.getElementById("total-revenue").textContent = "Error loading data";
        document.getElementById("roas").textContent = "Error loading data";
    });