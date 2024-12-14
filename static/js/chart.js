async function drawPriceChart(cryptoType = 'bitcoin') {
    try {
        const response = await fetch(`/api/price-history/${cryptoType}`);
        const data = await response.json();

        const labels = data.map(item => new Date(item[0]).toLocaleString());
        const prices = data.map(item => item[1]);

        const ctx = document.getElementById('priceChart').getContext('2d');
        if (chart) chart.destroy();

        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: `${cryptoType.charAt(0).toUpperCase() + cryptoType.slice(1)} Price History`,
                    data: prices,
                    borderColor: '#ff9900',
                    backgroundColor: 'rgba(255, 153, 0, 0.2)',
                    tension: 0.2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error fetching price chart data:', error);
    }
}
