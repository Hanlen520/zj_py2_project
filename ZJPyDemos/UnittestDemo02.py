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
class test_multiply_2(unittest.TestCase):

    def setUp(self):
        logging.debug('method setup.')
        
    def tearDown(self):
        logging.debug('method teardown.')
        
    @classmethod
    def setUpClass(cls):
        logging.debug('class setup.')
        logging.info('start to run test class: %s' % (os.path.basename(__file__)))

    @classmethod
    def tearDownClass(cls):
        logging.debug('class teardown.') 

    def test_0_x_1(self):
        logging.warn('Verify multiply 0 and 1.')
        self.assertEquals(PyDemo03.my_multiply(0, 1), 0)


# ------------------------------------------------
# Main
# ------------------------------------------------
if __name__ == '__main__':

    unittest.main(verbosity=1)
    print 'unit test DONE.'
