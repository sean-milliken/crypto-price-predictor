let chart; // global chart variable

document.getElementById("predict-btn").addEventListener("click", async () => {
  const symbol = document.getElementById("symbol").value.trim();
  const resultDiv = document.getElementById("result");

  if (!symbol) {
    alert("Please enter a crypto symbol!");
    return;
  }

  resultDiv.innerText = "Fetching prediction...";

  try {
    const res = await fetch(`http://127.0.0.1:8000/predict/${symbol}`);
    const data = await res.json();

    if (res.ok) {
      resultDiv.innerText = `Symbol: ${data.symbol}\nPrediction: ${data.prediction}\nProbability: ${data.probability}`;

      // Prepare data for chart
      const probabilities = [
        data.probability,          // probability UP
        1 - data.probability       // probability DOWN
      ];

      const ctx = document.getElementById("predictionChart").getContext("2d");

      if (chart) chart.destroy(); // remove previous chart

      chart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: ["UP", "DOWN"],
          datasets: [{
            label: "Probability",
            data: probabilities,
            backgroundColor: ["#4CAF50", "#F44336"]
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: { beginAtZero: true, max: 1 }
          }
        }
      });

    } else {
      resultDiv.innerText = `Error: ${data.error}`;
    }
  } catch (err) {
    resultDiv.innerText = "Error connecting to API. Make sure the backend is running.";
  }
});
