# -*- coding: utf-8 -*-
'''
Created on 2016-8-10

@author: zhengjin
'''
import os
import sys
import time
import logging

from ZJPyUtils import WinSysUtils,AdbUtils,LogUtils,FileUtils

# ----------------------------------------------------
# Variables
# ----------------------------------------------------
g_device_ip = '172.17.5.106'

g_test_class = 'com.example.zhengjin.funsettingsuitest.testcases.TestPlayingFilm#testDemo'
g_component = 'com.example.zhengjin.funsettingsuitest.test'
g_test_runner = 'android.support.test.runner.AndroidJUnitRunner'

g_total_run_times = 0
g_total_failed = 0


g_report_dir_path = ''
g_report_file_path = ''
g_log_file_path = ''

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


# ----------------------------------------------------
# Helper functions
# ----------------------------------------------------
def remove_old_captures():
    cmd = 'adb shell rm /data/local/tmp/captures/*.png'
    WinSysUtils.run_sys_cmd(cmd)

def copy_and_pull_captures():
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

def build_instrument_cmd_v1():
    return 'adb shell am instrument -w -r -e debug false -e class %s %s/%s >> %s' \
        %(g_test_class,g_component,g_test_runner,g_report_file_path)

def build_instrument_cmd_v2():
    return 'adb shell am instrument -w -r -e debug false -e class %s %s/%s' \
        %(g_test_class,g_component,g_test_runner)

def run_instrument_tests_v1(cmd):
    WinSysUtils.run_sys_cmd(cmd)

def run_instrument_tests_v2(cmd):
    output_content = WinSysUtils.run_sys_cmd_and_ret_content(cmd)
    if output_content is None:
        return
    FileUtils.append_content_to_file(g_report_file_path, output_content)
    
    if not check_test_case_failed(output_content):
        check_test_case_force_closed(output_content)

def check_test_case_failed(content):
    global g_total_failed
    
    if 'AssertionFailedError' in content:
        g_total_failed += 1
        return True
    return False

def check_test_case_force_closed(content):
    '''
    force close the testing process by Java code System.exit(0), 
    then check the keyword "Process crashed" in the testing runner, 
    if yes, stop the testing runner at once.
    '''
    if 'Process crashed' in content:
        logging.error('Found issue(Buffer Refresh Failed), and testing runner process is force closed.')
        sys.exit(1)

def create_report_summary():
    logging.info('----- Testing report summary: ')
    logging.info('Total run times: %d' %g_total_run_times)
    logging.info('Total passed: %d' %(g_total_run_times - g_total_failed))
    logging.info('Total failed: %d' %g_total_failed)


# ----------------------------------------------------
# Main
# ----------------------------------------------------
def loop_run_test(during):
    global g_total_run_times

    i = 1
    cmd = build_instrument_cmd_v2()

    start_time = int(time.clock())
    while 1:
        logging.info('run test %d times.' %i)
        if not AdbUtils.verify_adb_devices_serialno():
            if not AdbUtils.adb_connect_to_device(g_device_ip):
                exit(1)
        
        run_instrument_tests_v2(cmd)
        i += 1
        time.sleep(3)
        
        cur_run_time = int(time.clock()) - start_time
        logging.info('current run time: %d minutes' %(cur_run_time/60))
        if ((cur_run_time - start_time) > during):
            break
    # END LOOP
    g_total_run_times = i

def run_test_setup(during):
    init_report_paths()
    LogUtils.init_log_config(logging.DEBUG, logging.INFO, g_log_file_path)

    if not AdbUtils.adb_connect_with_root(g_device_ip):
        exit(1)
    remove_old_captures()

    test_case = g_test_class[(g_test_class.rindex('.') + 1) : ]
    logging.info('----- START run test %s for %s minutes' %(test_case, during/60))

def run_test_clearup():
    copy_and_pull_captures()
    create_report_summary()
    logging.info('----- END run test')

def main(during):
    run_test_setup(during)
    loop_run_test(during)
    run_test_clearup()


if __name__ == '__main__':

    run_during = 12 * 60 * 60   # seconds
    main(run_during)

    
    print '%s done!' %(os.path.basename(__file__))
    pass