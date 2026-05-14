console.log("dashboard.js loaded");
fetch("/api/kpis/")
    .then(response => response.json())
    .then(data => {
        document.getElementById("kpi-output").textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        document.getElementById("kpi-output").textContent = "Error loading KPI data: " + error;
    });