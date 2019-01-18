#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import subprocess
import codecs
import json
import platform
import tempfile
from pathlib import Path
from datetime import datetime

from bottle import Bottle, request, static_file

#Server settings
app = Bottle()
rootPath = str(Path(__file__).resolve().parent)
root = datetime.now().strftime('?%Y%m%d%H%M%S')
url = 'http://0.0.0.0:3000' + root
edit_name = ''
new_edit_name = ''
comp = None
p_arg = None
cmd = []
init_cmd = ''

#Server routings
@app.get('/')
def indexfile():
    return static_file('index.html', root=rootPath)

@app.post('/compile')
def compile():
    if not hasattr(request, 'json'):
        return createResponseJson('', 'ajex error', 'content error: not json type')
    req = request.json

    file = tempfile.NamedTemporaryFile(mode='w', suffix='.zen', prefix='tmp', dir='/tmp')
    editer = file.name
    file.close() #tempfile cannot use utf-8 in python 2.7, so need to reopen

    createSourceFile(editer, req['source'])
    if edit_name:
        path = file_search2(edit_name)
        if path is not None:
            with path.open('w') as f:
                f.write(req['source'])

    try:
        return createResponseJson('', compileCommand(editer, cmd), '')
    except Exception as e:
        return createResponseJson('', 'compile error in python\n\n' + str(e), str(e))

@app.post('/command')
def command():
    if not hasattr(request, 'json'):
        return createResponseJson('', 'ajex error', 'content error: not json type')
    req = request.json

    file = tempfile.NamedTemporaryFile(mode='w', suffix='.zen', prefix='tmp', dir='/tmp')
    editer = file.name
    file.close() #tempfile cannot use utf-8 in python 2.7, so need to reopen

    global cmd, edit_name, new_edit_name
    new_edit_name = ''
    cmd2 = req['cmd'].strip().split(' ')
    cmd = cmd2[:2] + restore_arg(p_arg(cmd2[2:]))

    if new_edit_name != edit_name:
        edit_name = new_edit_name
        write_inputs([edit_name])
        with file_search('input.k').open() as f:
            input = f.read()
            createSourceFile(editer, input)
    else:
        input = ''
        createSourceFile(editer, req['source'])
        if edit_name:
            path = file_search2(edit_name)
            if path is not None:
                with path.open('w') as f:
                    f.write(req['source'])

    try:
        return createResponseJson(input, compileCommand(editer, cmd), '')
    except Exception as e:
        return createResponseJson(input, 'compile error in python\n\n' + str(e), str(e))

@app.route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=rootPath)

@app.post('/close')
def close():
    app.close()
    write_inputs([])
    write_inputs([], 'output.k')
    sys.stderr.close()

@app.post('/init')
def init():
    with file_search('input.k').open() as f:
        input = f.read()
    return json.dumps({'cmd': init_cmd, 'input': input})

def createResponseJson(input, output, error):
    return json.dumps({'input': input, 'output': output, 'error': error})

def createSourceFile(editer, contents):
    with codecs.open(editer, 'w', 'utf-8') as f:
        f.write(contents)

def compileCommand(editer, cmd):
    d = p_arg(cmd[2:])
    w = comp(cmd[:2] + restore_arg(d) + ([] if 'output' in d else ['-o', str(file_search('output.k'))]) + ([] if edit_name else [editer]))
    w.file.seek(0)
    cont = w.file.read()
    w.file.close()
    return cont

def file_search(file, subdir = 'sample'):
    return Path(__file__).resolve().parent / subdir / file

def file_search2(file):
    path = Path(file)
    if path.exists():
        return path
    for dir in ['sample', '../grammar', '../origami']:
        path = file_search(file, dir)
        if path.exists():
            return path
    return None

def write_inputs(datas, name = 'input.k'):
    text = ''
    for d in datas:
        if d == 'edit': continue

        path = file_search2(d)
        if path is None:
            text += d + '\n'
        else:
            with path.open() as f:
                text += f.read() + '\n'

    with file_search(name).open(mode = 'w') as f:
        f.write(text)

restore_data = {
    'grammar': '-g',
    'start': '-s',
    'output': '-o',
    'extension': '-X',
    'option': '-D',
    'inputs': '',
}

def parse_name(name):
    global new_edit_name
    if ':' in name:
        _, name = name.split(':')
        new_edit_name = name
    return name

def restore_arg(d, data = restore_data):
    arg = []
    for key, pre in data.items():
        if key not in d:
            continue
        if pre:
            arg.append(pre)
            arg.append(parse_name(d[key]))
        else:
            for name in d[key]:
                name = parse_name(name)
                if name and name != 'edit':
                    file = file_search2(name)
                    arg.append(str(file) if file is not None else name)
    return arg

def playground(argv, main, parse_arg):
    global comp, cmd, p_arg, edit_name, new_edit_name, init_cmd
    init_cmd = ' '.join(argv[:-1] if argv[-1] == 'edit' else argv)
    cmd = argv[:2] + restore_arg(parse_arg(argv[2:]))
    edit_name = new_edit_name
    comp = main
    p_arg = parse_arg
    write_inputs([edit_name] if edit_name else [])

    if platform.system() == 'Darwin':
        try:
            subprocess.check_call(['open', url])
        except:
            pass
    app.run(host='0.0.0.0', port=3000)
    write_inputs([])
    write_inputs([], 'output.k')
