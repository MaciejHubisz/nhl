// Fetch data from the Flask server
fetch("/data")
    .then(response => response.json())
    .then(data => {
        // Przygotowanie danych
        const labels = data["Player Name"];
        const shiftCounts = data["Shift #"];
        const durations = data["Duration"];

        // Wykres słupkowy
        const barTrace = {
            x: labels,
            y: shiftCounts,
            type: "bar",
            marker: {
                color: "rgba(55, 128, 191, 0.7)",
                line: { color: "rgba(55, 128, 191, 1.0)", width: 2 }
            },
            name: "Shifts"
        };

        const barLayout = {
            title: "Liczba Shiftów dla Zawodników",
            xaxis: { title: "Zawodnicy" },
            yaxis: { title: "Liczba Shiftów" }
        };

        Plotly.newPlot("bar-chart", [barTrace], barLayout);

        // Wykres kołowy
        const pieTrace = {
            labels: labels,
            values: durations,
            type: "pie",
            textinfo: "label+percent",
            hoverinfo: "label+value"
        };

        const pieLayout = {
            title: "Procentowy Czas Gry dla Zawodników"
        };

        Plotly.newPlot("pie-chart", [pieTrace], pieLayout);
    })
    .catch(error => console.error("Error fetching data:", error));
