#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Usage:
    for m in empty none one tuple named list dict flat array object slots ; do python2.6 mem.py $m 20 ; done

Change python2.6 to your version.
"""

import sys, math
import array
import collections


def pf(formatstr, *args):
    sys.stdout.write(formatstr % tuple(args))

def read_proc(path):
    if 'Java' in sys.version:
        # in Jython normal approach dont work, so here is lame workaround
        import java.io.FileReader
        f = java.io.FileReader(path)
        result = []
        ch = f.read()
        while ch >= 0:
            result.append(ch)
            ch = f.read()
        f.close()
        return ''.join([chr(i) for i in result])
    else:
        f = open(path)
        data = f.read()
        f.close()
        return data

def get_memory_usage():
    data = read_proc('/proc/self/statm')
    return float(data.split()[5]) / 256

def xy(i):
    return i * 3.14, 1.0 / (i + 1)


class A(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class B(object):
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = x
        self.y = y

C = collections.namedtuple('C', 'x y')


class MemoryUse(object):
    def __init__(self, size):
        self.size = size
        self.tab = []
    
    def repeat(self):
        if sys.version_info[0] == 2:
            return xrange(self.size)
        else:
            return  range(self.size)

    def method_none(self):
        for i in self.repeat():
            self.tab.append(None)
            
    def method_one(self):
        for i in self.repeat():
            self.tab.append(1)

    def method_tuple(self):
        for i in self.repeat():
            self.tab.append(xy(i))

    def method_named(self):
        for i in self.repeat():
            self.tab.append(C(*xy(i)))

    def method_list(self):
        for i in self.repeat():
            x, y = xy(i)
            self.tab.append([x, y])

    def method_dict(self):
        for i in self.repeat():
            x, y = xy(i)
            self.tab.append({'x': x, 'y': y})

    def method_flat(self):
        for i in self.repeat():
            x, y = xy(i)
            self.tab.append(x)
            self.tab.append(y)

    def method_array(self):
        self.tab = array.array('d')
        for i in self.repeat():
            x, y = xy(i)
            self.tab.append(x)
            self.tab.append(y)

    def method_object(self):
        for i in self.repeat():
            self.tab.append(A(*xy(i)))

    def method_slots(self):
        for i in self.repeat():
            self.tab.append(B(*xy(i)))


if __name__ == '__main__':
    mem_start = get_memory_usage()

    method  = sys.argv[1]
    
    if method == 'empty':
        sizelog, size = 0, 1
        mem_usage = mem_start
    else:
        sizelog = int(sys.argv[2])
        size    = 2 ** sizelog

        mem = MemoryUse(size)
        getattr(mem, 'method_' + method)()

        mem_total = get_memory_usage()
        mem_usage = mem_total - mem_start

    pf("%-6s  %2i    %7.2f  %i\n", method, sizelog, mem_usage, math.trunc(mem_usage * 2 ** 20 / size))

