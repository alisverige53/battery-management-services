function updateData() {
  fetch("http://127.0.0.1:5000/info")
    .then(response => response.json())
    .then(data => {
      const box = document.getElementById("data-box");
      box.innerHTML = `
        <p>Simulerad tid: ${data.sim_time_hour}:${data.sim_time_min}</p>
        <p>Förbrukning: ${data.base_current_load} kW</p>
        <p>Batterinivå: ${data.battery_capacity_kWh} kWh</p>
        <p>Laddning: ${data.ev_battery_charge_start_stopp ? "PÅ" : "AV"}</p>
      `;
    })
    .catch(error => {
      document.getElementById("data-box").innerText = "Kunde inte hämta data.";
    });
}

setInterval(updateData, 2000);
updateData();
