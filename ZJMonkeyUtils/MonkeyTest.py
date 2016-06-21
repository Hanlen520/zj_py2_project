# -*- coding: utf-8 -*-
'''
Created on 2016-3-15

@author: zhengjin

Run monkey test by time, and generate monkey reports and system profile reports at the same time.

'''

import subprocess
import os
import time
import re
import cmd
import threading
from ZJPyAndroidMonitorUtils import MonitorRunner
from ZJPyAndroidMonitorUtils import MonitorUtils

# --------------------------------------------------------------
# Env vars
# --------------------------------------------------------------
g_target_ip = ''
g_package_name = ''
g_report_parse_keyword = 'tv.fun'

# default monkey parms
g_monkey_run_times = '1000000'  # default 1000000
g_flag_monkey_crash_ignore = True  # ignore crash or error for monkey
g_flag_monkey_for_package = True  # false for use whitelist.xml instead

g_max_run_time = 3600 * 4  # seconds, max execution time is 4 hours
g_loop_wait_time = 60  # seconds, wait time in loop

g_flag_capture = False
g_flag_profile_monitor = False
g_flag_print_log = False

g_cur_date = time.strftime('%Y%m%d')
g_run_num = '01'

# default monkey execution time
g_run_hours = 0
g_run_mins = 60
g_run_secs = 0

# default logcat level
g_log_level = 'I'


# --------------------------------------------------------------
# Path vars
# --------------------------------------------------------------
# log directory path
log_root_path = os.path.join(os.getcwd(), 'MonkeyReprots')
log_dir_for_win = r'%s\%s_%s' %(log_root_path, g_cur_date, g_run_num)
log_dir_for_shell = '/sdcard/testlogs'

# screen captures path
captures_dir_for_win = r'%s\captures' %(log_dir_for_win)
captures_dir_for_shell = '%s/captures' %(log_dir_for_shell)
capture_path_for_shell = '%s/capture_%s' %(captures_dir_for_shell, g_cur_date)

# logs of logcat path
logcat_log_for_win = r'%s\logcat_log_%s_%s.log' %(log_dir_for_win, g_cur_date, g_run_num)
logcat_log_for_shell = '%s/logcat_log_%s_%s.log' %(log_dir_for_shell, g_cur_date, g_run_num)

# log path for monkey, local
monkey_log = r'%s\monkey_log_%s_%s.log' %(log_dir_for_win, g_cur_date, g_run_num)

# rom props path, local
path_rom_props = r'%s\rom_props_%s_%s.log' %(log_dir_for_win, g_cur_date, g_run_num)

# parsed log path, local
logcat_parse_log_for_win = r'%s\logcat_parse_log_%s_%s.log' %(log_dir_for_win, g_cur_date, g_run_num)

# white list path
whitelist_file_for_win = os.path.join(os.getcwd(), 'whitelist.txt')
whitelist_file_for_shell = '%s/whitelist.txt' %(log_dir_for_shell)

# log levels
verbose = 0
debug = 1
info = 2
warn = 3
error = 4
fatal = 5


# --------------------------------------------------------------
# Build shell commands
# --------------------------------------------------------------
def build_command_monkey_for_whitelist():
    monkey_cmd_for_list = r'adb shell monkey --throttle 500 --pkg-whitelist-file %s ' %(whitelist_file_for_shell)
    monkey_launch_parm = '-c android.intent.category.MONKEY -c android.intent.category.LAUNCHER -c android.intent.category.DEFAULT ' + \
        '--monitor-native-crashes --kill-process-after-error '
    monkey_ignore = '--ignore-crashes --ignore-timeouts --ignore-security-exceptions --ignore-native-crashes '
    monkey_pct = '--pct-touch 0 --pct-motion 0 --pct-trackball 0 --pct-nav 50 ' + \
        '--pct-majornav 30 --pct-syskeys 15 --pct-appswitch 5 --pct-flip 0 --pct-anyevent 0 '
    monkey_format = '-v -v -v %s > %s' %(g_monkey_run_times, monkey_log)

    if g_flag_monkey_crash_ignore:
        cmd = monkey_cmd_for_list + monkey_launch_parm + monkey_ignore + monkey_pct + monkey_format
    else:
        cmd = monkey_cmd_for_list + monkey_launch_parm + monkey_pct + monkey_format

    return cmd
    
def build_command_monkey_for_package():
    monkey_cmd_for_package = 'adb shell monkey --throttle 500 -p %s ' %(g_package_name)
    monkey_launch_parm = '-c android.intent.category.MONKEY -c android.intent.category.LAUNCHER -c android.intent.category.DEFAULT ' + \
        '--monitor-native-crashes --kill-process-after-error '
    monkey_ignore = '--ignore-crashes --ignore-timeouts --ignore-security-exceptions --ignore-native-crashes '
    monkey_pct = '--pct-touch 0 --pct-motion 0 --pct-trackball 0 --pct-nav 60 ' + \
        '--pct-majornav 30 --pct-syskeys 10 --pct-appswitch 0 --pct-flip 0 --pct-anyevent 0 '
    monkey_format = '-v -v -v %s > %s' %(g_monkey_run_times, monkey_log)

    if g_flag_monkey_crash_ignore:
        cmd = monkey_cmd_for_package + monkey_launch_parm + monkey_ignore + monkey_pct + monkey_format
    else:
        cmd = monkey_cmd_for_package + monkey_launch_parm + monkey_pct + monkey_format

    return cmd

def build_command_logcat():
    logcat_cmd = 'adb logcat -c && adb logcat -f %s -v threadtime *:%s' %(logcat_log_for_shell, g_log_level)
    return logcat_cmd

def build_command_pull_anr_file():
    anr_files_path = '/data/anr'
    cmd = 'adb pull %s %s' %(anr_files_path, log_dir_for_win)
    return cmd

def build_command_pull_tombstone_file():
    tombstone_files_path = '/data/tombstones'
    cmd = 'adb pull %s %s' %(tombstone_files_path, log_dir_for_win)
    return cmd

def build_command_rm_anr_files():
    rm_anr_files_cmd = '/data/anr/*'
    cmd = 'adb shell rm %s' %(rm_anr_files_cmd)
    return cmd

def build_command_rm_tombstone_files():
    rm_tombstone_files_cmd = '/data/tombstones/*'
    cmd = 'adb shell rm {0}'.format(rm_tombstone_files_cmd)
    return cmd


# --------------------------------------------------------------
# Run shell commands
# --------------------------------------------------------------
def get_rom_properties_and_write_file():
    cmd = 'adb shell getprop'
    if g_flag_print_log:
        print cmd
    output = os.popen(cmd)
    
    f = open(path_rom_props, 'w')
    try:
        f.write(output.read())
    finally:
        f.close()

def remove_log_dir_for_shell():
    cmd = 'adb shell rm -rf %s' %(log_dir_for_shell)
    if g_flag_print_log:
        print cmd
    os.system(cmd)

def run_cmd_screen_capture():
    capture_file_path = '%s_%s.%s' %(capture_path_for_shell, time.strftime('%H%M%S'), 'png')
    cmd = 'adb shell screencap -p %s' %(capture_file_path)
    if g_flag_print_log:
        print cmd
    os.system(cmd)

def run_cmd_adb_root():
    # return True if adb root success
    cmd = 'adb root'
    if g_flag_print_log:
        print cmd
    p = subprocess.Popen('adb root',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()

    lines_error = p.stderr.readlines()
    if len(lines_error) > 0:
        print 'Error, adb root failed.'
        return False

    for line in p.stdout.readlines():
        if 'already' in line:
            print 'adbd is already running as root.'
            return True
        elif 'adbd as root' in line:
            print 'adb root success.'
            return True
        else:
            print 'Error, adb root failed.'
            return False

def run_cmd_adb_connect():
    cmd = 'adb connect %s' %(g_target_ip)
    if g_flag_print_log:
        print cmd
    os.system(cmd)


# --------------------------------------------------------------
# Adb shell utils
# --------------------------------------------------------------
def try_to_build_adb_connect():
    try_adb_connect_times = 3
    wait_time = 3
    for i in range(0,try_adb_connect_times):
        run_cmd_adb_connect()
        print 'try to connect to adb device, %d times.' %(i + 1)
        if verify_adb_devices_serialno():  # verify connect success
            return True

        time.sleep(wait_time)
    
    return False

def adb_connect_with_root():
    if not try_to_build_adb_connect():  # adb connect
        print 'Error, when adb connect to the device!'
        exit(1)
        
    if not run_cmd_adb_root():
        print 'Error, when connect to the device with root!'
        exit(1)

    if not try_to_build_adb_connect():   # adb connect as root
        print 'Error, when adb connect to the device!'
        exit(1)

def verify_adb_devices():
    cmd = 'adb devices'
    if g_flag_print_log:
        print cmd
    output = os.popen(cmd)

    port_num = ':5555'
    if port_num in output.read():
        return True
    else:
        return False

def verify_adb_devices_serialno():
    cmd = 'adb get-serialno'
    if g_flag_print_log:
        print cmd
    output = os.popen(cmd)

    if 'unknown' in output.read():
        return False
    else:
        return True

def adb_disconnect_device():
    cmd = 'adb disconnect'
    if g_flag_print_log:
        print cmd
    os.system(cmd)

def get_monkey_process_id():
    monkey_process_name = 'monkey'
    process_id = ''

    cmd = 'adb shell ps | findstr %s' %(monkey_process_name)
    if g_flag_print_log:
        print cmd
    lines = os.popen(cmd).readlines()
    for line in lines:
        if monkey_process_name in line:
            process_id = line[10:].split(' ')[0]
            print 'Monkey process id %s' %(process_id)
            return process_id
    
    print 'Error, the monkey process id is NONE!'
    exit(1)

def kill_monkey_process(process_id):
    cmd = 'adb shell kill %s' %(process_id)
    if g_flag_print_log:
        print cmd
    os.system(cmd)


# --------------------------------------------------------------
# IO, and report files
# --------------------------------------------------------------
def create_log_dir_for_win(path):
    if os.path.exists(path):
        return
    else:
        os.makedirs(path)
        time.sleep(1)

def create_log_dir_for_shell():
    cmd = 'adb shell mkdir %s' %(log_dir_for_shell)
    if g_flag_print_log:
        print cmd
    os.system(cmd)
    time.sleep(1)

def create_captures_dir_for_shell():
    cmd = 'adb shell mkdir %s' %(captures_dir_for_shell)
    if g_flag_print_log:
        print cmd
    os.system(cmd)
    time.sleep(1)

def upload_white_list():
    # upload whitelist to shell env
    cmd = 'adb push %s %s' %(whitelist_file_for_win, log_dir_for_shell)
    if g_flag_print_log:
        print cmd
    os.system(cmd)

def pull_all_testing_logs():
    cmd_pull_log_files = 'adb pull %s %s' %(log_dir_for_shell, log_dir_for_win)
    cmd_pull_anr_files = build_command_pull_anr_file()
    cmd_pull_tombstone_file = build_command_pull_tombstone_file()
    
    if g_flag_print_log:
        print cmd_pull_log_files
        print cmd_pull_anr_files
        print cmd_pull_tombstone_file
    
    # the adb connection maybe disconnect when running the monkey
    if verify_adb_devices():
        os.system(cmd_pull_log_files)
        os.system(cmd_pull_anr_files)
        os.system(cmd_pull_tombstone_file)
    else:
        print 'Error, no devices connected, NO files pulled!'

def pull_captures():
    if verify_adb_devices():
        cmd = 'adb pull %s %s' %(captures_dir_for_shell, captures_dir_for_win)
        if g_flag_print_log:
            print cmd
        os.system(cmd)
    else:
        print 'Error, no devices connected, NO captures pulled!'


# --------------------------------------------------------------
# Sub process
# --------------------------------------------------------------
# Kill monkey after specific time from subprocess
def thread_monkey_monitor_at_specific_time():
    spec_running_time = (g_run_hours * 3600) + (g_run_mins * 60) + g_run_secs
    if spec_running_time >= g_max_run_time:
        print 'Warn, spec_time must be less than max_time (4 hours)!'
        exit(1)

    wait_time_for_monkey_launch = 5
    time.sleep(wait_time_for_monkey_launch)  # wait for monkey process start
    monkey_process_id = get_monkey_process_id()
    
    # LOOP
    start = int(time.clock())
    while True:
        get_monkey_process_id()  # verify monkey is running currently
        if g_flag_capture:
            run_cmd_screen_capture()
        
        current_time = int(time.clock()) - start
        print 'LOOP, execution time: %d minutes and %d seconds' %((current_time / 60), (current_time % 60))
        if current_time >= spec_running_time or current_time >= g_max_run_time:
            kill_monkey_process(monkey_process_id)
            break

        time.sleep(g_loop_wait_time)
    # LOOP end

def build_thread_for_monkey_monitor():
    t = threading.Thread(target = thread_monkey_monitor_at_specific_time)
    return t

def build_thread_for_system_profile_monitor():
    MonitorRunner.g_pkg_name_all = g_package_name
    MonitorRunner.g_run_num_all = g_run_num
    MonitorRunner.g_run_time_all = g_run_mins * MonitorUtils.g_min
    MonitorRunner.g_suffix_all = '%s_%s' %(g_cur_date, g_run_num)
    
    t = threading.Thread(target=MonitorRunner.monitor_runner_main)
    return t

def start_all_threads(threads):
    for t in threads:
        if t is not None:
            t.start()

def wait_all_threads_exit(threads):
    for t in threads:
        if t is not None:
            t.join()


# --------------------------------------------------------------
# Parse log
# --------------------------------------------------------------
def parse_logcat_log(log_level, keyword):
    parse_lines = []
    
    f_log = open(logcat_log_for_win, 'r')
    lines = f_log.readlines()
    if len(lines) == 0:
        print 'Warn, there is no record in log file!'
        return
    
    try:
        for line in lines:
            if not re.match(r'\d\d', line[0:2]):
                continue
            if keyword not in line:
                continue
            if transform_log_level(line[31]) >= log_level:
                parse_lines.append(line)
    finally:
        f_log.close()

    if len(parse_lines) == 0:
        print 'Warn, no matched log parse_lines, parse finished!'
        return

    f_parse_log = open(logcat_parse_log_for_win, 'w')
    try:
        f_parse_log.writelines(parse_lines)
    finally:
        f_parse_log.flush()
        f_parse_log.close()

def transform_log_level(level):
    if level == 'v' or level == 'V':
        return verbose
    elif level == 'd' or level == 'D':
        return debug
    elif level == 'i' or level == 'I':
        return info
    elif level == 'w' or level == 'W':
        return warn
    elif level == 'e' or level == 'E':
        return error
    elif level == 'f' or level == 'F':
        return fatal
    else:
        print 'invalid log level %s' %(level)
        exit(1)


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
def main_test_setup():
    adb_connect_with_root()
    
    # clear
    os.system(build_command_rm_anr_files())    
    os.system(build_command_rm_tombstone_files())
    remove_log_dir_for_shell()

    # create dirs for shell
    create_log_dir_for_shell()
    if not g_flag_monkey_for_package:
        upload_white_list()
    if g_flag_capture:
        create_captures_dir_for_shell()

    # create dirs for win
    create_log_dir_for_win(log_dir_for_win)
    create_log_dir_for_win(captures_dir_for_win)
    
    get_rom_properties_and_write_file()
    
def main_test_clearup():
    pull_all_testing_logs()
    time.sleep(2)
    adb_disconnect_device()

def monkey_test_main():
    # main_test_setup
    main_test_setup()
    p = subprocess.Popen(build_command_logcat(), shell=True)

    # subprocess handler
    threads = []
    threads.append(build_thread_for_monkey_monitor())
    threads.append(build_thread_for_system_profile_monitor())
    start_all_threads(threads)
#     exec_loop_fn_from_thread(fn_start_specific_sub_activity)

    # monkey test
    if g_flag_monkey_for_package:
        os.system(build_command_monkey_for_package())
    else:
        os.system(build_command_monkey_for_whitelist())

    # clear up
    wait_all_threads_exit(threads)
    
    p.kill()
    main_test_clearup()

def cal_exec_time(fn):
    start = int(time.clock())
    fn()
    during = int(time.clock()) - start
    print '%s cost %d minutes %d seconds.' %(fn.__name__, (during/60), (during%60))

# --------------------------------------------------------------
# Monkey test
# --------------------------------------------------------------
if __name__ == '__main__':

    g_target_ip = '172.17.5.134'
    g_run_num = '01'
    g_run_mins = 10
 
    g_flag_monkey_for_package = True
    g_package_name = 'tv.fun.filemanager'

    cal_exec_time(monkey_test_main)
    parse_logcat_log(warn, g_report_parse_keyword)

    
    print 'Monkey test FINISHED!'
    pass
