#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import commands
import codecs
import json

def CreateResponseJson(source, result, error):
    return json.dumps({'source': source, 'result': result, 'error': error})

def CreateSourceFile(name, contents):
    f = codecs.open(name, 'w', 'utf-8')
    f.write(contents)
    f.close()

def Compile(name, target):
    return commands.getoutput('java -jar /usr/local/bin/libzen.jar -l ' + target+ ' '+ name + ' > ' + name + '.txt')


if __name__ == '__main__':
    print "Content-Type: application/json"
    print ""

    if os.environ['REQUEST_METHOD'] != "POST":
        print '{\'error\':No Method Error\' }'
        sys.exit()

    name = commands.getoutput("/bin/mktemp -q /tmp/XXXXXX.zen")
    req = json.load(sys.stdin)

    CreateSourceFile(name, req["source"])
    message = Compile(name, req["option"])

    filecontent = ''
    compile_flag = os.path.exists(name+".txt")
    if compile_flag:
        a = open(name+'.txt', 'r')
        filecontent = a.read()

    print CreateResponseJson(filecontent, '', message)
