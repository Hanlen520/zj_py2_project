# -*- coding: utf-8 -*-

'''
Created on 2016-5-5

@author: zhengjin
'''

class MyRangeIterator(object):
    
    def __init__(self, n):
        self.i = 0
        self.n = n

    def __iter__(self):
        return self
    
    def next(self):
        if self.i < self.n:
            i = self.i
            self.i += 1
            return i
        else:
            raise StopIteration()

class MyRangeGenerator(object):
    
    def __init__(self, n):
        self.n = n
        
    def __iter__(self):
        for i in xrange(self.n):
            yield i


if __name__ == '__main__':
    
    my_iter_cls = MyRangeIterator(3)
    print 'Type:', type(my_iter_cls)
    for item in my_iter_cls:
        print 'item:', item
    
    my_gen_cls = MyRangeGenerator(3)
    print 'Type:', type(my_gen_cls)
    for item in my_gen_cls:
        print 'item:', item

    print 'Iterator demo done!'
    pass
