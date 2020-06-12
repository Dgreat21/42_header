import os
import random
from datetime import datetime
from config import AUTHORS
from sys import argv


def findAllFiles(path, lst):
    dir_ = os.listdir(path)
    for node in dir_:
        if os.path.isdir(path + '/' + node):
            findAllFiles(path + '/' + node, lst)
        elif node.re('.+\.[ch]'):
            lst.append(path + '/' + node)
        else:
            continue


def cleanFile(path):
    with open(path, 'r+') as f:
        f.seek(0)
        lst = f.read().split('\n')
        flag = 0
        for i in lst[:]:
            if i.find("#") == 0 or i.find("{") == 0 or i == "/*":
                flag = 1
            if flag == 0 and (i.find('/*') == 0 or i.find('')):
                lst.remove(i)
        F = open(path,'w')
        flag = 0
        for line in lst:
            if line.find("#") == 0 or line.find("{") == 0:
                flag = 1
            if line == "" and flag == 0:
                continue
            F.write(line + '\n')


def createHeader(path, author):
    i = path.rfind('/') + 1
    filename = path[i:]

    stat = os.stat(path)
    ts = int(stat.st_birthtime)
    create = datetime.utcfromtimestamp(ts).strftime('%Y/%m/%d %H:%M:%S')
    ts = int(stat.st_mtime)
    mod = datetime.utcfromtimestamp(ts).strftime('%Y/%m/%d %H:%M:%S')

    h1 = "/* ************************************************************************** */" + '\n'
    h2 = "/*                                                                            */" + '\n'
    h3 = "/*                                                        :::      ::::::::   */" + '\n'
    h4 = "/*   %s:+:      :+:    :+:   */" % (filename.ljust(51, ' ')) + '\n'
    h5 = "/*                                                    +:+ +:+         +:+     */" + '\n'
    h6 = "/*   By: %s+#+  +:+       +#+        */" % ((author + ' <marvin@42.fr>').ljust(43, ' ')) + '\n'
    h7 = "/*                                                +#+#+#+#+#+   +#+           */" + '\n'
    h8 = "/*   Created: %s by %s#+#    #+#             */" % (create, author.ljust(18, ' ')) + '\n'
    h9 = "/*   Updated: %s by %s###   ########.fr       */" % (mod, author.ljust(17, ' ')) + '\n'
    h10 = "/*                                                                            */" + '\n'
    h11 = "/* ************************************************************************** */" + '\n'
    h = h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9 + h10 + h11
    # print(h)
    with open(path, 'r+') as f:
        lines = f.readlines()
        len_lines = len(lines)
        tmp = lines[0:len_lines-1]
        f.seek(0)
        f.writelines([h + '\n'] + tmp)


def addHeadersToDir(path):
    random.seed()
    queue = []
    findAllFiles(path, queue)
    for node in queue:
        cleanFile(node)
        createHeader(node, AUTHORS[random.randint(0, len(AUTHORS) - 1)])


for arg in argv:
    if os.path.isdir(arg):
        addHeadersToDir(arg)
    elif arg == 'header.py':
        continue
    else:
        print('"' + arg + '" isn\'t dir')
        continue
