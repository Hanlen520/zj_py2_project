# -*- coding: utf-8 -*-

'''
Created on 2016-5-5

@author: zhengjin
'''

class ZrangeIterator:
    
    def __init__(self, n):
        self.i = 0
        self.n = n

#     def __iter__(self):
#         return self
    
    def next(self):
        if self.i < self.n:
            i = self.i
            self.i += 1
            return i
        else:
            raise StopIteration()

class Zrange:
    
    def __init__(self, n):
        self.n = n
        
    def __iter__(self):
        return ZrangeIterator(self.n)
#         return iter(ZrangeIterator(self.n))


if __name__ == '__main__':
    
    zrange = Zrange(3)
    
    print zrange is iter(zrange)
    print zrange
    print iter(zrange)
    
    print [i for i in zrange]
    print [i for i in zrange]

    print 'Iterator demo done!'
    pass