// Base URL of your FastAPI backend
const BASE_URL = "http://localhost:8000"; // Replace with actual URL of FastAPI Backend

// Function to handle hourly data submission
async function submitHourlyData(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // Get form input values
    const timestamp = document.getElementById("timestamp").value;
    const flowRate = document.getElementById("flowRate").value;
    const cod = document.getElementById("cod").value;
    const waterQuality = document.getElementById("waterQuality").value;

    try {
        // Send POST request to FastAPI
        const response = await fetch(`${BASE_URL}/submit-hourly`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
                timestamp: timestamp,
                flow_rate: flowRate,
                cod: cod,
                water_quality: waterQuality,
            }),
        });

        const result = await response.json();
        if (response.ok) {
            alert("Hourly data submitted successfully!");
        } else {
            alert(`Error: ${result.detail || "Failed to submit data"}`);
        }
    } catch (error) {
        console.error("Error submitting hourly data:", error);
        alert("Failed to submit hourly data.");
    }
}

// Function to handle daily summary submission
async function submitDailySummary(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // Get form input values
    const date = document.getElementById("date").value;
    const clarifierStatus = document.getElementById("clarifierStatus").value;
    const observations = document.getElementById("observations").value;

    try {
        // Send POST request to FastAPI
        const response = await fetch(`${BASE_URL}/submit-daily`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
                date: date,
                clarifier_status: clarifierStatus,
                observations: observations,
            }),
        });

        const result = await response.json();
        if (response.ok) {
            alert("Daily summary submitted successfully!");
        } else {
            alert(`Error: ${result.detail || "Failed to submit data"}`);
        }
    } catch (error) {
        console.error("Error submitting daily summary:", error);
        alert("Failed to submit daily summary.");
    }
}

// Function to list exported files
async function listExports() {
    try {
        // Send GET request to FastAPI
        const response = await fetch(`${BASE_URL}/list-exports`, {
            method: "GET",
        });

        const files = await response.json();
        if (response.ok) {
            const fileListElement = document.getElementById("fileList");
            fileListElement.innerHTML = ""; // Clear the list

            if (files.length > 0) {
                files.forEach((file) => {
                    const listItem = document.createElement("li");
                    listItem.textContent = file;
                    fileListElement.appendChild(listItem);
                });
            } else {
                fileListElement.textContent = "No files found.";
            }
        } else {
            alert("Failed to list export files.");
        }
    } catch (error) {
        console.error("Error listing exports:", error);
        alert("Failed to fetch export files.");
    }
}

// Function to clear exported files
async function clearExports() {
    try {
        // Send DELETE request to FastAPI
        const response = await fetch(`${BASE_URL}/clear-exports`, {
            method: "DELETE",
        });

        if (response.ok) {
            alert("Export files cleared successfully!");
            listExports(); // Refresh the file list
        } else {
            alert("Failed to clear export files.");
        }
    } catch (error) {
        console.error("Error clearing exports:", error);
        alert("Failed to clear export files.");
    }
}

// Toggle between light mode and dark mode
document.addEventListener("DOMContentLoaded", () => {
    setTimeout(() => {
        const toggleButton = document.getElementById("modeToggle");

        toggleButton.addEventListener("click", () => {
            document.body.classList.toggle("dark-mode");

            // Update the button text based on the current mode
            if (document.body.classList.contains("dark-mode")) {
                toggleButton.textContent = "Switch to Light Mode";
            } else {
                toggleButton.textContent = "Switch to Dark Mode";
            }
        });
        // Auto-populate datetime-local fields with the current time
        const datetimeFields = document.querySelectorAll('input[type="datetime-local"]');
        const now = new Date();
        const formattedTime = now.toISOString().slice(0, 16); // Format as YYYY-MM-DDTHH:mm

        datetimeFields.forEach((field) => {
            field.value = formattedTime;
        });
        },100);
	
});


// Attach event listeners to forms and buttons
//document.getElementById("hourlyForm").addEventListener("submit", submitHourlyData);
//document.getElementById("dailyForm").addEventListener("submit", submitDailySummary);
// document.getElementById("listExportsButton").addEventListener("click", listExports);
// document.getElementById("clearExportsButton").addEventListener("click", clearExports);
