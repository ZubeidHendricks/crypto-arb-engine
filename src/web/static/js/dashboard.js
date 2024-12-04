// WebSocket connection
const ws = new WebSocket(`ws://${window.location.host}/ws`);

// Update UI with real-time data
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    updateDashboard(data);
};

// Update dashboard components
function updateDashboard(data) {
    // Update status cards
    document.getElementById('engineStatus').textContent = data.status;
    document.getElementById('activeOpportunities').textContent = data.opportunities.length;
    document.getElementById('dailyProfit').textContent = 
        `$${data.metrics.total_profit_24h.toFixed(2)}`;

    // Update opportunities table
    updateOpportunitiesTable(data.opportunities);

    // Update charts
    updateProfitChart(data.metrics.profit_history);
    updateVolumeChart(data.metrics.volume_by_exchange);
}

// Update opportunities table
function updateOpportunitiesTable(opportunities) {
    const tbody = document.getElementById('opportunitiesTable');
    tbody.innerHTML = '';

    opportunities.forEach(opp => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="px-6 py-4">${opp.symbol}</td>
            <td class="px-6 py-4">${opp.buy_exchange}</td>
            <td class="px-6 py-4">${opp.sell_exchange}</td>
            <td class="px-6 py-4 ${opp.profit > 1 ? 'text-green-600' : 'text-red-600'}">
                ${opp.profit.toFixed(2)}%
            </td>
            <td class="px-6 py-4">${opp.volume.toFixed(4)}</td>
            <td class="px-6 py-4">
                <button onclick="executeArbitrage(${JSON.stringify(opp)})" 
                        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                    Execute
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Execute arbitrage opportunity
async function executeArbitrage(opportunity) {
    try {
        const response = await fetch('/api/execute-arbitrage', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(opportunity),
        });

        const result = await response.json();
        if (result.success) {
            alert('Arbitrage execution started!');
        } else {
            alert(`Error: ${result.error}`);
        }
    } catch (error) {
        alert(`Error executing arbitrage: ${error.message}`);
    }
}

// Initialize and update profit chart
function updateProfitChart(profitHistory) {
    const trace = {
        x: profitHistory.map(p => p.timestamp),
        y: profitHistory.map(p => p.profit),
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Profit',
        line: {
            color: '#10B981',
            width: 2
        }
    };

    const layout = {
        title: 'Profit History (24h)',
        xaxis: {
            title: 'Time'
        },
        yaxis: {
            title: 'Profit ($)'
        },
        margin: { t: 30 }
    };

    Plotly.newPlot('profitChart', [trace], layout);
}

// Initialize and update volume chart
function updateVolumeChart(volumeData) {
    const trace = {
        x: Object.keys(volumeData),
        y: Object.values(volumeData),
        type: 'bar',
        marker: {
            color: '#60A5FA'
        }
    };

    const layout = {
        title: 'Trading Volume by Exchange',
        xaxis: {
            title: 'Exchange'
        },
        yaxis: {
            title: 'Volume (USD)'
        },
        margin: { t: 30 }
    };

    Plotly.newPlot('volumeChart', [trace], layout);
}
