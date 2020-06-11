import os
import random
from datetime import datetime
from config import AUTHORS


def find_all_files(path, lst):
    dir_ = os.listdir(path)
    for node in dir_:
        if os.path.isdir(path + '/' + node):
            find_all_files(path + '/' + node, lst)
        elif node.find('.c') or node.find('.h'):
            lst.append(path + '/' + node)
        else:
            continue


def clean_header(path):
    with open(path, 'r+') as f:
        f.seek(0)
        lst = f.read().split('\n')
        for i in lst[:]:
            if i.find('/*') == 0 or i.find(''):
                lst.remove(i)
        F = open(path,'w')
        for i in lst:
            if i != "":
                F.write(i + '\n')


def create_header(path, author):
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
    h6 = "/*   By: %s+#+  +:+       +#+        */" % (author + ' <marvin@42.fr>'.ljust(37, ' ')) + '\n'
    h7 = "/*                                                +#+#+#+#+#+   +#+           */" + '\n'
    h8 = "/*   Created: %s by %s#+#    #+#             */" % (create, author.ljust(18, ' ')) + '\n'
    h9 = "/*   Updated: %s by %s###   ########.fr       */" % (mod, author.ljust(17, ' ')) + '\n'
    h10 = "/*                                                                            */" + '\n'
    h11 = "/* ************************************************************************** */" + '\n'
    h = h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9 + h10 + h11
    with open(path, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.writelines([h + '\n'] + lines)


random.seed()
queue = []
find_all_files('/Volumes/Storage/RT/utils', queue)
for node in queue:
    clean_header(node)
    create_header(node, AUTHORS[random.randint(0, len(AUTHORS) - 1)])
