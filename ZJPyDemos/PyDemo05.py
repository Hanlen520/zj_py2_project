# -*- coding: utf-8 -*-
'''
Created on 2017-2-6

@author: zhengjin
'''

# EXAMPLE 01, functional program
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


# EXAMPLE 05, insert sort
# def move_ele_into_sroted_list(test_list, ele_pos):
#     tmp_key = test_list[ele_pos]
#     sub_pos = ele_pos - 1
# 
#     if tmp_key >= test_list[sub_pos]:
#         return
#     while sub_pos >= 0 and test_list[sub_pos] > tmp_key:
#         test_list[sub_pos + 1] = test_list[sub_pos]
#         sub_pos -= 1
#     test_list[sub_pos + 1] = tmp_key
# 
# def insert_sort(test_list):
#     list_len = len(test_list)
#     for idx in xrange(1, list_len):
#         move_ele_into_sroted_list(test_list, idx)
#         print 'Sorting: ', test_list
#                  
#     return test_list
#   
# my_list = [13, 5, 43, 22, 11, 67, 43, 70, 39, 2]
# print 'Before sort:', my_list
# insert_sort(my_list)
# print 'After sort: ', my_list


# EXAMPLE 05, bubble sort
# def move_max_val_to_end_by_bubble_com(test_list, end_pos):
#     is_exchanged = False
#     for j in xrange(end_pos):
#         if test_list[j] > test_list[j+1]:
#             test_list[j], test_list[j+1] = test_list[j+1], test_list[j]
#             is_exchanged = True
# 
#     return is_exchanged
# 
# def bubble_sort(test_list):
#     list_len = len(test_list)
#     for i in xrange(list_len - 1):
#         is_exchanged = move_max_val_to_end_by_bubble_com(test_list, (list_len-1-i))
#         print 'Sorting: ', test_list
#         if not is_exchanged:
#             break
# 
#     return test_list
# 
# my_list = [13, 5, 22, 43, 11, 67, 43, 70, 2, 39]
# print 'Before sort:', my_list
# bubble_sort(my_list)
# print 'After sort: ', my_list


# EXAMPLE 06, quick sort
# def quick_sort(test_list, start_pos, end_pos):
#     if start_pos >= end_pos:
#         return test_list
#     
#     tmp_key = test_list[start_pos]
#     low = start_pos
#     high = end_pos
#     
#     while low < high:
#         while low < high and tmp_key <= test_list[high]:
#             high -= 1
#         test_list[low] = test_list[high]
#         while low < high and tmp_key >= test_list[low]:
#             low += 1
#         test_list[high] = test_list[low]
#     test_list[low] = tmp_key  # low == high
#     print 'Sorting: ', test_list
#     
#     quick_sort(test_list, start_pos, (low - 1))
#     quick_sort(test_list, (low + 1), end_pos)
#     
#     return test_list
# 
# my_list = [13, 5, 22, 43, 11, 67, 43, 70, 2, 39]
# print 'Before sort:', my_list
# quick_sort(my_list, 0, (len(my_list) - 1))
# print 'After sort: ', my_list


# EXAMPLE 07, select sort
# def select_sort_01(test_list):
#     # get min value in start by select
#     list_len = len(test_list)
#     for i in xrange(list_len-1):
#         for j in xrange((i+1), list_len):
#             if test_list[i] > test_list[j]:
#                 test_list[i], test_list[j] = test_list[j], test_list[i]
#         print 'Sorting: ', test_list
#      
#     return test_list

# def select_sort_02(test_list):
#     list_len = len(test_list)
#     for i in xrange(list_len-1):
#         min_idx = i
#         for j in xrange((i+1), list_len):
#             if test_list[min_idx] > test_list[j]:
#                 min_idx = j
#         test_list[i], test_list[min_idx] = test_list[min_idx], test_list[i]
#         print 'Sorting: ', test_list
#      
#     return test_list

# my_list = [13, 5, 22, 43, 11, 67, 43, 70, 2, 39]
# print 'Before sort:', my_list
# # select_sort_01(my_list)
# select_sort_02(my_list)
# print 'After sort: ', my_list


# EXAMPLE 08, shell sort
# def shell_sort(test_list):
#     list_len = len(test_list)
#     group = list_len / 2
#  
#     while group > 0:
#         i = 0
#         while i < group:  # iterator for each grouped list
#             j = i + group
#             while j < list_len:  # iterator for each element in grouped list
#                 k = j - group
#                 while k >= 0:  # iterator for each element in sub grouped list
#                     if test_list[k + group] < test_list[k]:  # insert sort by exchange
#                         test_list[k + group], test_list[k] = test_list[k], test_list[k + group]
#                     k -= group
#                 # end while
#                 j += group
#             # end while
#             i += 1
#         # end while
#         print 'Sorting: ', test_list
#         group = group / 2
#     # end while
# 
#     return test_list
# 
# my_list = [13, 5, 22, 43, 11, 67, 43, 70, 2, 39]
# print 'Before sort:', my_list
# shell_sort(my_list)
# print 'After sort: ', my_list


# EXAMPLE 09, import and reload
# import PyDemo04
# PyDemo04.print_message()
# 
# reload(PyDemo04)
# PyDemo04.print_message()


# EXAMPLE 10, built-in functions
# import sys
# print 'Module search paths:', sys.path
# 
# print 'Defined fields and methods:', dir()
# 
# print 'Access global fields:', globals()
# print 'Access local fields:', locals()


# EXAMPLE 11, iteritems()
# mapping = {1:'one', 2:'two', 3:'three', 4:'four'}
# for key, val in mapping.iteritems():
#     print 'key:', key, 'value:', val


# EXAMPLE 12, method(*arg)
# def mul(x, y):
#     return x * y
# 
# tmp_lst = [2, 3]
# print mul(*tmp_lst)


# EXAMPLE 13, division
# a = 1
# print a / 2, a / float(2)

# from __future__ import division
# b = 1
# print b // 2, b / 2


# EXAMPLE 14, isinstance()
# tmp_str = 'test'
# if isinstance(tmp_str, basestring):
#     print 'Type is string.'
# 
# tmp_lst = [1, 2, 3]
# if isinstance(tmp_lst, (list, tuple)):
#     print 'Type is collection.'


# EXAMPLE 14, get char count in string
# tmp_str = 'abracadabra'
# freqs = {}
# for ch in tmp_str:
#     if ch in freqs:
#         freqs[ch] += 1
#     else:
#         freqs[ch] = 1
# 
# for key, val in freqs.iteritems():
#     print 'key: ', key, 'count: ', val


if __name__ == '__main__':

    import os
    print __name__
    print '%s done!' % os.path.basename(__file__)
    pass
