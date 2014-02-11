#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
import json

app = Flask(__name__)

f = open('output.json', 'r')
data = f.read()

bi_data = json.loads(data)

                   
@app.route('/fuzebox/analytics/bi_data', methods = ['GET'])
def get_data():
    return jsonify( { 'bi_data': bi_data } )

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route('/fuzebox/analytics/groups/<int:groupid>', methods = ['GET'])
def get_group(groupid):
    output = filter(lambda t: t['Groupid'] == int(groupid), bi_data)
    if len(output) == 0:
        abort(404)
    return jsonify( { 'output': output } )



if __name__ == '__main__':
    app.run(debug = True)





