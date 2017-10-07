from flask import Flask, request, jsonify
import json
from scrape_attack import Attack
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app)
att = Attack()

@app.route('/login',methods=['POST'])
def login ():
    if request.method == 'POST':
        if request.form['username'] == 'tester' and request.form['password'] == 'no-secret' :
            return json.dumps({"success": true})
        else:
            return json.dumps({"success": false})

@app.route('/data/<register>',methods = ['GET'])
def send_data():
    test_obj = {}
    test_obj['GPA'] = 8.5
    test_obj['name'] = 'Tester_'+register
    test_obj['register'] = register
    test_obj['CGPA'] = 8.5
    return json.dumps(test_obj)

@app.route('/pull',methods = ['POST'])
def pull_data():
    content = request.get_json()
    print (content)
    data = {}
    data = att.attack(content['reg'],content['dob'])
    return jsonify(data)

app.run()
