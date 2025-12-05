from flask import Flask, render_template, request
from lib import getrand
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getjson')
def getjson():
    plrsunder = request.args.get('plrsunder')
    plrsover = request.args.get('plrsover')
    keyword = request.args.get('keyword')

    if not plrsunder: plrsunder = 5
    if not plrsover: plrsover = 5
    if not keyword: keyword = '\\n'

    plrsunder = int(plrsunder)
    plrsover = int(plrsover)
    keyword = str(keyword)

    res = getrand(keyword, plrsunder, plrsover, excluisons=json.loads(open('exclude.json', 'r').read()))

    exclusions = json.load(open('exclude.json', 'r'))

    with open('exclude.json', 'w') as outfile:
        exclusions.append(res['placeid'])
        json.dump(exclusions, outfile, indent=4)

    return res

if __name__ == '__main__':
    app.run()
