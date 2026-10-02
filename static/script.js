
async function analyzeMessage() {
    const messageInput = document.getElementById("message");
    const analyzeBtn = document.getElementById("analyzeBtn");
    const resultSection = document.getElementById("result");
    const errorElement = document.getElementById("error");
    const predictionElement = document.getElementById("prediction");
    const confidenceElement = document.getElementById("confidence");
    const riskLevelElement = document.getElementById("riskLevel");
    const riskBarFill = document.getElementById("riskBarFill");
    const indicatorList = document.getElementById("indicatorList");

    const message = messageInput.value.trim();

    errorElement.textContent = "";
    resultSection.classList.add("hidden");

    if (!message) {
        errorElement.textContent = "Please enter a message to analyze.";
        return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "Analyzing...";

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Unable to analyze the message."
            );
        }

        // Display prediction
        predictionElement.textContent = data.prediction;
        predictionElement.classList.remove("safe", "suspicious");

        if (String(data.prediction).toLowerCase() === "safe") {
            predictionElement.classList.add("safe");
        } else {
            predictionElement.classList.add("suspicious");
        }

        // Display suspicious probability
        let confidence = Number(data.confidence);

        if (Number.isFinite(confidence)) {
            if (confidence <= 1) {
                confidence *= 100;
            }
            confidence = Math.min(100, Math.max(0, confidence));
            confidenceElement.textContent = confidence.toFixed(2) + "%";
        } else {
            confidenceElement.textContent = "Unavailable";
        }

        // Calculate risk level
        let riskLevel = "Unavailable";
        let riskClass = "";

        if (Number.isFinite(confidence)) {
            if (confidence < 30) {
                riskLevel = "LOW";
                riskClass = "risk-low";
            } else if (confidence < 70) {
                riskLevel = "MEDIUM";
                riskClass = "risk-medium";
            } else {
                riskLevel = "HIGH";
                riskClass = "risk-high";
            }
        }

        // Display risk level and bar
        riskLevelElement.textContent = riskLevel;
        riskLevelElement.className = riskClass;

        riskBarFill.className = "risk-bar-fill " + riskClass;
        riskBarFill.style.width =
            Number.isFinite(confidence) ? confidence + "%" : "0%";

        // Display warning indicators
        indicatorList.replaceChildren();

        if (Array.isArray(data.indicators) && data.indicators.length > 0) {
            data.indicators.forEach((indicator) => {
                const item = document.createElement("li");
                item.textContent = indicator;
                indicatorList.appendChild(item);
            });
        } else {
            const item = document.createElement("li");
            item.textContent = "No obvious warning indicators detected.";
            indicatorList.appendChild(item);
        }

        // Show analysis results
        resultSection.classList.remove("hidden");

        // Save and display history
        addToHistory(message, data, confidence, riskLevel);

    } catch (error) {
        errorElement.textContent = error.message;
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.textContent = "Analyze Message";
    }
}


// Save a new analysis and refresh the history display
function addToHistory(message, data, confidence, riskLevel) {
    const history = loadHistory();

    history.unshift({
        message: message,
        prediction: data.prediction,
        confidence: confidence,
        riskLevel: riskLevel,
        date: new Date().toLocaleString()
    });

    // Keep only the latest 20 analyses
    history.splice(20);

    localStorage.setItem("analysisHistory", JSON.stringify(history));

    displayHistory();
}


// Load saved history safely
function loadHistory() {
    try {
        const savedHistory = JSON.parse(
            localStorage.getItem("analysisHistory") || "[]"
        );

        return Array.isArray(savedHistory) ? savedHistory : [];
    } catch (error) {
        console.error("Could not load analysis history:", error);
        return [];
    }
}


// Display saved analysis history
function displayHistory() {
    const historyList = document.getElementById("historyList");
    const historyEmpty = document.getElementById("historyEmpty");

    if (!historyList || !historyEmpty) {
        return;
    }

    const history = loadHistory();

    historyList.replaceChildren();
    updateDashboardStats();
    historyEmpty.style.display = history.length === 0 ? "block" : "none";

    history.forEach((entry) => {
        const item = document.createElement("div");
        item.className = "history-item";

        // Prediction
        const heading = document.createElement("strong");
        heading.textContent = entry.prediction;

        if (String(entry.prediction).toLowerCase() === "safe") {
            heading.className = "safe";
        } else {
            heading.className = "suspicious";
        }

        // Message
        const messageText = document.createElement("p");
        messageText.className = "history-message";
        messageText.textContent = entry.message;

        // Risk and probability
        const riskText = document.createElement("p");
        const probability = Number(entry.confidence);

        riskText.textContent =
            "Risk: " + entry.riskLevel +
            " | Suspicious Probability: " +
            (Number.isFinite(probability)
                ? probability.toFixed(2) + "%"
                : "Unavailable");

        // Date and time
        const dateText = document.createElement("p");
        dateText.textContent = "Analyzed: " + entry.date;

        item.appendChild(heading);
        item.appendChild(messageText);
        item.appendChild(riskText);
        item.appendChild(dateText);

        historyList.appendChild(item);
    });
}


// Display saved history when the page opens
document.addEventListener("DOMContentLoaded", displayHistory);



function clearHistory() {
    const confirmClear = confirm(
        "Are you sure you want to delete all analysis history?"
    );

    if (!confirmClear) {
        return;
    }

    localStorage.removeItem("analysisHistory");
    displayHistory();
}





function exportHistory() {
    const history = loadHistory();

    if (history.length === 0) {
        alert("There is no analysis history to export.");
        return;
    }

    const headers = [
        "Message",
        "Prediction",
        "Risk Level",
        "Suspicious Probability",
        "Date"
    ];

    // Protect CSV values and reduce spreadsheet formula risks.
    function escapeCSV(value) {
        let text = String(value ?? "");

        if (/^[\s]*[=+\-@]/.test(text)) {
            text = "'" + text;
        }

        return '"' + text.replace(/"/g, '""') + '"';
    }

    const rows = history.map((entry) => [
        entry.message,
        entry.prediction,
        entry.riskLevel,
        Number.isFinite(Number(entry.confidence))
            ? Number(entry.confidence).toFixed(2) + "%"
            : "Unavailable",
        entry.date
    ]);

    const csvContent = [
        headers.map(escapeCSV).join(","),
        ...rows.map((row) => row.map(escapeCSV).join(","))
    ].join("\r\n");

    const blob = new Blob(
        ["\uFEFF" + csvContent],
        { type: "text/csv;charset=utf-8;" }
    );

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "social_engineering_analysis_history.csv";
    document.body.appendChild(link);
    link.click();
    link.remove();

    URL.revokeObjectURL(url);
}



function updateDashboardStats() {
    const history = loadHistory();

    const total = history.length;
    const suspicious = history.filter(
        entry => String(entry.prediction).toLowerCase() === "suspicious"
    ).length;
    const safe = history.filter(
        entry => String(entry.prediction).toLowerCase() === "safe"
    ).length;
    const highRisk = history.filter(
        entry => String(entry.riskLevel).toUpperCase() === "HIGH"
    ).length;

    document.getElementById("totalCount").textContent = total;
    document.getElementById("suspiciousCount").textContent = suspicious;
    document.getElementById("safeCount").textContent = safe;
    document.getElementById("highRiskCount").textContent = highRisk;
}