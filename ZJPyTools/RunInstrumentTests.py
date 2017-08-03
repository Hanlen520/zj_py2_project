# -*- coding: utf-8 -*-
'''
Created on 2017-7-14

@author: zhengjin

Run Andorid instrument UI test cases.
1) Run test cases and dump execution logs.
2) Start and dump logcat log.
3) Pull run listener results files and snapshots.
4) Generate html testing report.
'''

import os
import time
import subprocess

from ZJPyUtils import AdbUtils, WinSysUtils

# ----------------------------------------------------
# Constants
# ----------------------------------------------------
CUR_DATE_TIME = WinSysUtils.get_current_date_and_time()
REPORT_DIR_NAME = 'logs_inst_test_%s' % CUR_DATE_TIME
REPORT_DIR_PATH = os.path.join(os.getcwd(), 'logs', REPORT_DIR_NAME)
LOGCAT_FILE_NAME = 'logcat_log.txt'
LOGCAT_FILE_PATH = os.path.join(REPORT_DIR_PATH, LOGCAT_FILE_NAME)
INST_TEST_LOG_FILE_NAME = 'instrument_test_log.txt'
INST_TEST_LOG_FILE_PATH = os.path.join(REPORT_DIR_PATH, INST_TEST_LOG_FILE_NAME)

SHELL_TEST_LOG_DIR_PATH = '/sdcard/auto_test_logs/'
SHELL_SNAPSHOTS_DIR_PATH = SHELL_TEST_LOG_DIR_PATH + '.snapshots'
SHELL_SNAPSHOTS_DIR_NEW_PATH = SHELL_TEST_LOG_DIR_PATH + 'snapshots'

DATA_DIR_PATH = os.path.join(os.getcwd(), 'data')
JAR_FILE_PATH = os.path.join(DATA_DIR_PATH, 'XmlTransform.jar')
XSLT_FILE_PATH = os.path.join(DATA_DIR_PATH, 'testsuites.xstl')

TEST_CLASS_PARENT = 'com.example.zhengjin.funsettingsuitest.testcases.'
TEST_SUITE_PARENT = 'com.example.zhengjin.funsettingsuitest.testsuites.'
ALL_TEST_CASES_SUITE = TEST_SUITE_PARENT + 'AllTestsSuite'


# ----------------------------------------------------
# Logs
# ----------------------------------------------------
def start_logcat_log():
    cmd = 'adb logcat -c && adb logcat -v time *:I > %s' % LOGCAT_FILE_PATH
    print cmd
    return subprocess.Popen(cmd, shell=True)

def stop_logcat_log(p):
    if p is not None:
        p.kill()
    AdbUtils.adb_stop()

def delete_old_instrument_run_listener_logs():
    cmd = 'adb shell rm -rf ' + SHELL_TEST_LOG_DIR_PATH
    print cmd
    WinSysUtils.run_sys_cmd(cmd)

def pull_results_file_and_create_report():
    for f_name in get_instrument_run_listener_results_files_name():
        pull_instrument_run_listener_results_file(f_name)
        time.sleep(1)
        create_html_report(os.path.join(REPORT_DIR_PATH, f_name))

def get_instrument_run_listener_results_files_name():
    cmd = 'adb shell ls %s' % SHELL_TEST_LOG_DIR_PATH
    print cmd
    ret_lines = WinSysUtils.run_sys_cmd_and_ret_lines(cmd)
    return [line.rstrip('\r\n') for line in ret_lines if line.rstrip('\r\n').endswith('.xml')]

def pull_instrument_run_listener_results_file(file_name):
    cmd = 'adb pull %s %s' % (SHELL_TEST_LOG_DIR_PATH + file_name, REPORT_DIR_PATH)
    print cmd
    WinSysUtils.run_sys_cmd(cmd)

def create_html_report(src_results):
    cmd = 'java -jar %s -f=%s -x=%s' % (JAR_FILE_PATH, src_results, XSLT_FILE_PATH)
    print cmd
    WinSysUtils.run_sys_cmd(cmd)

def pull_instrument_run_snapshorts():
    cmd = 'adb shell rename %s %s' % (SHELL_SNAPSHOTS_DIR_PATH, SHELL_SNAPSHOTS_DIR_NEW_PATH)
    print cmd
    if not WinSysUtils.run_sys_cmd(cmd):
        return

    time.sleep(1)
    cmd = 'adb pull %s %s' % (SHELL_SNAPSHOTS_DIR_NEW_PATH, REPORT_DIR_PATH)
    print cmd
    WinSysUtils.run_sys_cmd(cmd)


# ----------------------------------------------------
# Run instrument test
# ----------------------------------------------------
def run_instrument_tests(test_class):
    inst_test_cmd_lst = ['adb shell am instrument', '-w -r',
                         '-e debug false', '-e class ' + test_class,
                         '-e listener com.example.zhengjin.funsettingsuitest.testrunner.RunnerListenerFunSettings',
                         'com.example.zhengjin.funsettingsuitest.test/android.support.test.runner.AndroidJUnitRunner']
    cmd = ' '.join(inst_test_cmd_lst) + ' > ' + INST_TEST_LOG_FILE_PATH
    print cmd
    p = subprocess.Popen(cmd, shell=True)
    time.sleep(1)  # wait for process start
    return p
    
def is_instrument_test_process_alive():
    cmd = 'adb shell ps | findstr funsettingsuitest'
    ret_lines = os.popen(cmd).readlines()

    if len(ret_lines) == 1:
        return True
    elif len(ret_lines) == 0:
        print 'Instrument test process exit.'
        return False
    else:
        print 'Error, more than one instrument test process running!'
        exit(1)


# ----------------------------------------------------
# Main
# ----------------------------------------------------
def main_instument_setup():
    if not AdbUtils.verify_adb_devices_serialno():
        print 'Error, No adb devices connected, and exit!'
        exit(1)

    if not os.path.exists(REPORT_DIR_PATH):
        os.makedirs(REPORT_DIR_PATH)
    delete_old_instrument_run_listener_logs()

def main_instument_clearup():
    pull_instrument_run_snapshorts()
    pull_results_file_and_create_report()

def main_loop(p):
    t_start = int(time.clock())
    t_interval = 60

    while is_instrument_test_process_alive():
        t_end = int(time.clock())
        t_during = t_end - t_start
        print 'Instrument test run time => %s minutes and %s seconds' % (t_during / 60, t_during % 60)
        time.sleep(t_interval)

    p.wait()
    print 'Instrument test finished!'

def main_instument_test():
    main_instument_setup()
    p_logcat = None 
    if is_logcat_log:
        p_logcat = start_logcat_log()
    
    p_test = run_instrument_tests(test_class)
    main_loop(p_test)
    
    main_instument_clearup()
    if is_logcat_log:
        stop_logcat_log(p_logcat)


if __name__ == '__main__':

    is_logcat_log = True

#     test_class = TEST_CLASS_PARENT + 'TestAboutInfoPage#test01_01AboutInfoPageTitle'
#     test_class = TEST_CLASS_PARENT + 'TestAboutInfoPage'
    test_class = ALL_TEST_CASES_SUITE

    main_instument_test()

    print os.path.basename(__file__), 'DONE!'
