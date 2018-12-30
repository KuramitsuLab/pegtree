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
from datetime import datetime

from bottle import Bottle, run, request, static_file

from pegpy.utils import find_path

def createResponseJson(source, result, error):
    return json.dumps({'source': source, 'result': result, 'error': error})

def createSourceFile(name, contents):
    f = codecs.open(name, 'w', 'utf-8')
    f.write(contents)
    f.close()

comp = None

def compileCommand(name, cmd):
    cmd2 = cmd.strip().split(' ')
    if '-o' in cmd2 or '--output' in cmd2:
        w = comp(['dummy'] + cmd2 + [name])
    else:
        w = comp(['dummy'] + cmd2 + ['-o', str(file_search('input.k')), name])
    w.file.seek(0)
    return w.file.read()

#Server settings
app = Bottle()
rootPath = str(Path(__file__).resolve().parent)
root = datetime.now().strftime('?%Y%m%d%H%M%S')

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

    try:
        filecontent = compileCommand(name, req['cmd'])
        message = ''
    except Exception as e:
        filecontent = 'compile error in python'
        message = str(e)

    return createResponseJson(filecontent, '', message)

@app.route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=rootPath)

@app.post('/sample/ifexpr')
def get_ifexpr():
    with file_search('ifexpr.k').open() as f:
        return f.read()

@app.post('/sample/fib')
def get_fib():
    with file_search('fib.k').open() as f:
        return f.read()

@app.post('/sample/input')
def get_ifexpr():
    with file_search('input.k').open() as f:
        return f.read()

@app.post('/save')
def saveFile():
    if not hasattr(request, 'json'):
        return 'error'
    req = request.json
    cmd = req['cmd'].split(' ')
    out = ''
    for i in range(len(cmd)):
        if (cmd[i] == '-o' or cmd[i] == '--output') and i+1 < len(cmd):
            out = cmd[i+1]

    if out:
        with Path(out).open(mode = 'w') as f:
            f.write(req['source'])
    return 'success'

cmd = ''

@app.post('/init')
def init():
    return json.dumps({'cmd': cmd})

def file_search(file, subdir = 'sample'):
    return Path(__file__).resolve().parent / subdir / file

def write_inputs(datas, file = file_search('input.k')):
    text = ''
    for d in datas:
        try:
            with find_path(d, subdir='playground/sample').open() as f:
                text += f.read() + '\n'
                continue
        except:
            pass
        try:
            with find_path(d, subdir='grammar').open() as f:
                text += f.read() + '\n'
                continue
        except:
            pass
        text += d + '\n'

    with file.open(mode = 'w') as f:
        f.write(text)

def playground(argv, main):
    global comp, cmd, grammar, output
    write_inputs(list(map(lambda x: x[5:], list(filter(lambda x: x.startswith('edit:'), argv)))))
    arg = list(map(lambda x: x.replace('edit:', '').replace('edit', ''), argv[1:]))

    cmd = ' '.join(arg)
    comp = main

    if platform.system() == 'Darwin':
        try:
            subprocess.check_call(['open', 'http://0.0.0.0:3000' + root])
        except:
            pass
    run(app, host='0.0.0.0', port=3000)
    write_inputs([])
