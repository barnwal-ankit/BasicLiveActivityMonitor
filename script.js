let chart;
let activityData = {
  labels: [],
  datasets: [
    { label: "Running", data: [], borderColor: "red", fill: false },
    { label: "Sitting", data: [], borderColor: "blue", fill: false },
    { label: "Standing", data: [], borderColor: "green", fill: false },
    { label: "Walking", data: [], borderColor: "orange", fill: false },
  ],
};

async function connectSerial() {
  try {
    const baudRate = parseInt(document.getElementById("baudRate").value);
    const port = await navigator.serial.requestPort();
    await port.open({ baudRate });

    const decoder = new TextDecoderStream();
    const reader = port.readable.pipeThrough(decoder).getReader();

    document.getElementById(
      "output"
    ).textContent = `Connected at ${baudRate} baud... Waiting for data...\n`;

    let buffer = "";
    initChart();

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      buffer += value;

      if (buffer.includes("Predictions") && buffer.includes("Anomaly score")) {
        processSerialData(buffer);
        buffer = "";
      }
    }

    await reader.cancel();
    await port.close();
  } catch (error) {
    console.error("Serial connection error:", error);
    document.getElementById("output").textContent =
      "Error: Could not connect to serial device.";
  }
}

function processSerialData(data) {
  const output = document.getElementById("output");
  const rawDataToggle = document.getElementById("rawDataToggle").checked;
  const graphToggle = document.getElementById("graphToggle").checked;

  const predictions = {
    running_forearm: 0,
    sitting_forearm: 0,
    standing_forearm: 0,
    walking_forearm: 0,
  };

  data.match(/(\w+_forearm:\s*-?\d+(\.\d+)?)/g)?.forEach((line) => {
    const [activity, score] = line.split(":").map((s) => s.trim());
    if (predictions.hasOwnProperty(activity)) {
      predictions[activity] = parseFloat(score);
    }
  });

  const anomalyMatch = data.match(/Anomaly score:\s*(-?\d+\.\d+)/);
  const anomalyScore = anomalyMatch
    ? `Anomaly Score: ${anomalyMatch[1]}`
    : "Anomaly Score: Not found";

 
  if (rawDataToggle) {
    output.style.background = "rgba(255, 0, 0, 0.1)";
    output.textContent = data; 
  } else {
    output.style.background = "rgba(0, 255, 0, 0.1)";
    output.textContent = `\nActivity Predictions:\n
        Running: ${predictions.running_forearm}\n
        Sitting: ${predictions.sitting_forearm}\n
        Standing: ${predictions.standing_forearm}\n
        Walking: ${predictions.walking_forearm}\n
        \n${anomalyScore}`;
  }

  if (graphToggle) {
    document.getElementById("chartContainer").style.display = "block";
    updateChart(predictions);
  } else {
    document.getElementById("chartContainer").style.display = "none";
  }
}

function initChart() {
  const ctx = document.getElementById("activityChart").getContext("2d");
  chart = new Chart(ctx, {
    type: "line",
    data: activityData,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      scales: {
        x: { title: { display: true, text: "Time" } },
        y: {
          title: { display: true, text: "Activity Score" },
          min: -1,
          max: 1,
        },
      },
    },
  });
}

function updateChart(predictions) {
  const time = new Date().toLocaleTimeString();

  // Keep last 20 entries to prevent performance issues
  if (activityData.labels.length > 20) {
    activityData.labels.shift();
    activityData.datasets.forEach((dataset) => dataset.data.shift());
  }

  activityData.labels.push(time);
  activityData.datasets.forEach((dataset, i) => {
    dataset.data.push(Object.values(predictions)[i]);
  });

  chart.update();
}
