let chart;

async function fetchCryptoRates() {
  try {
    const response = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,binancecoin,the-open-network&vs_currencies=usd,eur');
    const data = await response.json();

    // Update rates on cards
    document.getElementById('btc-rate').innerHTML = `1 BTC = $${data.bitcoin.usd} / €${data.bitcoin.eur}`;
    document.getElementById('eth-rate').innerHTML = `1 ETH = $${data.ethereum.usd} / €${data.ethereum.eur}`;
    document.getElementById('bnb-rate').innerHTML = `1 BNB = $${data.binancecoin.usd} / €${data.binancecoin.eur}`;
    document.getElementById('ton-rate').innerHTML = `1 TON = $${data['the-open-network'].usd} / €${data['the-open-network'].eur}`;

    return data; // Return data for conversion
  } catch (error) {
    console.error('Error fetching crypto rates:', error);
  }
}

async function handleConversion(event) {
  event.preventDefault();
  const cryptoType = document.getElementById('crypto-type').value;
  const amount = parseFloat(document.getElementById('amount').value);
  const currency = document.getElementById('currency').value;
  const resultDiv = document.getElementById('conversion-result');

  if (isNaN(amount) || amount <= 0) {
    resultDiv.innerHTML = '<p class="text-danger">Please enter a valid amount.</p>';
    return;
  }

  try {
    const rates = await fetchCryptoRates();
    const rate = rates[cryptoType][currency];
    const convertedAmount = (amount * rate).toFixed(2);

    resultDiv.innerHTML = `<p class="text-success">${amount} ${cryptoType.toUpperCase()} = ${convertedAmount} ${currency.toUpperCase()}</p>`;

    // Save conversion data to the database
    const response = await fetch('/api/save-conversion', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        cryptocurrency: cryptoType,
        amount: amount,
        currency: currency,
        converted_amount: convertedAmount
      })
    });

    const result = await response.json();
    if (result.status !== "success") {
      resultDiv.innerHTML += `<p class="text-danger">Error saving conversion: ${result.message}</p>`;
    }
  } catch (error) {
    console.error('Error during conversion:', error);
    resultDiv.innerHTML += '<p class="text-danger">Error during conversion. Please try again later.</p>';
  }
}

async function drawPriceChart(cryptoType = 'bitcoin') {
  try {
    const response = await fetch(`https://api.coingecko.com/api/v3/coins/${cryptoType}/market_chart?vs_currency=usd&days=7`);
    const data = await response.json();

    const labels = data.prices.map(item => new Date(item[0]).toLocaleDateString());
    const prices = data.prices.map(item => item[1]);

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

document.getElementById('crypto-type').addEventListener('change', (event) => {
  const cryptoType = event.target.value;
  drawPriceChart(cryptoType);
});

// Initialize rates, event listeners, and default price chart
fetchCryptoRates();
document.getElementById('conversion-form').addEventListener('submit', handleConversion);
drawPriceChart();