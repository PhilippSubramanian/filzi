from flask import Flask, request
import hashlib

from bot import config  # Убедись, что config содержит SECRET_1

app = Flask(__name__)

@app.route('/pay/notify', methods=['POST'])
def payment_notify():
    data = request.form
    order_id = data.get('MERCHANT_ORDER_ID')
    amount = data.get('AMOUNT')
    received_sign = data.get('SIGN')

    # Проверка подписи (FreeKassa Docs)
    sign_string = f"{config.MERCHANT_ID}:{amount}:{config.SECRET_1}:{order_id}"
    calculated_sign = hashlib.md5(sign_string.encode()).hexdigest()

    if received_sign != calculated_sign:
        return "bad sign", 403

    # Здесь можно что-то записать в базу или файл, например:
    with open("payments.log", "a", encoding='utf-8') as f:
        f.write(f"✅ Успешная оплата! Заказ: {order_id}, Сумма: {amount}₽\n")

    return "YES"

if __name__ == '__main__':
    app.run(port=5000)
