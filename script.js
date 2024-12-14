async function fetchCryptoRates() {
    try {
      const response = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd');
      const data = await response.json();
  
      // Обновление данных на странице
      document.getElementById('btc-rate').innerHTML = `BTC: <span>$${data.bitcoin.usd}</span>`;
      document.getElementById('eth-rate').innerHTML = `ETH: <span>$${data.ethereum.usd}</span>`;
    } catch (error) {
      console.error('Error fetching crypto rates:', error);
    }
  }
  
  // Запуск функции при загрузке страницы
  fetchCryptoRates();
  setInterval(fetchCryptoRates, 60000); // Обновление каждые 60 секунд
  