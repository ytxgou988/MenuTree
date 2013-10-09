#!/usr/bin/python

import os, sys, time, subprocess, re

# recursive list all items by given directory
def traversal(dir):
    rc = []
    for dirname, dirnames, filenames in os.walk(dir):
        for subdirname in dirnames:
            rc.append((os.path.join(dirname, subdirname), 'dir'))
        for filename in filenames:
            rc.append((os.path.join(dirname, filename), 'file'))
    return rc

# recursive list all png files by given directory
def traversal_by_ext(dir, ext):
    rc = []
    for dirname, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            path = os.path.join(dirname, filename)
            path = path.replace(dir, '.')
            file, extension = os.path.splitext(path)
            if extension.upper() == ext.upper(): rc.append(path)
    return rc

def traversal_by_exts(dir, exts):
    rc = []
    for dirname, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            path = os.path.join(dirname, filename)
            path = path.replace(dir, '.')
            file, extension = os.path.splitext(path)
            E = []
            for e in exts: E.append(e.upper())
            if extension.upper() in E: rc.append(path)
    return rc


def rmdir(d):
    if os.name in ['posix', 'mac']:
        subprocess.call(['rm', '-rf', d])
    elif os.name in ['nt']:
        subprocess.call(["rmdir", "/S", "/Q", d], shell=True)
    else:
        print 'unsupport rmdir in %s' % os.name


def mkdir(d):
    if os.name in ['posix', 'mac']:
        subprocess.call(['mkdir', '-p', d])
    elif os.name in ['nt']:
        subprocess.call(["mkdir", "", d], shell=True)
    else:
        print 'unsupport rmdir in %s' % os.name


def mvdir(d, x):
    if os.name in ['posix', 'mac']:
        subprocess.call(['mv', d, x])
    elif os.name in ['nt']:
        subprocess.call(["move", d, x], shell=True)
    else:
        print 'unsupport rmdir in %s' % os.name

def tok():
    if os.name in ['posix', 'mac']:
        tok = '/'
    elif os.name in ['nt']:
        tok = '\\'
    else:
        tok = '/'
    return tok


def compose(args):
    rc = ""
    for arg in args:
        rc += arg+tok()
    return rc[:-1]


def filesplit(file):
    return file.rsplit(tok(), 1)


def create_newpath(path, suffix):
    if path[-1] == tok(): path = path[:-1]
    return "%s_%s_%s%s" % (path, suffix, time.strftime('%Y%m%d_%H%M%S'), tok())


def load_languages(path):
    langf = open("languages1.cfg")
    rc = langf.readlines()
    items = []
    empty = re.compile(" ")
    ret = re.compile("\n")
    for l in rc:
        l = empty.sub("",l)
        l = ret.sub("",l)
        if l.startswith('.') : continue
        if '#' in l : continue
        if l == '' : continue
        items.append(l)
    langf.close()
    return items

def load_packages(path):
    langf = open("packages1.cfg")
    rc = langf.readlines()
    items = []
    empty = re.compile(" ")
    ret = re.compile("\n")
    for l in rc:
        l = empty.sub("",l)
        l = ret.sub("",l)
        if l.startswith('.') : continue
        if '#' in l : continue
        if l == '' : continue
        items.append(l)
    langf.close()
    return items

def find_min(display):
    min = 99999
    rc = None
    for d in display:
        if d[0] < min:
            min = d[0]
            rc = d
    return rc



if __name__ == '__main__' :

    print '#'*80
    print 'test traversal()'
    for item in traversal('.') : print item

    print '#'*80
    print 'test traversal_by_ext()'
    for item in traversal_by_ext('.', '.png') : print item
