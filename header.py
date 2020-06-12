import re
import os
import random
from datetime import datetime
from config import AUTHORS
from sys import argv


def findAllFiles(path, lst):
    if os.path.isdir(path):
        dir_ = os.listdir(path)
    elif os.path.isfile(path) and re.match('.+\.[ch]', path):
        lst.append(path)
        return
    else:
        return
    for node in dir_:
        if os.path.isdir(path + '/' + node) and (node != 'external' or node != '.git'):
            findAllFiles(path + '/' + node, lst)
        elif re.match('.+\.[ch]', node):
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
    h = """/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   {filename}:+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: {author}+#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: {time_cr} by {author_cr}#+#    #+#             */
/*   Updated: {time_upd} by {author_upd}###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
"""
    h = h.format(
        filename=filename.ljust(51, ' '),
        author=(author + ' <marvin@42.fr>').ljust(43, ' '),
        time_cr=create,
        author_cr=author.ljust(18, ' '),
        time_upd=mod,
        author_upd= author.ljust(17, ' ')
    )
    # print(h)
    with open(path, 'r+') as f:
        lines = f.readlines()
        len_lines = len(lines)
        len_lines -= 1
        tmp = lines[0:len_lines]
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
    if os.path.isdir(arg) or os.path.isfile(arg):
        addHeadersToDir(arg)
    elif arg == 'header.py':
        continue
    else:
        print('"' + arg + '" isn\'t directory or file')
        continue
