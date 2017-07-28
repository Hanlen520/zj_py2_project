# -*- coding: utf-8 -*-
'''
Created on 2016-3-15

@author: zhengjin

1) Run monkey test in main process.
2) Run monkey monitor in subprocess (verify monkey process, captures).
3) Run profile monitor in subprocess, includes CPU and memory.
4) Generate monkey reports, contains logcat log, monkey log and anr files...
'''

import os
import time
import subprocess
import threading

from ZJPyUtils import WinSysUtils, AdbUtils
from ZJAndroidMonitor import MonitorRunner

# --------------------------------------------------------------
# Constants
# --------------------------------------------------------------
PKG_NAME_LAUNCHER = 'com.bestv.ott'
PKG_NAME_SETTINGS = 'tv.fun.settings'
PKG_NAME_FILEMANAGER = 'tv.fun.filemanager'
PKG_NAME_WEATHER = 'tv.fun.weather'
PKG_NAME_TV_GUIDE = 'tv.fun.instructions'

MONKEY_TOTAL_RUN_TIMES = '1000000'  # default 1000000

MAX_RUN_TIME = 12 * 60 * 60  # seconds, max execution time is 12 hours
WAIT_TIME_IN_LOOP = 60  # seconds, wait time in loop

IS_MONKEY_CRASH_IGNORE = True  # ignore crash or error for monkey
IS_CAPTURE = False
IS_PRINT_LOG = False

LOGCAT_LOG_LEVEL = 'I'


# --------------------------------------------------------------
# Path Variables
# --------------------------------------------------------------
# log directory path
g_log_root_path = ''
g_log_dir_path_for_win = ''
g_log_dir_path_for_shell = ''

# screen captures path
g_captures_dir_path_for_win = ''
g_captures_dir_path_for_shell = ''
g_capture_path_for_shell = ''

# profile log path
g_profile_log_dir_path = ''

# logcat log path
g_logcat_log_path_for_shell = ''

# monkey log, local
g_monkey_log_path = ''

# rom props path, local
g_rom_props_file_path = ''

# whitelist path
g_whitelist_file_path_for_win = ''
g_whitelist_file_path_for_shell = ''

def init_path_vars():
    cur_date = WinSysUtils.get_current_date()
    
    global g_log_root_path
    global g_log_dir_path_for_win
    global g_log_dir_path_for_shell
    g_log_root_path = os.path.join(os.getcwd(), 'MonkeyReprots', cur_date)
    g_log_dir_path_for_win = r'%s\%s_%s' % (g_log_root_path, cur_date, g_run_num)
    g_log_dir_path_for_shell = '/sdcard/monkey_test_logs'
    
    # profile log path
    global g_profile_log_dir_path
    g_profile_log_dir_path = os.path.join(g_log_dir_path_for_win, 'profile_logs')
    
    # screen captures path
    global g_captures_dir_path_for_win
    global g_captures_dir_path_for_shell
    global g_capture_path_for_shell
    g_captures_dir_path_for_win = r'%s\captures' % g_log_dir_path_for_win
    g_captures_dir_path_for_shell = '%s/captures' % g_log_dir_path_for_shell
    g_capture_path_for_shell = '%s/capture_%s' % (g_captures_dir_path_for_shell, cur_date)
    
    # logcat log path
    global g_logcat_log_path_for_shell
    g_logcat_log_path_for_shell = '%s/logcat_log.log' % g_log_dir_path_for_shell
    
    # monkey log, local
    global g_monkey_log_path
    g_monkey_log_path = r'%s\monkey_log.log' % g_log_dir_path_for_win
    
    # rom props path, local
    global g_rom_props_file_path
    g_rom_props_file_path = r'%s\rom_props.log' % g_log_dir_path_for_win
    
    # whitelist path
    global g_whitelist_file_path_for_win
    global g_whitelist_file_path_for_shell
    g_whitelist_file_path_for_win = os.path.join(os.getcwd(), 'whitelist.txt')
    g_whitelist_file_path_for_shell = '%s/whitelist.txt' % g_log_dir_path_for_shell


# --------------------------------------------------------------
# Build Shell Commands
# --------------------------------------------------------------
def build_monkey_command():
    monkey_cmd_for_package = 'adb shell monkey --throttle 500 -p %s' % g_package_name
    monkey_cmd_for_list = r'adb shell monkey --throttle 500 --pkg-whitelist-file %s' % g_whitelist_file_path_for_shell

    monkey_launch_params = '-c android.intent.category.MONKEY -c android.intent.category.LAUNCHER -c ' + \
        'android.intent.category.DEFAULT --monitor-native-crashes --kill-process-after-error'
    monkey_ignore = '--ignore-crashes --ignore-timeouts --ignore-security-exceptions --ignore-native-crashes'
    monkey_actions_pct = '--pct-touch 0 --pct-motion 0 --pct-trackball 0 --pct-nav 60 ' + \
        '--pct-majornav 30 --pct-syskeys 10 --pct-appswitch 0 --pct-flip 0 --pct-anyevent 0'
    monkey_format = '-v -v -v %s > %s' % (MONKEY_TOTAL_RUN_TIMES, g_monkey_log_path)

    if g_is_monkey_for_package:
        if IS_MONKEY_CRASH_IGNORE:
            return ' '.join((monkey_cmd_for_package, monkey_launch_params, monkey_ignore, monkey_actions_pct, monkey_format))
        else:
            return ' '.join((monkey_cmd_for_package, monkey_launch_params, monkey_actions_pct, monkey_format))
    else:  # for whitelist
        if IS_MONKEY_CRASH_IGNORE:
            return ' '.join((monkey_cmd_for_list, monkey_launch_params, monkey_ignore, monkey_actions_pct, monkey_format))
        else:
            return ' '.join((monkey_cmd_for_list, monkey_launch_params, monkey_actions_pct, monkey_format))

def build_command_logcat():
    logcat_cmd = 'adb logcat -c && adb logcat -f %s -v threadtime *:%s' % (g_logcat_log_path_for_shell, LOGCAT_LOG_LEVEL)
    return logcat_cmd

def build_command_pull_anr_file():
    anr_files_path = '/data/anr'
    cmd = 'adb pull %s %s' % (anr_files_path, g_log_dir_path_for_win)
    return cmd

def build_command_pull_tombstone_file():
    tombstone_files_path = '/data/tombstones'
    cmd = 'adb pull %s %s' % (tombstone_files_path, g_log_dir_path_for_win)
    return cmd

def build_command_rm_anr_files():
    cmd = 'adb shell rm /data/anr/*'
    return cmd

def build_command_rm_tombstone_files():
    cmd = 'adb shell rm /data/tombstones/*'
    return cmd


# --------------------------------------------------------------
# Run Shell Commands
# --------------------------------------------------------------
def run_system_command(cmd):
    if IS_PRINT_LOG:
        print cmd
    if os.system(cmd) != 0:
        print 'WARN, failed to run command: ' + cmd

def run_cmd_monkey():
    cmd_monkey_for_whitelist = build_monkey_command()
    print cmd_monkey_for_whitelist
    run_system_command(cmd_monkey_for_whitelist)

def run_cmd_screen_capture():
    capture_file_path = '%s_%s.%s' % (g_capture_path_for_shell, time.strftime('%H%M%S'), 'png')
    cmd = 'adb shell screencap -p %s' % capture_file_path
    run_system_command(cmd)
    
def run_cmd_adb_connect():
    cmd = 'adb connect %s' % g_target_ip
    run_system_command(cmd)
    
def run_cmd_adb_root_from_subprocess():
    cmd = 'adb root'
    print 'run adb root and reconnect.'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()

    lines_error = p.stderr.readlines()
    if len(lines_error) > 0:
        for line in lines_error:
            print line
        print 'Error, adb root failed!'
        return False

    lines_output = p.stdout.readlines()
    if len(lines_output) == 0:
        print 'No output from adb root.'
        return True
    for line in lines_output:
        if 'already' in line:
            print 'adbd is already running as root.'
            return True
        elif 'adbd as root' in line:
            print 'adb root success.'
            return True
        else:
            print 'Error, adb root failed.'
            return False

def run_cmd_adb_root_from_subprocess_and_kill():
    cmd = 'adb root'
    print 'run adb root and reconnect.'
    p = subprocess.Popen(cmd, shell=True)
    time.sleep(1)
    p.kill()

def run_cmd_logcat_from_subprocess_and_ret_process():
    p = subprocess.Popen(build_command_logcat(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# below logic will cause program pending until the adb logcat cmd done
#     lines_error = p.stderr.readlines()
#     if len(lines_error) > 0:
#         for line in lines_error:
#             print line
#         print 'Error, when start logcat!'
#         exit(1)
    return p


# --------------------------------------------------------------
# Adb Shell Utils
# --------------------------------------------------------------
def adb_connect_with_root(device_ip):
    if not AdbUtils.adb_connect_to_device(device_ip):  # adb connect
        print 'Error, when adb connect to the device!'
        exit(1)

# fix pending issue when run adb root command
#     if not run_cmd_adb_root_from_subprocess():
#         print 'Error, when run adb as root!'
#         exit(1)
    run_cmd_adb_root_from_subprocess_and_kill()

    if not AdbUtils.adb_connect_to_device(device_ip):  # adb connect as root
        print 'Error, when adb connect to the device with root!'
        exit(1)

def set_tv_audio_volume_to_low():
    print 'setting tv audio volume to low...'
    cmd = 'adb shell input keyevent KEYCODE_VOLUME_DOWN'
    for i in xrange(20):
        run_system_command(cmd)
        time.sleep(0.3)

def get_monkey_process_id():
    monkey_p_name = 'monkey'
    return get_process_id_by_name(monkey_p_name)

def get_logcat_process_id():
    logcat_p_name = 'logcat'
    return get_process_id_by_name(logcat_p_name)

def get_process_id_by_name(p_name):
    process_id = ''
    cmd = 'adb shell ps | findstr %s' % p_name
    if IS_PRINT_LOG:
        print cmd

    for line in os.popen(cmd).readlines():
        if p_name in line:
            process_id = line.split()[1]
            return process_id
    return process_id

def kill_process_by_id(p_id):
    cmd = 'adb shell kill %s' % p_id
    run_system_command(cmd)

def get_rom_properties_and_write_file():
    dir_path = os.path.dirname(g_rom_props_file_path)
    if not os.path.exists(dir_path):
        print 'Error, the directory %s is NOT exist!' % dir_path
    
    if os.path.exists(g_rom_props_file_path):
        print 'Warn, the file %s is exist!' % g_rom_props_file_path
    
    cmd = 'adb shell getprop > %s' % g_rom_props_file_path  # override existing file content
    run_system_command(cmd)


# --------------------------------------------------------------
# Functions: IO and report files
# --------------------------------------------------------------
def verify_device_is_busy(lines):
    for line in lines:
        if 'busy' in line:
            print line
            print 'Error, monkey test exit because of device busy!'
            exit(1)

def remove_testing_log_files_for_shell():
    cmd = 'adb shell rm -rf %s' % g_log_dir_path_for_shell
    if IS_PRINT_LOG:
        print cmd
    verify_device_is_busy(os.popen(cmd).readlines())

def remove_anr_and_tombstone_files():
    run_system_command(build_command_rm_anr_files())
    run_system_command(build_command_rm_tombstone_files())

def create_log_dir_for_win(path):
    if os.path.exists(path):
        return
    os.makedirs(path)
    time.sleep(1)

def create_log_dir_for_shell(dir_path):
    cmd = 'adb shell mkdir %s' % (dir_path)
    if IS_PRINT_LOG:
        print cmd
    verify_device_is_busy(os.popen(cmd).readlines())
    
def push_whitelist_file_to_shell():
    # upload whitelist to shell env
    cmd = 'adb push %s %s' % (g_whitelist_file_path_for_win, g_log_dir_path_for_shell)
    run_system_command(cmd)
    
def pull_all_testing_logs():
    # the adb connection maybe disconnect when running the monkey
    if not AdbUtils.verify_adb_devices_connect():
        print 'Warn, no devices connected, NO files pulled!'
        return

    cmd_pull_logcat_log = 'adb pull %s %s' % (g_logcat_log_path_for_shell, g_log_dir_path_for_win)
    run_system_command(cmd_pull_logcat_log)
    cmd_pull_whitelist = 'adb pull %s %s' % (g_whitelist_file_path_for_shell, g_log_dir_path_for_win)
    run_system_command(cmd_pull_whitelist)

    run_system_command(build_command_pull_anr_file())
    run_system_command(build_command_pull_tombstone_file())

def pull_captures():
    if not AdbUtils.verify_adb_devices_connect():
        print 'Warn, no devices connected, NO captures pulled!'
        return
    cmd = 'adb pull %s %s' % (g_captures_dir_path_for_shell, g_captures_dir_path_for_win)
    run_system_command(cmd)


# --------------------------------------------------------------
# Threads
# --------------------------------------------------------------
def wait_for_monkey_process_start():
    monkey_process_id = ''
    try_times = 3
    wait_time_for_monkey_launch = 3
    
    for i in xrange(0, try_times):
        monkey_process_id = get_monkey_process_id()
        if monkey_process_id != '':
            break
        time.sleep(wait_time_for_monkey_launch)
    return monkey_process_id

def thread_main_monkey_monitor_at_interval():
    spec_run_time = g_run_mins * 60
    if spec_run_time >= MAX_RUN_TIME:
        print 'Warn, spec_time must be less than max_time(4 hours)!'
        exit(1)

    monkey_p_id = wait_for_monkey_process_start()
    if monkey_p_id == '':
        print 'Error, the monkey process is NOT started!'
        exit(1)
    
    # LOOP
    start = int(time.clock())
    while 1:
        if get_monkey_process_id() == '':
            print 'Error, the monkey process is NOT running!'
            return
        if IS_CAPTURE:
            run_cmd_screen_capture()
        
        current_time = int(time.clock()) - start
        print 'Monkey is running... %d minutes and %d seconds' % ((current_time / 60), (current_time % 60))
        if (current_time >= spec_run_time) or (current_time >= MAX_RUN_TIME):
            kill_process_by_id(monkey_p_id)  # Kill monkey after specific time
            break
        time.sleep(WAIT_TIME_IN_LOOP)

def build_thread_for_monkey_monitor():
    t = threading.Thread(target=thread_main_monkey_monitor_at_interval)
    return t

def build_thread_for_profile_monitor():
    MonitorRunner.report_root_path = g_profile_log_dir_path
    MonitorRunner.pkg_name = g_package_name
    MonitorRunner.run_number = g_run_num
    MonitorRunner.run_time = g_run_mins * 60
    MonitorRunner.monitor_interval = g_profile_monitor_interval
    
    MonitorRunner.g_is_for_pkg = True
    MonitorRunner.g_is_mem_monitor_by_dumpsys = False

    t = threading.Thread(target=MonitorRunner.monitor_runner_main)
    return t

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
# Monkey Test Main
# --------------------------------------------------------------
def main_test_setup():
    adb_connect_with_root(g_target_ip)
    set_tv_audio_volume_to_low()
    
    # shell env setup
    init_path_vars()
    remove_anr_and_tombstone_files()
    remove_testing_log_files_for_shell()

    create_log_dir_for_shell(g_log_dir_path_for_shell)
    if not g_is_monkey_for_package:
        push_whitelist_file_to_shell()
    if IS_CAPTURE:
        create_log_dir_for_shell(g_captures_dir_path_for_shell)
        create_log_dir_for_win(g_captures_dir_path_for_win)

    # win env setup
    create_log_dir_for_win(g_log_dir_path_for_win)
    get_rom_properties_and_write_file()
    
def main_test_clearup():
    pull_all_testing_logs()
    kill_process_by_id(get_logcat_process_id())  # stop logcat

def main_test():
    logcat_sub_process = run_cmd_logcat_from_subprocess_and_ret_process()
    
    threads = []
    if g_is_profile_monitor:
        threads.append(build_thread_for_profile_monitor())
    threads.append(build_thread_for_monkey_monitor())
    start_all_threads_in_pool(threads)

    run_cmd_monkey()  # run monkey

    wait_all_threads_exit(threads)
    kill_subprocess(logcat_sub_process)

def monkey_test_main():
    start = int(time.clock())
    
    main_test_setup()
    main_test()
    main_test_clearup()

    during = int(time.clock()) - start
    print 'Monkey finish and execution time: %d minutes %d seconds' % ((during / 60), (during % 60))


if __name__ == '__main__':

    g_target_ip = '172.17.5.104'
    g_run_num = '01'
    g_run_mins = 60

    # if false, run monkey for whitelist as default
    g_is_monkey_for_package = False
    g_package_name = PKG_NAME_LAUNCHER  # for both monkey and profile monitor

    g_is_profile_monitor = True
    g_profile_monitor_interval = 1

    monkey_test_main()
    
    print 'Monkey test DONE!'
