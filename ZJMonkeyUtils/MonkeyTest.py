# -*- coding: utf-8 -*-
'''
@author: zhengjin
'''

import subprocess
import os
import time
import re
import cmd
import threading

# --------------------------------------------------------------
# Env vars
# --------------------------------------------------------------
global_target_ip = ''
global_package_name = ''
global_parse_keyword = 'tv.fun'

global_date = time.strftime('%Y%m%d')
global_num = '01'

# set monkey parms
global_monkey_times = '1000000'  # default 1000000
global_flag_crash_ignore = True  # ignore crash or error for monkey
global_flag_test_for_package = True  # false for use whitelist.xml instead
global_flag_capture = False

# set logcat level
global_log_level = 'I'

# set monkey execution time
global_hours = 0
global_mins = 60
global_secs = 0

global_wait_time = 60  # seconds, wait time in loop
global_max_time = 3600 * 4  # seconds, max execution time is 4 hours

# --------------------------------------------------------------
# Path vars
# --------------------------------------------------------------
# log directory path
log_root_path = os.path.join(os.getcwd(), 'MonkeyReprots')
log_dir_for_win = r'%s\%s_%s' %(log_root_path, global_date, global_num)
log_dir_for_shell = '/sdcard/testlogs'

# screen captures path
captures_dir_for_win = r'%s\captures' %(log_dir_for_win)
captures_dir_for_shell = '%s/captures' %(log_dir_for_shell)
capture_for_shell = '%s/capture_%s' %(captures_dir_for_shell, global_date)

# logs of logcat path
logcat_log_for_win = r'{0}\logcat_log_{1}_{2}.log'.format(log_dir_for_win, global_date, global_num)
logcat_log_for_shell = '%s/logcat_log_%s_%s.log' %(log_dir_for_shell, global_date, global_num)

# log path for monkey, local
monkey_log = r'{0}\monkey_log_{1}_{2}.log'.format(log_dir_for_win, global_date, global_num)

# rom props path, local
path_rom_props = r'{0}\rom_props_{1}_{2}.log'.format(log_dir_for_win, global_date, global_num)

# parsed log path, local
logcat_parse_log_for_win = r'{0}\logcat_parse_log_{1}_{2}.log'.format(log_dir_for_win, global_date, global_num)

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
# Build commands
# --------------------------------------------------------------
def build_command_mkdir_testlogs():
    cmd = 'adb shell mkdir %s' %(log_dir_for_shell)
    print cmd
    return cmd

def build_command_mkdir_captures():
    cmd = 'adb shell mkdir %s' %(captures_dir_for_shell)
    print cmd
    return cmd

def build_command_push_whitelist():
    cmd = 'adb push {0} {1}'.format(whitelist_file_for_win, log_dir_for_shell)
    print cmd
    return cmd

def build_command_monkey_for_whitelist():
    times = global_monkey_times
    flag_ignore = global_flag_crash_ignore
    
    monkey_cmd_for_list = r'adb shell monkey --throttle 500 --pkg-whitelist-file {0} '.format(whitelist_file_for_shell)
    monkey_launch_parm = '-c android.intent.category.MONKEY -c android.intent.category.LAUNCHER -c android.intent.category.DEFAULT ' + \
        '--monitor-native-crashes --kill-process-after-error '
    monkey_ignore = '--ignore-crashes --ignore-timeouts --ignore-security-exceptions --ignore-native-crashes '
    monkey_pct = '--pct-touch 0 --pct-motion 0 --pct-trackball 0 --pct-nav 50 ' + \
        '--pct-majornav 30 --pct-syskeys 15 --pct-appswitch 5 --pct-flip 0 --pct-anyevent 0 '
    monkey_format = '-v -v -v {0} > {1}'.format(times, monkey_log)

    if flag_ignore:
        cmd = monkey_cmd_for_list + monkey_launch_parm + monkey_ignore + monkey_pct + monkey_format
    else:
        cmd = monkey_cmd_for_list + monkey_launch_parm + monkey_pct + monkey_format

    print cmd
    return cmd
    
def build_command_monkey_for_package():
    times = global_monkey_times
    flag_ignore = global_flag_crash_ignore
    
    monkey_cmd_for_package = 'adb shell monkey --throttle 500 -p {0} '.format(global_package_name)
    monkey_launch_parm = '-c android.intent.category.MONKEY -c android.intent.category.LAUNCHER -c android.intent.category.DEFAULT ' + \
        '--monitor-native-crashes --kill-process-after-error '
    monkey_ignore = '--ignore-crashes --ignore-timeouts --ignore-security-exceptions --ignore-native-crashes '
    monkey_pct = '--pct-touch 0 --pct-motion 0 --pct-trackball 0 --pct-nav 60 ' + \
        '--pct-majornav 30 --pct-syskeys 10 --pct-appswitch 0 --pct-flip 0 --pct-anyevent 0 '
    monkey_format = '-v -v -v {0} > {1}'.format(times, monkey_log)

    if flag_ignore:
        cmd = monkey_cmd_for_package + monkey_launch_parm + monkey_ignore + monkey_pct + monkey_format
    else:
        cmd = monkey_cmd_for_package + monkey_launch_parm + monkey_pct + monkey_format

    print cmd
    return cmd

def build_command_logcat():
    log_level = global_log_level
    logcat_cmd = 'adb logcat -c && adb logcat -f {0} -v threadtime *:{1}'.format(logcat_log_for_shell, log_level)
    print logcat_cmd
    return logcat_cmd

def build_command_pull_log_files():
    cmd = 'adb pull %s %s' %(log_dir_for_shell, log_dir_for_win)
    print cmd
    return cmd

def build_command_pull_anr_file():
    anr_path = '/data/anr'
    cmd = 'adb pull {0} {1}'.format(anr_path, log_dir_for_win)
    print cmd
    return cmd

def build_command_pull_tombstone_file():
    tombstone_path = '/data/tombstones'
    cmd = 'adb pull {0} {1}'.format(tombstone_path, log_dir_for_win)
    print cmd
    return cmd

# --------------------------------------------------------------
# Shell actions
# --------------------------------------------------------------
def shell_rm_anr():
    rm_path = '/data/anr/*'
    cmd = 'adb shell rm {0}'.format(rm_path)
    print cmd
    return cmd

def shell_rm_tombstone():
    rm_path = '/data/tombstones/*'
    cmd = 'adb shell rm {0}'.format(rm_path)
    print cmd
    return cmd

def get_rom_properties():
    cmd = 'adb shell getprop'
    print cmd
    output = os.popen(cmd)
    
    f = open(path_rom_props, 'w')
    try:
        f.write(output.read())
    finally:
        f.close()

def screen_capture():
    suffix = 'png'
    path = '%s_%s.%s' %(capture_for_shell, time.strftime('%H%M%S'), suffix)
    cmd = 'adb shell screencap -p %s' %(path)
    print cmd
    os.system(cmd)

def remove_log_dir_for_shell():
    cmd = 'adb shell rm -rf %s' %(log_dir_for_shell)
    print cmd
    os.system(cmd)

# --------------------------------------------------------------
# Utils
# --------------------------------------------------------------
def restart_adb_with_root_auth():
    cmd = 'adb root'
    print cmd
    output = os.popen(cmd)
    
    if 'already' in output.read():
        print 'adbd is already running as root'
        return
    
    for i in range(3):
        cmd = 'adb connect %s' %(global_target_ip)
        print cmd
        os.system(cmd)
        time.sleep(3)
        print 'try to connect %d times' %(i + 1)

        if verify_adb_devices_serialno():
            return
    
    print 'Error, when connect to the device with root!'
    exit()

def verify_adb_devices():
    cmd = 'adb devices'
    print cmd
    output = os.popen(cmd)

    port_num = ':5555'
    if port_num in output.read():
        return True
    else:
        return False

def verify_adb_devices_serialno():
    cmd = 'adb get-serialno'
    print cmd
    
    output = os.popen(cmd)
    if 'unknown' in output.read():
        return False
    else:
        return True

def adb_disconnect_device():
    cmd = 'adb disconnect'
    print cmd
    os.system(cmd)

def create_log_dir_for_win(path):
    if os.path.exists(path):
        return
    else:
        os.makedirs(path)
        time.sleep(1)

def create_log_dir_for_shell():
    os.system(build_command_mkdir_testlogs())
    time.sleep(1)

def create_captures_dir_for_shell():
    os.system(build_command_mkdir_captures())
    time.sleep(1)

def upload_white_list():
    # upload whitelist to shell env
    os.system(build_command_push_whitelist())

def pull_logs():
    # the adb connection maybe disconnect when running the monkey
    if verify_adb_devices():
        os.system(build_command_pull_log_files())
        os.system(build_command_pull_anr_file())
        os.system(build_command_pull_tombstone_file())
    else:
        print 'no devices connected, NO files pulled'

def pull_captures():
    if verify_adb_devices():
        cmd = 'adb pull %s %s' %(captures_dir_for_shell, captures_dir_for_win)
        print cmd
        os.system(cmd)
    else:
        print 'no devices connected, NO captures pulled'

# --------------------------------------------------------------
# sub process
# --------------------------------------------------------------
# Kill monkey after specific time from subprocess
def get_monkey_process_id():
    monkey_process_name = 'monkey'
    process_id = ''
    cmd = 'adb shell ps | findstr %s' %(monkey_process_name)
    print cmd

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in p.stdout.readlines():
        if monkey_process_name in line:
            process_id = line[10:].split(' ')[0]
            print 'Monkey process id %s' %(process_id)
            return process_id
    
    print 'Error, the monkey process id is NONE!'
    exit()

def kill_monkey_process(process_id):
    cmd = 'adb shell kill %s' %(process_id)
    print cmd
    os.system(cmd)
    
def monkey_monitor_for_specific_time():
    hours = global_hours
    mins = global_mins
    secs = global_secs

    wait_time_for_monkey_launch = 5
    wait_time = global_wait_time
    spec_running_time = (hours * 3600) + (mins * 60) + secs
    max_time = global_max_time

    if spec_running_time >= max_time:
        print 'spec_time must be less than max_time!'
        exit()

    time.sleep(wait_time_for_monkey_launch)  # wait for monkey process start
    monkey_process_id = get_monkey_process_id()
    
    # LOOP
    start = int(time.clock())
    while True:
        get_monkey_process_id()  # verify monkey is running currently
        time.sleep(wait_time)
        current_time = int(time.clock()) - start
        print 'LOOP, execution time: %d minutes and %d seconds' %((current_time / 60), (current_time % 60))

        if current_time >= spec_running_time or current_time >= max_time:
            kill_monkey_process(monkey_process_id)
            return
        if global_flag_capture:
            screen_capture()
    #end while LOOP

def monkey_monitor_for_specific_time_from_sub_process():
    t = threading.Thread(target = monkey_monitor_for_specific_time)
    t.start()

# loop handler from subprocess
def loop_in_subprocess(fn, wait_time):
    max_time = global_max_time

    # LOOP
    start = int(time.clock())
    while True:
        time.sleep(wait_time)
        end = int(time.clock())
        print 'Looper handler exec after time %d ' %((end - start))
        
        if not verify_adb_devices_serialno():
            return
        if (end - start) >= max_time:
            return
        fn()
    #end while LOOP

def fn_start_specific_sub_activity():
# for test
    activity_name = '.inputsource.InputSourceActivity'
    cmd = 'adb shell am start %s/%s' %(global_package_name, activity_name)
    print cmd
    os.system(cmd)

def exec_loop_fn_from_thread(fn):
    wait_time = 60  # default 60 seconds, to be update
    t = threading.Thread(target = loop_in_subprocess, args = (fn, wait_time))
    t.start()

# --------------------------------------------------------------
# Parse log
# --------------------------------------------------------------
def parse_logcat_log(log_level, key_word):
    
    lines = []
    f_log = open(logcat_log_for_win, 'r')
    try:
        for line in f_log.readlines():
            if not re.match(r'\d\d', line[0:2]):
                continue
            if key_word not in line:
                continue
            if transform_log_level(line[31]) >= log_level:
                lines.append(line)
    finally:
        f_log.close()

    if len(lines) == 0:
        print 'No matched log lines, parse finished.'
        return

    f_parse_log = open(logcat_parse_log_for_win, 'w')
    try:
        f_parse_log.writelines(lines)
    finally:
        f_parse_log.close()
    
    print 'Parse log finished!'

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
        exit()

# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
def setup():
    restart_adb_with_root_auth()
    
    # clear
    os.system(shell_rm_anr())    
    os.system(shell_rm_tombstone())
    remove_log_dir_for_shell()

    # create dirs for shell
    create_log_dir_for_shell()
    if not global_flag_test_for_package:
        upload_white_list()
    if global_flag_capture:
        create_captures_dir_for_shell()

    # create dirs for win
    create_log_dir_for_win(log_dir_for_win)
    create_log_dir_for_win(captures_dir_for_win)
    
    get_rom_properties()
    
def clearup():
    pull_logs()
    time.sleep(2)
    adb_disconnect_device()

def main():
    # setup
    setup()
    p = subprocess.Popen(build_command_logcat(), shell=True)

    # subprocess handler
    monkey_monitor_for_specific_time_from_sub_process()
#     exec_loop_fn_from_thread(fn_start_specific_sub_activity)

    # monkey test
    if global_flag_test_for_package:
        os.system(build_command_monkey_for_package())
    else:
        os.system(build_command_monkey_for_whitelist())

    # clear up
    p.kill()
    clearup()

def cal_exec_time(fn):
    start = int(time.clock())
    fn()
    end = int(time.clock())
    during = end - start
    print 'Monkey test FINISHED!'
    print '%s cost %d minutes %d seconds.' %(fn.__name__, (during / 60), (during % 60))

# --------------------------------------------------------------
# Monkey test
# --------------------------------------------------------------
if __name__ == '__main__':

    global_target_ip = '172.17.5.134'
    global_num = '01'
    global_mins = 60

    global_flag_test_for_package = False
#     global_package_name = 'tv.fun.filemanager'

    cal_exec_time(main)
#     parse_logcat_log(warn, global_parse_keyword)

    pass