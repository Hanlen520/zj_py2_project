# -*- coding: utf-8 -*-
'''
Created on 2017-4-2

@author: Vieira
'''

# EXAMPLE 01, method override
# def my_func(name):
#     print 'Hello,', name
# 
# def deco_func(func):
#     print 'in deco func'
#     
#     def in_deco_func(name):
#         print'in in_deco_func'
#         func(name)
# 
#     return in_deco_func
# # end deco_func()
# 
# # 1
# my_func('Test')
# print '*' * 30
# 
# my_func = deco_func(my_func)
# my_func('test override')
# print '*' * 30
# 
# # 2
# @deco_func
# def my_new_func(name):
#     print 'New, hello,', name
# 
# my_new_func('test @deco')


# EXAMPLE 02, method override in class
class OverrideTest(object):

    def check(self):
        ''' only be invoked at first time'''
        print 'check Invoked'
        self.check = self.check_post  # re-assign

    def check_post(self):
        print 'check_post Invoked'

my_test = OverrideTest()
for i in xrange(5):
    my_test.check()


if __name__ == '__main__':

    import os
    print '%s done!' % os.path.basename(__file__)
    pass
