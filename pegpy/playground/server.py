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
from importlib import import_module
from pathlib import Path

from bottle import Bottle, run, request, static_file

from pegpy.main import read_inputs

def createResponseJson(source, result, error):
    return json.dumps({'source': source, 'result': result, 'error': error})

def createSourceFile(name, contents):
    f = codecs.open(name, 'w', 'utf-8')
    f.write(contents)
    f.close()

comp = None
compname = ''
grammar = ''

def compileCommand(name, target, grammar):
    t = comp({'inputs': [name, target + '.origami'] if compname == 'origami' else [name], 'grammar': grammar})
    with open(name + '.txt', mode = 'w') as f:
        f.write(t)
    return ''

def readCompiledFile(name):
    path = Path(name + '.txt')
    if path.exists():
        with path.open() as f:
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

    createSourceFile(name, req['source'])
    global compname
    if compname != req['mode']:
        global comp
        compname = req['mode']
        comp = getattr(import_module('pegpy.main'), compname)

    try:
        message = compileCommand(name, req['target'], req['syntax'])
    except Exception as e:
        message = str(e)

    filecontent = readCompiledFile(name)
    return createResponseJson(filecontent, '', message)

@app.route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=rootPath)

@app.post('/sample/ifexpr')
def get_ifexpr():
    with file_search('ifexpr.k').open() as f:
        return f.read()

@app.post('/sample/input')
def get_ifexpr():
    with file_search('input.k').open() as f:
        return f.read()

@app.post('/init')
def init():
    return json.dumps({'mode': compname, 'syntax': grammar, 'target': ''})

def file_search(file, subdir = 'sample'):
    return Path(__file__).resolve().parent / subdir / file

def write_inputs(datas, file = file_search('input.k')):
    with file.open(mode = 'w') as f:
        text = ''
        for d in datas:
            if not d or d == 'playground':
                continue
            text += read_inputs(d) + '\n'
        #f.write(reduce(lambda x, y: x + '\n' + read_inputs(y), datas[1:], read_inputs(datas[0])))
        f.write(text)

def playground(cmd = 'origami', opt = {'inputs': [], 'grammar': 'konoha6.tpeg'}):
    global comp, compname, grammar
    for name in [cmd] + opt['inputs']:
        if name in dir(import_module('pegpy.main')):
            comp = getattr(import_module('pegpy.main'), name)
            compname = name
            break
    if comp is None:
        print('import error', [cmd] + opt['inputs'])
        return
    grammar = opt['grammar'] if 'grammar' in opt else 'konoha6.tpeg'

    write_inputs(opt['inputs'])

    if platform.system() == 'Darwin':
        try:
            subprocess.check_call(['open', 'http://0.0.0.0:3000'])
        except:
            pass
    run(app, host='0.0.0.0', port=3000)
    write_inputs([])

if __name__ == '__main__':
    playground()
