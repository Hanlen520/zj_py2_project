# -*- coding: utf-8 -*-
'''
Created on 2017-2-6

@author: zhengjin
'''

# EXAMPLE 01, functional gromgram
# cats = {'Mojo':84, 'Mao-Mao':34, 'Waffles':4, 'Pickles':6}
# for k in cats:
#     print k
# 
# kittens = []
# #1.1
# # for k,v in cats.items():
# #     if v < 7:
# #         kittens.append(k)
# #1.2
# # for k,v in cats.iteritems():
# #     if v < 7:
# #         kittens.append(k)
# 
# #2
# # kittens = [k for k, v in cats.items() if v < 7]
# #3
# kittens = map(lambda (k, v): k, filter(lambda (k, v):v < 7, cats.items()))
# print kittens


# EXAMPLE 02, file read
# import os
#  
# tmp_file_path = os.path.join(os.getcwd(), 'zjunittest.log')
# with open(tmp_file_path, 'r') as f:
# #     #1
# #     for line in f.readlines():
# #         print line.strip()
#     #2
#     print type(f)
#     print dir(f)
#     for line in f:
#         print line.strip()


# EXAMPLE 03, multiple lines
# print 'this is first line.\n' \
#        'this is 2nd line.\n'
# 
# print ('this is first line.\n'
#        'this is 2nd line.\n')


# EXAMPLE 04, zip, enumerate
# li1 = ['k1', 'k2', 'k3']
# li2 = ['a', 'b', 'c']
# tmp_d = dict(zip(li1, li2))
# print tmp_d
# 
# for idx, val in enumerate(li1):
#     print 'position: %d value: %s' %(idx, val)


if __name__ == '__main__':

    import os
    print '%s done!' % os.path.basename(__file__)
    pass
