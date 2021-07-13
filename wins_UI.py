from flask import Flask, request
import json, logging
from wins_query import get_namelist
app = Flask(__name__)
app._config=""

@app.route('/', methods=['GET'])
def index():
    return(
            "winserver midware UI:\n"+
            "   index:\n"+
            "[GET]      1. ip:port/show\n"+
            "[GET]      2. ip:port/init\n"+
            "[POST]     3. ip:port/update\n"+
            "[POST]     4. ip:port/delete\n"+
            "[GET]      5. ip:port/namelist"
        )

@app.route('/show', methods=['GET'])
def show():
    pretty = request.args.get('pretty',"deFault")
    if (pretty == "deFault"):
        return json.dumps(app._config)
    else:
        return json.dumps(app._config,indent=4)

@app.route('/namelist', methods=['GET'])
def namelist():
    return json.dumps(get_namelist())
"""
def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                a[key] = b[key]
                #raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a
"""
@app.route("/reset", methods=['GET'])
def reset():
    
    app._config.clear()
    app._config[""]="Name, CPU" 
    return {"message":"reset complete"}

@app.route('/update', methods=['POST'])
def update():
    Name = request.form.get("ProcessName", default=None)
    Obj = request.form.getlist("Targets", default="")
    if Name == None:
        return {"error":{"code":-1,"message":"ATTRIBUT:missing_ProcessName"}}
    app._config[Name] = Obj
    return {"message":"update complete"}

@app.route('/delete', methods=['POST'])
def delete():
    Name = request.form.get("ProcessName", default=None)
    if Name == None:
        return {"error":{"code":-1,"message":"ATTRIBUT:missing_ProcessName"}}
    app._config.pop(Name, None)
    return {"message":"delete complete"}
    