# -*- coding: utf-8 -*-
'''
Created on 2016-3-15

@author: zhengjin

Run monkey test by specified time, 
and generate monkey reports and system profile reports at the same time.

'''

import subprocess
import os
import time
import re
import threading
from ZJAndroidMonitor import MonitorRunner
from ZJAndroidMonitor import MonitorUtils

# --------------------------------------------------------------
# Env vars
# --------------------------------------------------------------
g_pkg_settings = 'tv.fun.settings'
g_pkg_filemanager = 'tv.fun.filemanager'
g_pkg_weather = 'tv.fun.weather'

g_target_ip = ''
g_package_name = ''

# default monkey parms
g_monkey_run_times = '1000000'  # default 1000000
g_flag_monkey_crash_ignore = True  # ignore crash or error for monkey

g_flag_monkey_for_package = True
g_flag_monkey_for_whitelist = False

g_max_run_time = 3600 * 4  # seconds, max execution time is 4 hours
g_loop_wait_time = 60  # seconds, wait time in loop

g_flag_capture = False
g_flag_profile_monitor = False
g_flag_print_log = False
g_flag_parse_report = False

g_cur_date = time.strftime('%Y%m%d')
g_run_num = '01'

# default monkey execution time
g_run_hours = 0
g_run_mins = 30
g_run_secs = 0

# default logcat level
g_log_level = 'I'


# --------------------------------------------------------------
# Path vars
# --------------------------------------------------------------
# log directory path
g_log_root_path = ''
g_log_dir_for_win = ''
g_log_dir_for_shell = ''

# screen captures path
g_captures_dir_for_win = ''
g_captures_dir_for_shell = ''
g_capture_path_for_shell = ''

# logs of logcat path
g_logcat_log_for_win = ''
g_logcat_log_for_shell = ''

# log path for monkey, local
g_monkey_log = ''

# rom props path, local
g_path_rom_props = ''

# parsed log path, local
g_logcat_parse_log_for_win = ''

# white list path
g_whitelist_file_for_win = ''
g_whitelist_file_for_shell = ''

def init_path_vars():
    global g_log_root_path
    global g_log_dir_for_win
    global g_log_dir_for_shell
    g_log_root_path = os.path.join(os.getcwd(), 'MonkeyReprots', g_cur_date)
    g_log_dir_for_win = r'%s\%s_%s' %(g_log_root_path, g_cur_date, g_run_num)
    g_log_dir_for_shell = '/sdcard/testlogs'
    
    # screen captures path
    global g_captures_dir_for_win
    global g_captures_dir_for_shell
    global g_capture_path_for_shell
    g_captures_dir_for_win = r'%s\captures' %(g_log_dir_for_win)
    g_captures_dir_for_shell = '%s/captures' %(g_log_dir_for_shell)
    g_capture_path_for_shell = '%s/capture_%s' %(g_captures_dir_for_shell, g_cur_date)
    
    # logs of logcat path
    global g_logcat_log_for_win
    global g_logcat_log_for_shell
    g_logcat_log_for_win = r'%s\logcat_log_%s_%s.log' %(g_log_dir_for_win, g_cur_date, g_run_num)
    g_logcat_log_for_shell = '%s/logcat_log_%s_%s.log' %(g_log_dir_for_shell, g_cur_date, g_run_num)
    
    # log path for monkey, local
    global g_monkey_log
    g_monkey_log = r'%s\monkey_log_%s_%s.log' %(g_log_dir_for_win, g_cur_date, g_run_num)
    
    # rom props path, local
    global g_path_rom_props
    g_path_rom_props = r'%s\rom_props_%s_%s.log' %(g_log_dir_for_win, g_cur_date, g_run_num)
    
    # parsed log path, local
    global g_logcat_parse_log_for_win
    g_logcat_parse_log_for_win = r'%s\logcat_parse_log_%s_%s.log' %(g_log_dir_for_win, g_cur_date, g_run_num)
    
    # white list path
    global g_whitelist_file_for_win
    global g_whitelist_file_for_shell
    g_whitelist_file_for_win = os.path.join(os.getcwd(), 'whitelist.txt')
    g_whitelist_file_for_shell = '%s/whitelist.txt' %(g_log_dir_for_shell)


# --------------------------------------------------------------
# Build shell commands
# --------------------------------------------------------------
def build_command_monkey_for_whitelist():
    monkey_cmd_for_list = r'adb shell monkey --throttle 500 --pkg-whitelist-file %s ' %(g_whitelist_file_for_shell)
    monkey_launch_parm = '-c android.intent.category.MONKEY -c android.intent.category.LAUNCHER -c android.intent.category.DEFAULT ' + \
        '--monitor-native-crashes --kill-process-after-error '
    monkey_ignore = '--ignore-crashes --ignore-timeouts --ignore-security-exceptions --ignore-native-crashes '
    monkey_pct = '--pct-touch 0 --pct-motion 0 --pct-trackball 0 --pct-nav 50 ' + \
        '--pct-majornav 30 --pct-syskeys 15 --pct-appswitch 5 --pct-flip 0 --pct-anyevent 0 '
    monkey_format = '-v -v -v %s > %s' %(g_monkey_run_times, g_monkey_log)

    if g_flag_monkey_crash_ignore:
        return monkey_cmd_for_list + monkey_launch_parm + monkey_ignore + monkey_pct + monkey_format
    else:
        return monkey_cmd_for_list + monkey_launch_parm + monkey_pct + monkey_format
    
def build_command_monkey_for_package():
    monkey_cmd_for_package = 'adb shell monkey --throttle 500 -p %s ' %(g_package_name)
    monkey_launch_parm = '-c android.intent.category.MONKEY -c android.intent.category.LAUNCHER -c android.intent.category.DEFAULT ' + \
        '--monitor-native-crashes --kill-process-after-error '
    monkey_ignore = '--ignore-crashes --ignore-timeouts --ignore-security-exceptions --ignore-native-crashes '
    monkey_pct = '--pct-touch 0 --pct-motion 0 --pct-trackball 0 --pct-nav 60 ' + \
        '--pct-majornav 30 --pct-syskeys 10 --pct-appswitch 0 --pct-flip 0 --pct-anyevent 0 '
    monkey_format = '-v -v -v %s > %s' %(g_monkey_run_times, g_monkey_log)

    if g_flag_monkey_crash_ignore:
        return monkey_cmd_for_package + monkey_launch_parm + monkey_ignore + monkey_pct + monkey_format
    else:
        return monkey_cmd_for_package + monkey_launch_parm + monkey_pct + monkey_format

def build_command_logcat():
    logcat_cmd = 'adb logcat -c && adb logcat -f %s -v threadtime *:%s' %(g_logcat_log_for_shell, g_log_level)
    return logcat_cmd

def build_command_pull_anr_file():
    anr_files_path = '/data/anr'
    cmd = 'adb pull %s %s' %(anr_files_path, g_log_dir_for_win)
    return cmd

def build_command_pull_tombstone_file():
    tombstone_files_path = '/data/tombstones'
    cmd = 'adb pull %s %s' %(tombstone_files_path, g_log_dir_for_win)
    return cmd

def build_command_rm_anr_files():
    cmd = 'adb shell rm /data/anr/*'
    return cmd

def build_command_rm_tombstone_files():
    cmd = 'adb shell rm /data/tombstones/*'
    return cmd


# --------------------------------------------------------------
# Run shell commands
# --------------------------------------------------------------
def run_system_command(cmd):
    if g_flag_print_log:
        print cmd
    os.system(cmd)

def run_cmd_monkey_for_package():
    cmd_monkey_for_pkg = build_command_monkey_for_package()
    print cmd_monkey_for_pkg
    run_system_command(cmd_monkey_for_pkg)
    
def run_cmd_monkey_for_whitelist():
    cmd_monkey_for_whitelist = build_command_monkey_for_whitelist()
    print cmd_monkey_for_whitelist
    run_system_command(cmd_monkey_for_whitelist)

def run_cmd_screen_capture():
    capture_file_path = '%s_%s.%s' %(g_capture_path_for_shell, time.strftime('%H%M%S'), 'png')
    cmd = 'adb shell screencap -p %s' %(capture_file_path)
    run_system_command(cmd)
    
def run_cmd_adb_connect():
    cmd = 'adb connect %s' %(g_target_ip)
    run_system_command(cmd)
    
def run_cmd_adb_disconnect():
    cmd = 'adb disconnect'
    run_system_command(cmd)
    
def run_cmd_adb_root_from_subprocess():
    cmd = 'adb root'
    if g_flag_print_log:
        print cmd
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()

    lines_error = p.stderr.readlines()
    if len(lines_error) > 0:
        for line in lines_error:
            print line
        print 'Error, adb root failed!'
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

def run_cmd_adb_logcat_from_subprocess():
    p = subprocess.Popen(build_command_logcat(),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
# below logic will cause program pending until the adb logcat cmd done
#     lines_error = p.stderr.readlines()
#     if len(lines_error) > 0:
#         for line in lines_error:
#             print line
#         print 'Error, when start logcat!'
#         exit(1)
    return p


# --------------------------------------------------------------
# Adb shell utils
# --------------------------------------------------------------
def verify_adb_devices():
    cmd = 'adb devices'
    if g_flag_print_log:
        print cmd

    if ':5555' in os.popen(cmd).read():
        return True
    else:
        return False

def verify_adb_devices_serialno():
    cmd = 'adb get-serialno'
    if g_flag_print_log:
        print cmd

    if 'unknown' in os.popen(cmd).read():
        return False
    else:
        return True

def try_to_adb_connect_to_device():
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
    if not try_to_adb_connect_to_device():  # adb connect
        print 'Error, when adb connect to the device!'
        exit(1)
        
    if not run_cmd_adb_root_from_subprocess():
        print 'Error, when run adb as root!'
        exit(1)

    if not try_to_adb_connect_to_device():   # adb connect as root
        print 'Error, when adb connect to the device with root!'
        exit(1)

def get_monkey_process_id():
    process_id = ''
    monkey_process_name = 'monkey'
    cmd = 'adb shell ps | findstr %s' %(monkey_process_name)
    if g_flag_print_log:
        print cmd

    for line in os.popen(cmd).readlines():
        if monkey_process_name in line:
            process_id = line[10:].split(' ')[0]
            print 'Monkey process id %s' %(process_id)
            return process_id

    return process_id

def kill_monkey_process(process_id):
    cmd = 'adb shell kill %s' %(process_id)
    run_system_command(cmd)

def get_rom_properties_and_write_file():
    dir_path = os.path.dirname(g_path_rom_props)
    if not os.path.exists(dir_path):
        print 'Error, the directory %s is NOT exist!' %(dir_path)
    
    if os.path.exists(g_path_rom_props):
        print 'Warn, the file %s is exist.' %(g_path_rom_props)
    
    cmd = 'adb shell getprop > %s' %(g_path_rom_props)   # override existing file content
    run_system_command(cmd)


# --------------------------------------------------------------
# Function: IO, and report files
# --------------------------------------------------------------
def verify_device_is_busy(lines):
    for line in lines:
        if 'busy' in line:
            print line
            print 'Error, monkey test exit because of device busy!'
            exit(1)

def remove_testing_log_files_for_shell():
    cmd = 'adb shell rm -rf %s' %(g_log_dir_for_shell)
    if g_flag_print_log:
        print cmd
    verify_device_is_busy(os.popen(cmd).readlines())

def remove_anr_and_tombstone_files():
    run_system_command(build_command_rm_anr_files())
    run_system_command(build_command_rm_tombstone_files())

def create_log_dir_for_win(path):
    if os.path.exists(path):
        return
    else:
        os.makedirs(path)
        time.sleep(1)

def create_log_dir_for_shell(dir_path):
    cmd = 'adb shell mkdir %s' %(dir_path)
    if g_flag_print_log:
        print cmd
    verify_device_is_busy(os.popen(cmd).readlines())
    
def push_whitelist_file_to_shell():
    # upload whitelist to shell env
    cmd = 'adb push %s %s' %(g_whitelist_file_for_win, g_log_dir_for_shell)
    run_system_command(cmd)
    
def pull_all_testing_logs():
    cmd_pull_log_files = 'adb pull %s %s' %(g_log_dir_for_shell, g_log_dir_for_win)
    # the adb connection maybe disconnect when running the monkey
    if verify_adb_devices():
        run_system_command(cmd_pull_log_files)
        run_system_command(build_command_pull_anr_file())
        run_system_command(build_command_pull_tombstone_file())
    else:
        print 'Warn, no devices connected, NO files pulled!'

def pull_captures():
    if verify_adb_devices():
        cmd = 'adb pull %s %s' %(g_captures_dir_for_shell, g_captures_dir_for_win)
        run_system_command(cmd)
    else:
        print 'Warn, no devices connected, NO captures pulled!'


# --------------------------------------------------------------
# Threads main
# --------------------------------------------------------------
def wait_for_monkey_process_start():
    monkey_process_id = ''
    try_times = 3
    wait_time_for_monkey_launch = 3
    
    for i in range(0,try_times):
        monkey_process_id = get_monkey_process_id()
        if monkey_process_id != '':
            break
        time.sleep(wait_time_for_monkey_launch)

    return monkey_process_id

# Kill monkey after specific time from subprocess
def thread_main_monkey_monitor_at_specific_time():
    spec_running_time = (g_run_hours * 3600) + (g_run_mins * 60) + g_run_secs
    if spec_running_time >= g_max_run_time:
        print 'Warn, spec_time must be less than max_time(4 hours)!'
        exit(1)

    monkey_process_id = wait_for_monkey_process_start()
    if monkey_process_id == '':
        print 'Error, the monkey process is NOT start!'
        exit(1)
    
    # LOOP
    start = int(time.clock())
    while True:
        if get_monkey_process_id() == '':
            print 'Error, the monkey process is NOT running!'
            return
        if g_flag_capture:
            run_cmd_screen_capture()
        
        current_time = int(time.clock()) - start
        print 'LOOP, execution time: %d minutes and %d seconds' %((current_time / 60), (current_time % 60))
        if (current_time >= spec_running_time) or (current_time >= g_max_run_time):
            kill_monkey_process(monkey_process_id)
            break

        time.sleep(g_loop_wait_time)
    # LOOP end

def build_thread_for_monkey_monitor():
    t = threading.Thread(target = thread_main_monkey_monitor_at_specific_time)
    return t

def build_thread_for_system_profile_monitor():
    MonitorRunner.g_pkg_name_all = g_package_name
    MonitorRunner.g_run_num_all = g_run_num
    MonitorRunner.g_run_time_all = g_run_mins * MonitorUtils.g_min
    MonitorRunner.g_suffix_all = '%s_%s' %(g_cur_date, g_run_num)
    
    t = threading.Thread(target=MonitorRunner.monitor_runner_main)
    return t

def build_threads_pool(*arg):
    threads = []
    for t in arg:
        if t is not None:
            threads.append(t)
    return threads

def start_all_threads_in_pool(threads):
    for t in threads:
        if t is not None:
            t.start()

def wait_all_threads_exit(threads):
    for t in threads:
        if t is not None:
            t.join()

def kill_subprocess(p):
    if p is not None:
        p.kill()


# --------------------------------------------------------------
# Parse log
# --------------------------------------------------------------
g_verbose = 0
g_debug = 1
g_info = 2
g_warn = 3
g_error = 4
g_fatal = 5

def parse_logcat_log(g_logcate_log_level, keyword):
    parse_lines = []
    
    f_log = open(g_logcat_log_for_win, 'r')
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
            if transform_log_level(line[31]) >= g_logcate_log_level:
                parse_lines.append(line)
    finally:
        f_log.close()

    if len(parse_lines) == 0:
        print 'Warn, no matched log parse_lines, parse finished!'
        return

    f_parse_log = open(g_logcat_parse_log_for_win, 'w')
    try:
        f_parse_log.writelines(parse_lines)
    finally:
        f_parse_log.flush()
        f_parse_log.close()

def transform_log_level(level):
    if level == 'v' or level == 'V':
        return g_verbose
    elif level == 'd' or level == 'D':
        return g_debug
    elif level == 'i' or level == 'I':
        return g_info
    elif level == 'w' or level == 'W':
        return g_warn
    elif level == 'e' or level == 'E':
        return g_error
    elif level == 'f' or level == 'F':
        return g_fatal
    else:
        print 'Error, invalid log level %s' %(level)
        exit(1)


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
def main_test_setup():
    init_path_vars()
    adb_connect_with_root()
    
    # shell env setup
    remove_anr_and_tombstone_files()
    remove_testing_log_files_for_shell()

    create_log_dir_for_shell(g_log_dir_for_shell)
    if g_flag_monkey_for_whitelist:
        push_whitelist_file_to_shell()
    if g_flag_capture:
        create_log_dir_for_shell(g_captures_dir_for_shell)

    # win env setup
    create_log_dir_for_win(g_log_dir_for_win)
    if g_flag_capture:
        create_log_dir_for_win(g_captures_dir_for_win)
    get_rom_properties_and_write_file()
    
def main_test_clearup():
    pull_all_testing_logs()
#     run_cmd_adb_disconnect()

def main_test():
    logcat_sub_process = run_cmd_adb_logcat_from_subprocess()
    
    if g_flag_profile_monitor:
        threads = build_threads_pool(build_thread_for_monkey_monitor(), build_thread_for_system_profile_monitor())
    else:  # default
        threads = build_threads_pool(build_thread_for_monkey_monitor())
    start_all_threads_in_pool(threads)

    # run monkey test
    if g_flag_monkey_for_package:
        run_cmd_monkey_for_package()
    elif g_flag_monkey_for_whitelist:
        run_cmd_monkey_for_whitelist()
    else:
        print 'Error, both monkey for package or whitelist flags are set to False!'
        exit(1)

    wait_all_threads_exit(threads)
    kill_subprocess(logcat_sub_process)

def monkey_test_main():
    main_test_setup()
    main_test()
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

    g_target_ip = '172.17.5.106'
    g_run_num = '01'
    g_run_mins = 60
    g_package_name = g_pkg_weather

    g_flag_monkey_for_package = False
    g_flag_monkey_for_whitelist = True
    g_flag_profile_monitor = False

    cal_exec_time(monkey_test_main)

    if g_flag_parse_report:
        report_parse_keyword = 'tv.fun'
        parse_logcat_log(g_warn, report_parse_keyword)

    print 'Monkey test FINISHED!'
    pass
