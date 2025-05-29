from flask import Flask, request
import threading, time, requests, os

app = Flask(__name__)
last_ping_time = time.time()
CHECK_INTERVAL = 60
PING_TIMEOUT = 180
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_alert():
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    requests.post(url, data={'chat_id': CHAT_ID, 'text': '⚠️ Нет сигнала от ESP! Возможно, отключилось питание.'})

def monitor():
    global last_ping_time
    alerted = False
    while True:
        time.sleep(CHECK_INTERVAL)
        if time.time() - last_ping_time > PING_TIMEOUT and not alerted:
            send_alert()
            alerted = True
        elif time.time() - last_ping_time <= PING_TIMEOUT:
            alerted = False

@app.route('/ping')
def ping():
    global last_ping_time
    last_ping_time = time.time()
    return 'OK'

if __name__ == '__main__':
    threading.Thread(target=monitor, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)