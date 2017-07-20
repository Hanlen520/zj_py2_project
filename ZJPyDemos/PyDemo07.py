# -*- coding: utf-8 -*-
'''
Created on 2017-5-27

@author: zhengjin
'''
import os

from PyDemo01 import run_ex_by_flag

# collections
# EXAMPLE 01, defaultdict
def ex01_01():
    from collections import defaultdict
    
    tmp_lst = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
    d_dict = defaultdict(list)  # set default value to []
    for k, v in tmp_lst:
        d_dict[k].append(v)

    print sorted(d_dict.iteritems())
run_ex_by_flag(ex01_01)

def ex01_02():
    tmp_lst = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
    d_dict = {}
    for k, v in tmp_lst:
        d_dict.setdefault(k, []).append(v)  # set default value to []

    print sorted(d_dict.items())
run_ex_by_flag(ex01_02)

def ex01_03():
    from collections import defaultdict
    
    tmp_lst = [('red', 1), ('blue', 2), ('red', 3), ('blue', 4), ('red', 1), ('blue', 4)]
    d_dict = defaultdict(set)  # set default value to set (include distinct value)
    for k, v in tmp_lst:
        d_dict[k].add(v)

    print sorted(d_dict.items())
run_ex_by_flag(ex01_03)


# EXAMPLE 02, OrderedDict
def ex02():
    from collections import OrderedDict
    
    tmp_dict = {'banana': 3, 'apple': 4, 'pear': 1, 'orange': 2}
    print OrderedDict(sorted(tmp_dict.items(), key=lambda t:t[0]))
    print OrderedDict(sorted(tmp_dict.iteritems(), key=lambda t:len(t[0])))

    tmp_or_dict = OrderedDict.fromkeys('abcde', 'null')
    print tmp_or_dict

run_ex_by_flag(ex02)


# EXAMPLE 03, deque
def ex03():
    from collections import deque
    
    tmp_deque = deque(range(10), maxlen=10)
    print tmp_deque

    tmp_deque.appendleft(-1)
    print tmp_deque

    tmp_deque.extendleft([10, 20, 30])
    print tmp_deque
    
run_ex_by_flag(ex03)


# EXAMPLE 04, Counter
def ex04():
    from collections import Counter

    tmp_ct = Counter('abracadabra')
    print tmp_ct
    
    tmp_ct = Counter({'a': 5, 'r': 2, 'b': 2, 'd': 1, 'c': 1})
    tmp_ct.update('aaaaazzz')
    print tmp_ct
    print tmp_ct.most_common(2)
    print tmp_ct.elements()
    print ''.join(tmp_ct.elements())

run_ex_by_flag(ex04)


# EXAMPLE 05, namedtuple
def ex05():
    from collections import namedtuple
    
    City = namedtuple('City', 'name country population coordinates')
    tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
    
    print City._fields
    print tokyo
    print tokyo.population
    print tokyo.coordinates
    print tokyo[1]

run_ex_by_flag(ex05)


# tools
# EXAMPLE 06, functools
def ex06_01():
    from functools import partial

    print int('10010', base=2)
    base_2 = partial(int, base=2)
    print base_2('10010')
run_ex_by_flag(ex06_01)


def ex06_02():
    def my_decorator(f):
        from functools import wraps
        @wraps(f)
        def wrapper():
            """wrapper_doc"""
            print 'Calling decorated function'
            return f()
        return wrapper

    @my_decorator
    def example():
        """example_doc"""
        print 'Called example function'

    example()
    print example.__name__
    print example.__doc__
run_ex_by_flag(ex06_02)


def clock(func):
    import functools
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        import time
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        
        arg_lst = []
        if args:
            arg_lst.append(', '.join((repr(arg) for arg in args)))
        if kwargs:
            pairs = ('%s=%s' % (k, w) for k, w in kwargs)
            arg_lst.append(', '.join(pairs))
        arg_str = ', '.join(arg_lst)
        print '[%0.8fs] %s(%s) -> %r ' % (elapsed, name, arg_str, result)
        return result
    return clocked

def ex06_03():
    @clock
    def fibonacci(n):
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    print fibonacci(6)
run_ex_by_flag(ex06_03)


# EXAMPLE 07, itertools
# repeat
def ex07_01():
    from itertools import count, repeat
    for i, s in zip(count(1), repeat('over-and-over', 5)):
        print i, s
run_ex_by_flag(ex07_01)

# islice
def ex07_02():
    from itertools import islice
    for i in islice(range(60), 0, 100, 10):
        print i
run_ex_by_flag(ex07_02)

# starmap
def ex07_03():
    from itertools import starmap
    my_iter = starmap(os.path.join,
                      [('/bin', 'python'), ('/usr', 'bin', 'java'),
                       ('/usr', 'bin', 'perl'), ('/usr', 'bin', 'ruby')])
    print list(my_iter)
run_ex_by_flag(ex07_03)


# EXAMPLE 08, operator
class Student(object):
    def __init__(self, name, grade, age):
        self.name = name
        self.grade = grade
        self.age = age

    def __repr__(self):
        return repr((self.name, self.grade, self.age))

    def student_print(self, text):
        return '%s, %s, your grade: %s' % (text, self.name, self.grade)

def ex08_01():
    # attrgetter
    student_objects = [Student('john', 'A', 15), Student('jane', 'B', 12), Student('dave', 'B', 10), ]
    
    print sorted(student_objects, key=lambda student: student.age)
    from operator import attrgetter
    print sorted(student_objects, key=attrgetter('age'))
    print sorted(student_objects, key=attrgetter('grade', 'age'))

    f1 = attrgetter('name', 'age')
    s1 = Student('john', 'A', 15)
    print f1(s1)
    
    # itemgetter
    print '*' * 20
    student_tuples = [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10), ]
    print sorted(student_tuples, key=lambda student: student[2])
    from operator import itemgetter
    print sorted(student_tuples, key=itemgetter(2))
    print sorted(student_tuples, key=itemgetter(1, 2))
    
    f2 = itemgetter(0)
    s2 = ('john', 'A', 15)
    print f2(s2)

run_ex_by_flag(ex08_01)


def ex08_02():
    from operator import methodcaller
    f = methodcaller('student_print', 'hello')
    s = Student('john', 'A', 15)
    print f(s)

run_ex_by_flag(ex08_02)


# EXAMPLE 09, __get__
class RevealAccess(object):
    def __get__(self, obj, obj_type):
        print 'self in RevealAccess __get__: {}'.format(self)
        print 'self: {}\tobj: {}\tobjtype: {}'.format(self, obj, obj_type)

    def __set__(self, obj, value):
        print 'self in RevealAccess __set__: {}'.format(self)
        print 'self: {}\tobj: {}\tvalue: {}'.format(self, obj, value)

class MyClass(object):
    x = RevealAccess()
    def test(self):
        print 'self in MyClass: {}'.format(self)

def ex09():
    m = MyClass()
    m.test()

    print '*' * 20
    m.x  # __getattribute__() -> __get__(obj, type(obj))
    print '*' * 20
    m.x = 'test instance'

    print '*' * 20
    MyClass.x  # __getattribute__() -> __get__(None, self)
    print '*' * 20
    MyClass.x = 'test class'

run_ex_by_flag(ex09)


# EXAMPLE 10, property
class AccountTest1(object):
    def __init__(self):
        self._acct_num = None
    
    def get_acct_num(self):
        print 'AccountTest1, get account number.'
        return self._acct_num
    def set_acct_num(self, value):
        from decimal import Decimal
        print 'AccountTest1, set account number.'
        if isinstance(value, Decimal):
            self._acct_num = str(value)
        else:
            self._acct_num = value
    def del_acct_num(self):
        print 'AccountTest1, del account number.'
        del self._acct_num

    acct_num = property(get_acct_num, set_acct_num, del_acct_num, '_acct_num property')

def ex10():
    acct = AccountTest1()
    acct.acct_num = 100
    print acct.acct_num

run_ex_by_flag(ex10)


# EXAMPLE 11, property
class AccountTest2(object):
    def __init__(self):
        self._acct_num = None
        
    @property
    def acct_num(self):
        print 'AccountTest2, get account number.'
        return self._acct_num
    @acct_num.setter
    def acct_num(self, value):
        from decimal import Decimal
        print 'AccountTest2, set account number.'
        if isinstance(value, Decimal):
            self._acct_num = str(value)
        else:
            self._acct_num = value
    @acct_num.deleter
    def acct_num(self):
        print 'AccountTest2, del account number.'
        del self._acct_num

def ex11():
    acct = AccountTest2()
    acct.acct_num = 100
    print acct.acct_num

run_ex_by_flag(ex11)


# EXAMPLE 12, __getattr__
class MyDict(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)
    
    def __setattr__(self, key, value):
        self[key] = value
        
    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __repr__(self):
        return '<MyDict ' + dict.__repr__(self) + '>'

def ex12():
    d = MyDict(a=1)
    print d['a']
    
    d.a = 2
    print d.a

run_ex_by_flag(ex12)


# EXAMPLE 13, yield for concurrence
def ex13():
    from collections import deque
    
    def student(name, homeworks):
        for homework in homeworks.iteritems():
            yield(name, homework[0], homework[1])
            
    class Teacher(object):
        def __init__(self, students):
            self.students = deque(students)

        def handle(self):
            while len(self.students):
                student = self.students.pop()
                try:
                    homework = next(student)
                    print('handling', homework[0], homework[1], homework[2])
                except StopIteration:
                    print 'stop'
                    pass
                else:
                    self.students.appendleft(student)

    students = [
                student('Student1', {'math': '1+1=2', 'cs': 'operating system'}),
                student('Student2', {'math': '2+2=4', 'cs': 'computer graphics'}),
                student('Student3', {'math': '3+3=5', 'cs': 'compiler construction'})
                ]
    Teacher(students).handle()
    
run_ex_by_flag(ex13)


# EXAMPLE 14, empty function
def ex14():
    def empty_func():
        pass
    print empty_func()  # None
run_ex_by_flag(ex14)


g_test_var = 'init from beginning'

if __name__ == '__main__':

    g_test_var = 'init in main'
    print g_test_var

    print os.path.basename(__file__), 'DONE!'
