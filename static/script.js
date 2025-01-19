// Fetch data from the Flask server
fetch("/data")
    .then(response => {
        if (!response.ok) {
            throw new Error("Brak danych! Dane nie zostały jeszcze pobrane.");
        }
        return response.json();
    })
    .then(data => {
        console.log("Otrzymane dane z API:", data);

        // Filtrowanie danych dla drużyny domowej i wyjazdowej
        const homePlayers = data["Team"].map((team, index) => (team === "Home" ? index : null)).filter(x => x !== null);
        const awayPlayers = data["Team"].map((team, index) => (team === "Away" ? index : null)).filter(x => x !== null);

        const homeLabels = homePlayers.map(index => data["Player Name"][index]);
        const homeDurations = homePlayers.map(index => data["Duration"][index]);
        const awayLabels = awayPlayers.map(index => data["Player Name"][index]);
        const awayDurations = awayPlayers.map(index => data["Duration"][index]);

        // Wykres kołowy dla drużyny domowej
        const homePieTrace = {
            labels: homeLabels,
            values: homeDurations,
            type: "pie",
            textinfo: "label+percent",
            hoverinfo: "label+value",
            name: "Home Team"
        };

        const homePieLayout = {
            title: "Procentowy Czas Gry - Drużyna Domowa"
        };

        Plotly.newPlot("home-pie-chart", [homePieTrace], homePieLayout);

        // Wykres kołowy dla drużyny wyjazdowej
        const awayPieTrace = {
            labels: awayLabels,
            values: awayDurations,
            type: "pie",
            textinfo: "label+percent",
            hoverinfo: "label+value",
            name: "Away Team"
        };

        const awayPieLayout = {
            title: "Procentowy Czas Gry - Drużyna Wyjazdowa"
        };

        Plotly.newPlot("away-pie-chart", [awayPieTrace], awayPieLayout);
    })
    .catch(error => {
        console.error("Błąd:", error.message);
        document.getElementById("chart-container").innerHTML = `<h2>${error.message}</h2>`;
    });
