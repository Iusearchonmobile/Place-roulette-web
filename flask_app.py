from flask import Flask, render_template
from lib import getrand
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getjson')
def getjson():
    res = getrand('\\n', 5, excluisons=json.loads(open('exclude.json', 'r').read()))

    exclusions = json.load(open('exclude.json', 'r'))

    with open('exclude.json', 'w') as outfile:
        exclusions.append(res['placeid'])
        json.dump(exclusions, outfile, indent=4)

    return res

if __name__ == '__main__':
    app.run()