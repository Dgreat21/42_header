from os.path import isfile
from sys import argv

if len(argv) > 1:
    if isfile(argv[1]):
        au = open(argv[1])
else:
    if isfile('author'):
        au = open('author')
    else:
        print('No author file found\n'
              ' Usage: python authors.py or python authors.py [path to author]')
        quit()
f = open('config.py', 'w')
buf = au.read().split('\n')
try:
    buf.remove('')
except ValueError as error:
    pass
res = "AUTHORS = ["
buff_len = len(buf)
for i, author in enumerate(buf):
    if i != buff_len - 1:
        res += '\'' + author + '\', '
    else:
        res += '\'' + author + '\''
res += ']\n'
print(res)
f.write(res)
