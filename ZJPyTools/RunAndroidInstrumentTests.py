# -*- coding: utf-8 -*-
'''
Created on 2016-8-10

@author: zhengjin
'''
import os
import time
import logging

from ZJPyUtils import WinSysUtils,AdbUtils,LogUtils


# ----------------------------------------------------
# Variables
# ----------------------------------------------------
g_device_ip = '172.17.5.106'

g_test_class = 'tv.fun.appsautotest.testCases.TestFunTvFilm#testPlayFilm'
g_pkg = 'tv.fun.appsautotest.test'
g_test_runner = 'android.support.test.runner.AndroidJUnitRunner'

g_report_dir_path = ''
g_report_file_path = ''
g_log_file_path = ''


# ----------------------------------------------------
# Helper functions
# ----------------------------------------------------
def init_report_paths():
    report_dir_name = 'logs_%s' %WinSysUtils.get_current_date_and_time()
    report_dir_path = os.path.join(os.getcwd(), 'logs', report_dir_name)
    if not os.path.exists(report_dir_path):
        os.makedirs(report_dir_path)
    global g_report_dir_path
    g_report_dir_path = report_dir_path
    
    report_name = 'InstrutmentTestReport.log'
    report_file_path = os.path.join(report_dir_path, report_name)
    global g_report_file_path
    g_report_file_path = report_file_path
    
    log_name = 'InstrumentRunnerLog.log'
    log_file_path = os.path.join(report_dir_path, log_name)
    global g_log_file_path
    g_log_file_path = log_file_path

def remove_old_captures():
    cmd = 'adb shell rm /data/local/tmp/captures/*.png'
    WinSysUtils.run_sys_cmd(cmd)

def move_and_pull_captures():
    shell_tmp_captures_dir_path = '/data/local/tmp/captures'
    shell_captures_dir_path = '/sdcard/auto_test_captures/captures_%s' %WinSysUtils.get_current_date_and_time()

    cmd = 'adb shell mkdir -p %s' %shell_captures_dir_path  # make dir for multiple levels
    WinSysUtils.run_sys_cmd(cmd)
    time.sleep(1)
    
    cmd = 'adb shell busybox cp %s/*.png %s' %(shell_tmp_captures_dir_path, shell_captures_dir_path)
    WinSysUtils.run_sys_cmd(cmd)
    time.sleep(1)

    win_captures_dir_path = '%s/captures' %g_report_dir_path
    if not os.path.exists(win_captures_dir_path):
        os.mkdir(win_captures_dir_path)
    cmd = 'adb pull %s %s' %(shell_captures_dir_path, win_captures_dir_path)
    WinSysUtils.run_sys_cmd(cmd)

def build_instrument_cmd():
    return 'adb shell am instrument -w -r -e debug false -e class %s %s/%s >> %s' \
        %(g_test_class,g_pkg,g_test_runner,g_report_file_path)

def run_instrument_tests(cmd):
    WinSysUtils.run_sys_cmd(cmd)

    
# ----------------------------------------------------
# Main
# ----------------------------------------------------
def run_test_for_during(during):
    cmd = build_instrument_cmd()

    start_time = int(time.clock())
    i = 1
    while (True):
        logging.info('run test %d times.' %i)
        if not AdbUtils.verify_adb_devices_serialno():
            if not AdbUtils.adb_connect_to_device(g_device_ip):
                logging.error('Error, adb devices disconnect.')
                exit(1)
        run_instrument_tests(cmd)
        i += 1
        time.sleep(3)
        
        cur_run_time = int(time.clock()) - start_time
        logging.info('current run time: %d minutes' %(cur_run_time/60))
        if (cur_run_time - start_time > during):
            break
    # END LOOP

def run_test_setup(during):
    init_report_paths()
    LogUtils.init_log_config(logging.DEBUG, logging.INFO, g_log_file_path)

    if not AdbUtils.adb_connect_with_root(g_device_ip):
        exit(1)
    remove_old_captures()

    test_case = g_test_class[(g_test_class.rindex('.') + 1) : ]
    logging.info('----- START run test %s for %s minutes' %(test_case, during/60))

def run_test_clearup():
    move_and_pull_captures()
    logging.info('----- END run test')

def main(during):
    run_test_setup(during)
    run_test_for_during(during)
    run_test_clearup()


if __name__ == '__main__':

    during = 30 * 60   # seconds
    main(during)

    logging.debug('%s done!' %(os.path.basename(__file__)))
    pass