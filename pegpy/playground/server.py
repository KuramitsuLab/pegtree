#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import subprocess
import codecs
import json
import platform
import tempfile
from pathlib import Path

from bottle import Bottle, run, request, static_file
from pegpy.main import origami

def createResponseJson(source, result, error):
    return json.dumps({'source': source, 'result': result, 'error': error})

def createSourceFile(name, contents):
    f = codecs.open(name, 'w', 'utf-8')
    f.write(contents)
    f.close()

def compileCommand(name, target):
    t = origami({'inputs': [name]})
    with open(name + '.txt', mode = 'w') as f:
        f.write(t)
    return 0

    #return subprocess.call('pegpy origami {0} > {0}.txt'.format(name), shell=True)

def readCompiledFile(name):
    path = Path(name + '.txt')
    if path.exists():
        with path.open('r') as f:
            return f.read()
    return ''

#Server settings
app = Bottle()
rootPath = str(Path(__file__).resolve().parent)

#Server routings
@app.get('/')
def indexfile():
    return static_file('index.html', root=rootPath)

@app.post('/compile')
def compile():
    file = tempfile.NamedTemporaryFile(mode='w', suffix='.zen', prefix='tmp', dir='/tmp')
    name = file.name
    file.close() #tempfile cannot use utf-8 in python 2.7, so need to reopen

    if not hasattr(request, 'json'):
        return 'error'
    req = request.json

    createSourceFile(name, req["source"])
    message = compileCommand(name, req["option"])

    filecontent = readCompiledFile(name)
    return createResponseJson(filecontent, '', message)

@app.route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=rootPath)

def playground():
    if platform.system() == 'Darwin':
        try:
            subprocess.check_call(['open', 'http://0.0.0.0:3000'])
        except:
            pass
    run(app, host='0.0.0.0', port=3000)

if __name__ == '__main__':
    playground()
