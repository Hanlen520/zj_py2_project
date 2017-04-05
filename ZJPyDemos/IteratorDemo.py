# -*- coding: utf-8 -*-
'''
Created on 2016-5-5

@author: zhengjin
'''

class MyRangeIterator(object):
    
    def __init__(self, n):
        self.idx = 0
        self.n = n

    def __iter__(self):
        return self
    
    def next(self):
        if self.idx < self.n:
            tmp_idx = self.idx
            self.idx += 1
            return tmp_idx
        else:
            raise StopIteration()
# end class

class MyRange(object):
    
    def __init__(self, n):
        self.n = n
        
    def __iter__(self):
        return MyRangeIterator(self.n)
# end class

class MyRangeGenerator(object):
    
    def __init__(self, n):
        self.n = n
        
    def __iter__(self):
        for i in xrange(self.n):
            yield i
# end class


if __name__ == '__main__':
    
    # 1, iterate on object which includes both __iter__() and next()
    my_iter_obj = MyRangeIterator(3)
    print 'Type:', type(my_iter_obj)
    print 'Values:', [item for item in my_iter_obj]
    # Empty when loop iterator for 2nd time
    print 'Values:', [item for item in my_iter_obj]
    print '*' * 40

    # 2, iterate on object which supports __iter__()
    my_iter_obj2 = MyRange(3)
    print 'Type:', type(my_iter_obj2)
    print 'Type:', type(iter(my_iter_obj2))  # iter() calls __iter__()
    print 'Values:', [item for item in my_iter_obj2]
    # ok when loop iterator for 2nd time
    print 'Values:', [item for item in my_iter_obj2]
    print '*' * 40
    
    # 3, iterate on object which returns generator in __iter__() 
    my_iter_obj3 = MyRangeGenerator(3)
    print 'Type:', type(my_iter_obj3)
    for item in my_iter_obj3:
        print 'item:', item
    print '*' * 40

    # 4, iterate on generator
    my_gen_obj = iter(MyRangeGenerator(3))
    print 'Type:', type(my_gen_obj)
    try:
        while 1:
            print my_gen_obj.next()
    except StopIteration, e:
        print 'StopIteration!'
    print '*' * 40

    print 'Iterator demo done!'
    pass
