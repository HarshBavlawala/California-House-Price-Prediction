document.getElementById("predictForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    
    const payload = {
        longitude: parseFloat(document.getElementById("longitude").value),
        latitude: parseFloat(document.getElementById("latitude").value),
        housing_median_age: parseFloat(document.getElementById("housing_median_age").value),
        total_rooms: parseFloat(document.getElementById("total_rooms").value),
        total_bedrooms: parseFloat(document.getElementById("total_bedrooms").value),
        population: parseFloat(document.getElementById("population").value),
        households: parseFloat(document.getElementById("households").value),
        median_income: parseFloat(document.getElementById("median_income").value),
        ocean_proximity: document.getElementById("ocean_proximity").value
    };

    try {
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        const resultDiv = document.getElementById("result");
        resultDiv.style.display = "block";
        resultDiv.innerText = "Estimated Value: $" + data.predicted_price.toLocaleString();
    } catch (error) {
        const resultDiv = document.getElementById("result");
        resultDiv.style.display = "block";
        resultDiv.innerText = "Error: Backend server (uvicorn) start karein!";
    }
});