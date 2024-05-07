import os
import re
import json
import shutil
from glob import glob
from subprocess import run
from subprocess import PIPE

# reads a file
def read(filename):
    f = open(filename, 'r')
    text = f.read()
    f.close()
    return text.strip()


# writes json
def write_json(data, filename):
    f = open(filename, 'w')
    f.write(json.dumps(data))
    f.close()


# reads a json
def read_json(filename):
    f = open(filename, 'r')
    text = f.read()
    f.close()
    return json.loads(text)


# parse a json string
def parse_json(text):
    return json.loads(text)


# lists all files in dir
def ls(dir='.', files=[]):
    for e in glob(os.path.join(dir, '*')):
        if os.path.isdir(e):
            ls(dir=e, files=files)
        else:
            files.append(e)
    return files


# removes a directory
def delete_dir(dir):
    shutil.rmtree(dir)


# removes a file
def delete_file(f):
    os.remove(f)


# expected files
def expected_files(files, dir='.'):
    dirfiles = ls(dir=dir)
    not_found = []
    for f in files:
        if f not in dirfiles:
            not_found.append(f)
    return not_found


# executes a shell command
def execute(cmd=[], shell=False, dir='.', input=None, encoding='ascii', timeout=5):
    return run(cmd, shell=shell, stdout=PIPE, stderr=PIPE, input=input, cwd=dir, timeout=timeout)


# makes a target
def make(target=''):
    return execute(cmd=['make', target])


# parses a form
def parse_form(f):
    f = open(f, 'r', encoding='latin1')
    p = re.compile(r'^[0-9]+( )*:[a-zA-Z0-9, ]+$')
    lookup = {}
    for line in f:
        line = line.strip()
        if p.search(line) is not None:
            vals = line.split(':')
            lookup[vals[0].strip()] = vals[1].strip()
    return lookup


# passed message
def passed(*args):
    if len(args) > 0:
        return 'passed: ' + args[0]
    return 'passed'


# failed message
def failed(*args):
    if len(args) > 0:
        return 'failed: ' + args[0]
    return 'failed'


# incomplete message
def incomplete(*args):
    if len(args) > 0:
        return 'incomplete: ' + args[0]
    return 'incomplete'


# creates a compilation error msg
def create_error(filename, msg):
    if msg != '':
        return '[%s]\n\n%s\n' % (filename, msg)
    return ''


# creates a pretty result report
def report(table):
    result = ''
    for (name, grade, status) in table:
        result += '%24s: %6s [ %2d ]\n' % (name, status, grade)
    return result.rstrip()


# writes autograder result
def write_result(grade, msg):
    write_json({'grade': grade, 'output': msg}, 'result.json')
