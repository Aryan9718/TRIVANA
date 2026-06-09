window.pl_orbsmax = null;
window.pl_rade    = null;
window.pl_masse   = null;
window.pl_dens    = null;
window.pl_eqt     = null;

document.addEventListener("DOMContentLoaded", () => {
    const analyzeBtn = document.querySelector(".analyze-btn");
    const resultsSection = document.getElementById("results");
    const loader = document.getElementById("loader");
    const simContainer = document.getElementById("SimContainer");
    const fileInput = document.getElementById("fileInput"); // The file input element
    const analysisResultDiv = document.getElementById("analysisResult"); // Div to show 

    let planetData = [];
    let isSimulationInitialized = false;
    let selectedFeatures = null;

    // --- Load JSON with all planets ---
    async function loadPlanetData() {
        try {
            const response = await fetch("clean_labels_with_derived_cleaned.json");
            planetData = await response.json();
            console.log("Planet data ready for analysis:", planetData.length, "entries");
        } catch (error) {
            console.error("Failed to load planet data:", error);
        }
    }

    function masterAnalyze() {
        // BRANCH: Check if a file has been selected in the file input.
        if (fileInput.files.length > 0) {
            handleFileUpload();
        } else {
            analyzePlanet();
        }
    }

     async function handleFileUpload() {
    console.log("File detected. Starting analysis via API...");
    const file = fileInput.files[0];
    if (!file) {
        analysisResultDiv.innerHTML = `<p style="color: orange;">Please select a file first.</p>`;
        analysisResultDiv.style.display = 'block';
        return;
    }
    const formData = new FormData();
    formData.append("file", file);

    // Provide immediate feedback to the user
    analysisResultDiv.innerHTML = `<p>Analyzing light curve from ${file.name}...</p>`;
    analysisResultDiv.style.display = 'block';
    resultsSection.style.display = 'none'; // Hide the 3D sim section during analysis

    try {
        // --- MODIFICATION 1: Update the API URL ---
        // Replace this with the public URL of YOUR Hugging Face Space.
        // It looks like: https://[your-space-name]-[your-username].hf.space/predict/
        const apiUrl = "https://dipa567-exoplanetdetector.hf.space/predict/"; // <-- IMPORTANT: CHANGE THIS URL

        const response = await fetch(apiUrl, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            // Handle server errors (e.g., 500, 404)
            throw new Error(`API request failed with status: ${response.status}`);
        }

        const data = await response.json();

        // Log the actual response to see what we received
        console.log("API Prediction Response:", data);
        
        // --- MODIFICATION 2: Handle the new API response structure ---
        // Your API returns `exoplanet_probability` (a string) and `predicted_class` (a number).
        if (data.error) {
             // Handle errors returned by the API itself (e.g., wrong file type)
             throw new Error(data.error);
        }

        analysisResultDiv.innerHTML = `
            <h3>Light Curve Analysis Complete</h3>
            <p>Result: <strong>${data.interpretation}</strong></p>
            <p>Probability of Exoplanet: <strong>${data.exoplanet_probability}</strong></p>
        `;

        // --- MODIFICATION 3: Update the conditional check ---
        // The flag for your next step should check `predicted_class` being 1.
        if (data.predicted_class === 1) {
            console.log("FLAG: This is a likely exoplanet. You can proceed with further actions.");
            // You can call another function here if needed.
        }

    } catch (error) {
        console.error("Error during file analysis:", error);
        analysisResultDiv.innerHTML = `<p style="color: red;">Analysis Failed: ${error.message}</p>`;
    }
}

    // --- Analyze selected planet ---
    function analyzePlanet() {
        if (typeof getSelectedKepid !== "function") {
            alert("Search script not loaded or connected properly!");
            return;
        }

        const kepid = getSelectedKepid();
        if (!kepid) {
            alert("Please select a planet from the search first!");
            return;
        }

        // Find the planet in JSON
        const planet = planetData.find(p => p.Kepid === kepid);

        if (!planet) {
            alert("No planet data found for Kepid " + kepid);
            return;
        }

        resultsSection.style.display = 'flex';
        analysisResultDiv.style.display = 'none'; 
        resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });

        // 2. Check if we need to initialize the 3D scene
        
        if (!isSimulationInitialized) {
            if (typeof window.initSimulation === "function") {
                window.initSimulation();
                isSimulationInitialized = true;
            } else {
                alert("Simulator script is not ready yet.");
                return;
            }
        }

        window.current_planet_kepid = planet.Kepid;   
        window.pl_orbsmax = planet.features.pl_orbsmax;
        window.pl_rade    = planet.features.pl_rade;
        window.pl_masse   = planet.features.pl_masse;
        window.pl_dens    = planet.features.pl_dens;
        window.pl_eqt     = planet.features.pl_eqt;
        if (typeof window.regeneratePlanet === "function") {
            window.regeneratePlanet();
        } else {
             alert("Planet regenerator is not ready.");
        }
    }

    window.getSelectedFeatures = () => selectedFeatures;
    analyzeBtn.addEventListener("click", masterAnalyze);
    loadPlanetData();
});
