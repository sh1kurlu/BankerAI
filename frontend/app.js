const API_BASE = "http://127.0.0.1:8000";

const btn = document.getElementById("btn-recommend");
const statusEl = document.getElementById("status");
const resultsEl = document.getElementById("results");

// Visualization elements
const vizSection = document.getElementById("visualizations");
const vizContainer = document.getElementById("viz-container");
const vizChart = document.getElementById("viz-chart");
let currentChart = null;

// Visualization control buttons
const btnViz = document.getElementById("btn-visualizations");
const btnScoreDist = document.getElementById("btn-score-dist");
const btnCategoryDist = document.getElementById("btn-category-dist");
const btnUserPrefs = document.getElementById("btn-user-prefs");
const btnRecStrength = document.getElementById("btn-rec-strength");

btn.addEventListener("click", async () => {
  const userId = document.getElementById("user-id").value.trim();
  const k = parseInt(document.getElementById("k").value, 10) || 5;

  if (!userId) {
    alert("Please enter a user ID.");
    return;
  }

  statusEl.textContent = "Loading recommendations...";
  resultsEl.innerHTML = "";

  try {
    const res = await fetch(`${API_BASE}/api/recommend`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, k })
    });

    if (!res.ok) {
      let errText = `Error: ${res.status}`;
      try {
        const err = await res.json();
        errText = `Error: ${err.error || res.status}`;
      } catch {}
      statusEl.textContent = errText;
      return;
    }

    const data = await res.json();
    statusEl.textContent = `Showing ${data.recommendations.length} recommendations for user ${data.user_id}:`;

    data.recommendations.forEach((rec) => {
      const card = document.createElement("div");
      card.className = "card";

      card.innerHTML = `
        <div class="card-title">${rec.item_name}</div>
        <div class="card-chip">${rec.category}</div>
        <div class="card-score">Score: ${rec.score.toFixed(1)}</div>
        <div class="card-feedback">${rec.feedback}</div>
      `;

      resultsEl.appendChild(card);
    });

    if (data.recommendations.length === 0) {
      statusEl.textContent = "No recommendations found for this user.";
    }
  } catch (e) {
    console.error(e);
    statusEl.textContent = "Network or server error. Check console.";
  }
});

// Visualization functions
function showVisualizations() {
  vizSection.style.display = vizSection.style.display === "none" ? "block" : "none";
}

async function fetchVisualization(endpoint, chartType) {
  try {
    const res = await fetch(`${API_BASE}${endpoint}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    renderChart(data, chartType);
  } catch (e) {
    console.error("Visualization fetch error:", e);
    vizContainer.innerHTML = `<p class="error">Failed to load visualization: ${e.message}</p>`;
  }
}

function renderChart(vizData, chartType) {
  // Destroy existing chart if it exists
  if (currentChart) {
    currentChart.destroy();
  }

  const ctx = vizChart.getContext('2d');
  
  let chartConfig = {
    type: 'bar',
    data: {},
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: vizData.title
        }
      }
    }
  };

  switch (vizData.chart_type) {
    case 'histogram':
      chartConfig.type = 'bar';
      chartConfig.data = {
        labels: vizData.data.labels,
        datasets: [{
          label: 'Score Count',
          data: vizData.data.values,
          backgroundColor: 'rgba(54, 162, 235, 0.6)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        }]
      };
      chartConfig.options.scales = {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Count'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Score Range'
          }
        }
      };
      break;

    case 'pie':
      chartConfig.type = 'pie';
      chartConfig.data = {
        labels: vizData.data.labels,
        datasets: [{
          data: vizData.data.values,
          backgroundColor: [
            'rgba(255, 99, 132, 0.6)',
            'rgba(54, 162, 235, 0.6)',
            'rgba(255, 205, 86, 0.6)',
            'rgba(75, 192, 192, 0.6)',
            'rgba(153, 102, 255, 0.6)'
          ]
        }]
      };
      break;

    case 'multi':
      // Handle multi-chart data (user preferences)
      chartConfig.type = 'bar';
      chartConfig.data = {
        labels: vizData.data.category_preferences.labels,
        datasets: [{
          label: 'Category Activity',
          data: vizData.data.category_preferences.values,
          backgroundColor: 'rgba(75, 192, 192, 0.6)'
        }]
      };
      chartConfig.options.scales = {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Activity Count'
          }
        }
      };
      break;

    case 'scatter':
      chartConfig.type = 'scatter';
      const scatterData = vizData.data.users.map((user, index) => ({
        x: vizData.data.recommendation_counts[index],
        y: vizData.data.average_scores[index]
      }));
      
      chartConfig.data = {
        datasets: [{
          label: 'Users',
          data: scatterData,
          backgroundColor: 'rgba(255, 99, 132, 0.6)'
        }]
      };
      chartConfig.options.scales = {
        x: {
          title: {
            display: true,
            text: 'Number of Recommendations'
          }
        },
        y: {
          title: {
            display: true,
            text: 'Average Score'
          }
        }
      };
      break;

    default:
      chartConfig.data = {
        labels: vizData.data.labels || [],
        datasets: [{
          label: 'Data',
          data: vizData.data.values || [],
          backgroundColor: 'rgba(54, 162, 235, 0.6)'
        }]
      };
  }

  currentChart = new Chart(ctx, chartConfig);
}

// Event listeners for visualization buttons
btnViz.addEventListener("click", showVisualizations);
btnScoreDist.addEventListener("click", () => fetchVisualization('/api/visualization/score-distribution', 'histogram'));
btnCategoryDist.addEventListener("click", () => fetchVisualization('/api/visualization/category-distribution', 'pie'));
btnUserPrefs.addEventListener("click", () => {
  const userId = document.getElementById("user-id").value.trim();
  if (!userId) {
    alert("Please enter a user ID first.");
    return;
  }
  fetchVisualization(`/api/visualization/user-preferences/${userId}`, 'multi');
});
btnRecStrength.addEventListener("click", () => fetchVisualization('/api/visualization/recommendation-strength', 'scatter'));
