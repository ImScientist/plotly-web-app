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
};

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

function buildDensityFigure(curves, colors) {
  return {
    data: curves.map((curve, index) => ({
      x: curve.x,
      y: curve.y,
      type: "scatter",
      mode: "lines",
      name: `pod ${index + 1}`,
      line: {
        color: colors[index % colors.length],
        width: 3,
        shape: "spline",
        smoothing: 1.25,
      },
      marker: {
        color: colors[index % colors.length],
      },
      hovertemplate: "Score %{x:.2f}<br>Density %{y:.4f}<extra></extra>",
    })),
    layout: {
      xaxis: {
        title: "Score",
        showgrid: false,
        zeroline: false,
        showline: true,
        linecolor: "#5f6c80",
        linewidth: 1,
      },
      yaxis: {
        title: "Density",
        showgrid: false,
        zeroline: false,
        showline: true,
        linecolor: "#5f6c80",
        linewidth: 1,
      },
      legend: {
        x: 0.99,
        y: 0.99,
        xanchor: "right",
        yanchor: "top",
      },
      margin: { t: 24, r: 24, b: 56, l: 56 },
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

  const positiveCurves = state.content.positive_groups[positiveKey]?.curves;
  const negativeCurves = state.content.negative_groups[negativeKey]?.curves;
  const rocAuc = state.content.roc_auc_scores[scoreKey];

  if (!positiveCurves || !negativeCurves || !rocAuc) {
    throw new Error(`Missing precomputed content for selection ${scoreKey}.`);
  }

  const positiveFigure = buildDensityFigure(positiveCurves, POSITIVE_COLORS);
  const negativeFigure = buildDensityFigure(negativeCurves, NEGATIVE_COLORS);

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
  }
}

document.addEventListener("DOMContentLoaded", init);

