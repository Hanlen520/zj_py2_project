# -*- coding: utf-8 -*-
'''
Created on 2016-8-10

@author: zhengjin
'''
import os
import sys
import time
import logging

from ZJPyUtils import WinSysUtils, AdbUtils, LogUtils, FileUtils

# ----------------------------------------------------
# Global vars
# ----------------------------------------------------
g_device_ip = '172.17.5.95'

g_test_class = 'com.example.zhengjin.funsettingsuitest.testsuites.Launcher24x7TestsSuite'
g_component = 'com.example.zhengjin.funsettingsuitest.test'
g_test_runner = 'android.support.test.runner.AndroidJUnitRunner'

g_total_run_times = 0
g_total_failed = 0

g_remote_tmp_dir_path = '/data/local/tmp'
g_remote_tmp_captures_dir_name = 'AutoTestCaptures'
g_remote_tmp_captures_dir_path = '%s/%s' % (g_remote_tmp_dir_path, g_remote_tmp_captures_dir_name)

g_inst_runner_logcat_tag = 'TestRunner'


# ----------------------------------------------------
# Init local path
# ----------------------------------------------------
g_local_report_dir_path = ''
g_local_inst_run_log_file_path = ''
g_local_test_logging_file_path = ''
g_local_logcat_log_file_path = ''

def init_local_report_paths():
    report_dir_name = 'logs_%s' % WinSysUtils.get_current_date_and_time()
    report_dir_path = os.path.join(os.getcwd(), 'logs', report_dir_name)
    global g_local_report_dir_path
    g_local_report_dir_path = report_dir_path

    if not os.path.exists(report_dir_path):
        os.makedirs(report_dir_path)

    global g_local_inst_run_log_file_path
    inst_run_log_file_name = 'InstrutmentRunLog.log'
    g_local_inst_run_log_file_path = os.path.join(report_dir_path, inst_run_log_file_name)
    
    global g_local_test_logging_file_path
    logging_name = 'TestLoggingReport.log'
    g_local_test_logging_file_path = os.path.join(report_dir_path, logging_name)
    
    global g_local_logcat_log_file_path
    logcat_log_file_name = 'LogcatLogByTag.log'
    g_local_logcat_log_file_path = os.path.join(report_dir_path, logcat_log_file_name)


# ----------------------------------------------------
# Helper functions
# ----------------------------------------------------
def rm_old_captures_on_remote():
    cmd = 'adb shell ls %s' % g_remote_tmp_dir_path
    lines_files = WinSysUtils.run_sys_cmd_and_ret_lines(cmd)
    flag_found = False
    for line in lines_files:
        if g_remote_tmp_captures_dir_name in line:
            flag_found = True
            break
    
    if flag_found:
        cmd = 'adb shell ls %s' % g_remote_tmp_captures_dir_path
        lines_capture = WinSysUtils.run_sys_cmd_and_ret_lines(cmd)
        if len(lines_capture) > 0:
            cmd = 'adb shell rm %s/*.png' % g_remote_tmp_captures_dir_path
            WinSysUtils.run_sys_cmd(cmd)
    else:
        cmd = 'adb shell mkdir -p %s' % g_remote_tmp_captures_dir_path
        WinSysUtils.run_sys_cmd(cmd)

def pull_remote_captures_to_local():
    # pull both dir and files in the dir from remote
    cmd = 'adb pull %s %s' % (g_remote_tmp_captures_dir_path, g_local_report_dir_path)
    WinSysUtils.run_sys_cmd(cmd)

def build_instrument_cmd_v1():
    return 'adb shell am instrument -w -r -e debug false -e class %s %s/%s >> %s' \
        % (g_test_class, g_component, g_test_runner, g_local_inst_run_log_file_path)

def build_instrument_cmd_v2():
    return 'adb shell am instrument -w -r -e debug false -e class %s %s/%s' \
        % (g_test_class, g_component, g_test_runner)

def run_instrument_tests_v1(cmd):
    WinSysUtils.run_sys_cmd(cmd)

def run_instrument_tests_v2(cmd):
    input_lines = WinSysUtils.run_sys_cmd_and_ret_lines(cmd)
    if len(input_lines) == 0:
        return
    
    output_lines = []
    for line in input_lines:
        output_lines.append(line.rstrip('\r\n')  + '\n')
    FileUtils.append_lines_to_file(g_local_inst_run_log_file_path, (output_lines))
    
    check_test_case_force_closed(output_lines)
    check_test_case_failed(output_lines)
    
def check_test_case_failed(lines):
    global g_total_failed
    for line in lines:
        if 'AssertionFailedError' in line:
            g_total_failed += 1
            return

def check_test_case_force_closed(lines):
    '''
    force close the testing process by Java code System.exit(1), 
    then check the keyword "Process crashed" in the testing runner, 
    if yes, stop the testing runner at once.
    '''
    for line in lines:
        if 'Process crashed' in line:
            logging.error('Found issue(Buffer Refresh Failed), and testing runner process is force closed.')
            sys.exit(1)

def create_report_summary():
    logging.info('----- Testing report summary: ')
    logging.info('Total run times: %d' % g_total_run_times)
    logging.info('Total passed: %d' % (g_total_run_times - g_total_failed))
    logging.info('Total failed: %d' % g_total_failed)


# ----------------------------------------------------
# Main
# ----------------------------------------------------
def loop_run_test(during):
    i = 0
    cmd = build_instrument_cmd_v2()
    
    start_time = int(time.clock())
    p = AdbUtils.adb_logcat_by_tag_and_ret_process(g_inst_runner_logcat_tag, g_local_logcat_log_file_path)
    while 1:
        if not AdbUtils.verify_adb_devices_serialno():
            if not AdbUtils.adb_connect_to_device(g_device_ip):
                logging.error('device is disconnect!')
                exit(1)
        
        run_instrument_tests_v2(cmd)
        time.sleep(3)
        
        i += 1
        logging.info('run ui test %d times.' % i)
        cur_run_time = int(time.clock()) - start_time
        logging.info('current run time: %d minutes %d seconds' % (cur_run_time / 60, cur_run_time % 60))
        
        if ((cur_run_time - start_time) > during):
            break
    # END LOOP
    
    # stop logcat
    AdbUtils.adb_stop()
    if p is not None:
        p.kill()

    global g_total_run_times
    g_total_run_times = i

def run_test_setup(during):
    init_local_report_paths()
    LogUtils.init_log_config(logging.DEBUG, logging.INFO, g_local_test_logging_file_path)

    if not AdbUtils.adb_connect_with_root(g_device_ip):
        logging.error('adb is NOT run with root!')
        exit(1)
    rm_old_captures_on_remote()

    test_case = g_test_class[(g_test_class.rindex('.') + 1) : ]
    logging.info('----- START run test %s for %s minutes' % (test_case, during / 60))

def run_test_clearup():
    create_report_summary()
    logging.info('----- END run test')
    pull_remote_captures_to_local()

def main(during):
    run_test_setup(during)
    loop_run_test(during)
    run_test_clearup()


if __name__ == '__main__':

    run_time = 5 * 60  # seconds
    main(run_time)

    print '%s done!' % (os.path.basename(__file__))
    pass
