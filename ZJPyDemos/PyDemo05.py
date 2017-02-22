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
# def insert_sort(test_list):
#     list_len = len(test_list)
#      
#     for i in xrange(1, list_len):
#         tmp_key = test_list[i];
#         j = i - 1;
#          
#         if tmp_key >= test_list[j]:
#             continue
#         while j >= 0 and test_list[j] > tmp_key:
#             test_list[j + 1] = test_list[j]
#             j -= 1
#    
#         test_list[j + 1] = tmp_key
#         print 'Sorting: ', test_list
#     # end for
#                 
#     return test_list
#  
# my_list = [13, 5, 43, 22, 11, 67, 43, 70, 39, 2]
# print 'Before sort:', my_list
# insert_sort(my_list)
# print 'After sort: ', my_list


# EXAMPLE 05, bubble sort
# def bubble_sort(test_list):
#     list_len = len(test_list)
#   
#     for i in xrange(list_len - 1):
#         exchange = False
#         for j in xrange(list_len - 1 - i):
#             if test_list[j] > test_list[j+1]:
#                 test_list[j], test_list[j+1] = test_list[j+1], test_list[j]
#                 exchange = True
#         if not exchange:
#             break
#         print 'Sorting: ', test_list
#     # end for
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
#     list_len = len(test_list)
#     for i in xrange(list_len-1):
#         for j in xrange((i+1), list_len):
#             if test_list[i] > test_list[j]:
#                 test_list[i], test_list[j] = test_list[j], test_list[i]
#     
#     return test_list
#     
# def select_sort_02(test_list):
#     list_len = len(test_list)
#     for i in xrange(list_len-1):
#         min_idx = i
#         for j in xrange((i+1), list_len):
#             if test_list[min_idx] > test_list[j]:
#                 min_idx = j
#         test_list[i], test_list[min_idx] = test_list[min_idx], test_list[i]
#     
#     return test_list
# 
# my_list = [13, 5, 22, 43, 11, 67, 43, 70, 2, 39]
# print 'Before sort:', my_list
# # select_sort_01(my_list)
# select_sort_02(my_list)
# print 'After sort: ', my_list


def shell_sort(test_list):
    # TODO:
    return test_list


if __name__ == '__main__':

    import os
    print '%s done!' % os.path.basename(__file__)
    pass
