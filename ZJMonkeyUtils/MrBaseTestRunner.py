# -*- coding: utf-8 -*-
'''
@author: zhengjin
'''
import os
import time

# ----------------------------------------------------
# build tests
# ----------------------------------------------------
def get_specified_test(dir_path, script_name):
    return os.path.join(dir_path, script_name)

def get_all_tests_from_dir(dir_path):
    tests = []
    test_prefix = 'MrTest'
    
    f_names = os.listdir(dir_path)
    for f_name in f_names:
        if f_name.startswith(test_prefix):
            tests.append(os.path.join(dir_path, f_name))

    if len(tests) != 0:
        return tests
    else:
        print 'No test case found!'
        exit()

# ----------------------------------------------------
# monkey_test_main
# ----------------------------------------------------
def run_mr_command(bat_path, script_path):
    cmd = '{0} {1}'.format(bat_path, script_path)
    print cmd
    os.system(cmd)

def set_env_var():
    os.environ['MR_PROJECT_PATH'] = r'E:\Eclipse_Workspace\ZJPyProject\ZJMonkeyUtils'

def monkey_test_main():
    test_scripts = []
    mr_bat_path = os.path.join(os.environ['ANDROID_SDK_HOME'], 'tools\monkeyrunner.bat');
    
    # build test cases
#     test_scripts.append(get_specified_test(os.getcwd(), 'MrDemo02.py'))
    test_scripts.append(get_specified_test(os.getcwd(), 'MrTestTVPlayer.py'))

#     test_scripts = get_all_tests_from_dir(os.getcwd())
    # build test cases, end
    
    if len(test_scripts) == 0:
        print 'No test case added!'
        exit()
    
    for test_script in test_scripts:
        print '-----> start run test script -> %s' %(test_script)
        run_mr_command(mr_bat_path, test_script);
        print '-----> end run test script -> %s' %(test_script)

def exec_time_main(fn):
    set_env_var()
    
    start = int(time.clock())
    fn()
    end = int(time.clock())
    print "MonkeyRunner finished and cost %d seconds" %((end - start))


# ----------------------------------------------------
# Runner
# ----------------------------------------------------
if __name__ == '__main__':

    exec_time_main(monkey_test_main)
    
    pass
