from flask import Flask
import random
app = Flask(__name__)

@app.route('/num')
def num():
    return random.randrange(1, 100)

@app.route('/name')
def name():
    return "A Developer"

if __name__=='__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=8000)
