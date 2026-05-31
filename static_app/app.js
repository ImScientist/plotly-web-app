const POSITIVE_COLORS = ["#6e44ff", "#8f5eff", "#b07bff", "#d2a0ff"];
const NEGATIVE_COLORS = ["#008585", "#179b9b", "#38b2ac", "#78dcca"];

const state = {
  content: null,
};

const elements = {
  positiveRatio: document.getElementById("positive-ratio"),
  negativeRatio: document.getElementById("negative-ratio"),
  globalScore: document.getElementById("global-score"),
  meanScore: document.getElementById("mean-score"),
  podScores: document.getElementById("pod-scores"),
  positiveChart: document.getElementById("positive-chart"),
  negativeChart: document.getElementById("negative-chart"),
  status: document.getElementById("app-status"),
};

function setStatus(message, isError = false) {
  elements.status.textContent = message;
  elements.status.classList.toggle("error", isError);
}

function formatRatioLabel(ratioKey) {
  return Number.parseFloat(ratioKey).toString();
}

function createOption(value, selectedValue) {
  const option = document.createElement("option");
  option.value = value;
  option.textContent = formatRatioLabel(value);
  option.selected = value === selectedValue;
  return option;
}

function populateRatioSelect(selectElement, ratios, selectedValue) {
  selectElement.replaceChildren(...ratios.map((ratio) => createOption(ratio, selectedValue)));
}

function buildHistogramFigure(groupData, title, colors) {
  return {
    data: groupData.map((podData, index) => ({
      x: podData,
      type: "histogram",
      name: `pod ${index + 1}`,
      opacity: 0.64,
      histnorm: "probability density",
      marker: {
        color: colors[index % colors.length],
      },
      autobinx: true,
    })),
    layout: {
      barmode: "overlay",
      title,
      xaxis: { title: "Score" },
      yaxis: { title: "Density" },
      legend: { orientation: "h", y: 1.12 },
      margin: { t: 72, r: 24, b: 56, l: 56 },
      paper_bgcolor: "#ffffff",
      plot_bgcolor: "#ffffff",
    },
  };
}

function updateMetricList(values) {
  const items = values.map((value, index) => {
    const item = document.createElement("li");
    item.textContent = `pod ${index + 1}: ${value}`;
    return item;
  });
  elements.podScores.replaceChildren(...items);
}

function renderCharts() {
  const positiveKey = elements.positiveRatio.value;
  const negativeKey = elements.negativeRatio.value;
  const scoreKey = `${positiveKey}_${negativeKey}`;

  const positiveGroups = state.content.positive_groups[positiveKey]?.data;
  const negativeGroups = state.content.negative_groups[negativeKey]?.data;
  const rocAuc = state.content.roc_auc_scores[scoreKey];

  if (!positiveGroups || !negativeGroups || !rocAuc) {
    throw new Error(`Missing precomputed content for selection ${scoreKey}.`);
  }

  const positiveFigure = buildHistogramFigure(
    positiveGroups,
    `Positive class pod distributions for ratio ${formatRatioLabel(positiveKey)}`,
    POSITIVE_COLORS,
  );
  const negativeFigure = buildHistogramFigure(
    negativeGroups,
    `Negative class pod distributions for ratio ${formatRatioLabel(negativeKey)}`,
    NEGATIVE_COLORS,
  );

  Plotly.react(elements.positiveChart, positiveFigure.data, positiveFigure.layout, {
    responsive: true,
    displaylogo: false,
  });
  Plotly.react(elements.negativeChart, negativeFigure.data, negativeFigure.layout, {
    responsive: true,
    displaylogo: false,
  });

  elements.globalScore.textContent = Number(state.content.global_score).toFixed(3);
  elements.meanScore.textContent = rocAuc.mean;
  updateMetricList(rocAuc.values);
  setStatus(`Showing precomputed combination ${scoreKey}.`);
}

async function loadContent() {
  const response = await fetch("./data/content.json", { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Failed to load static content: ${response.status} ${response.statusText}`);
  }
  return response.json();
}

async function init() {
  try {
    if (typeof Plotly === "undefined") {
      throw new Error("Plotly.js did not load. Check your network connection and try again.");
    }

    setStatus("Loading precomputed static content…");
    state.content = await loadContent();

    const ratios = state.content.ratios;
    const defaultPositive = state.content.defaults?.positive_ratio ?? ratios[0];
    const defaultNegative = state.content.defaults?.negative_ratio ?? ratios[0];

    populateRatioSelect(elements.positiveRatio, ratios, defaultPositive);
    populateRatioSelect(elements.negativeRatio, ratios, defaultNegative);

    elements.positiveRatio.addEventListener("change", renderCharts);
    elements.negativeRatio.addEventListener("change", renderCharts);

    renderCharts();
  } catch (error) {
    console.error(error);
    setStatus(error.message, true);
  }
}

document.addEventListener("DOMContentLoaded", init);

