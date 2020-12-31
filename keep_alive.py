#a file used to keep the bot alive, even when the file isn't open and running. This is done by using UptimeRobot.com
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return "Hello, I am alive!"

def run():
  app.run(host='0.0.0.0',port=8000)

def keep_alive():
  t = Thread(target=run)
  t.start()
