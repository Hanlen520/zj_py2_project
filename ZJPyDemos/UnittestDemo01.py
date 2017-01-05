# -*- coding: utf-8 -*-

'''
Created on 2016-7-12

@author: zhengjin
'''

import os
import unittest
import logging

from ZJPyDemos import PyDemo03

# ------------------------------------------------
# Test cases
# ------------------------------------------------
class test_multiply(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        logging.debug('method setup.')
        
    def tearDown(self):
        logging.debug('method teardown.')
        unittest.TestCase.tearDown(self)
        
    @classmethod
    def setUpClass(cls):
        super(test_multiply, cls).setUpClass()
        logging.debug('class setup.')
        logging.info('start to run test class: %s' %(os.path.basename(__file__)))

    @classmethod
    def tearDownClass(cls):
        logging.debug('class teardown.') 
        super(test_multiply, cls).tearDownClass()

    def test_3_x_4(self):
        logging.info('Verify multiply 3 and 4.')
        self.assertEquals(PyDemo03.my_multiply(3,4), 12)

    def test_a_x_3(self):
        logging.info('Verify multiply 3 and a.')
        logging.warn('This test will be failed(失败).')
        self.assertEquals(PyDemo03.my_multiply(3,'a'), 'aa')


# ------------------------------------------------
# Main
# ------------------------------------------------
if __name__ == '__main__':

    unittest.main(verbosity=1)

    pass