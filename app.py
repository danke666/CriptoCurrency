from flask import Flask, jsonify, render_template, request
from server.db_operations import get_price_history, insert_conversion
import logging

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/price-history/<cryptocurrency>")
def price_history(cryptocurrency):
    data = get_price_history(cryptocurrency)
    return jsonify(data)

@app.route("/api/save-conversion", methods=['POST'])
def save_conversion():
    data = request.get_json()
    app.logger.debug(f"Получены данные конвертации: {data}")
    if not data:
        app.logger.error("JSON данные не получены")
        return jsonify({"status": "fail", "message": "Данные не предоставлены"}), 400
    required_fields = ['cryptocurrency', 'amount', 'currency', 'converted_amount']
    if not all(field in data for field in required_fields):
        app.logger.error("Отсутствуют обязательные поля")
        return jsonify({"status": "fail", "message": "Отсутствуют обязательные поля"}), 400
    try:
        insert_conversion(data['cryptocurrency'], data['amount'], data['currency'], data['converted_amount'])
        app.logger.debug("Данные конвертации успешно сохранены")
        return jsonify({"status": "success"}), 200
    except Exception as e:
        app.logger.error(f"Ошибка при сохранении данных: {e}")
        return jsonify({"status": "fail", "message": "Ошибка при сохранении данных"}), 500

if __name__ == "__main__":
    app.run(debug=True)