# -*- coding: utf-8 -*-
'''
Created on 2016-3-11

@author: zhengjin
'''

import os
import subprocess
import time

# --------------------------------------------------------------
# Vars
# --------------------------------------------------------------
g_wait_time_between_cmds = 1

# Key Events
g_cmd_key_up = 'KEYCODE_DPAD_UP'
g_cmd_key_down = 'KEYCODE_DPAD_DOWN'
g_cmd_key_left = 'KEYCODE_DPAD_LEFT'
g_cmd_key_right = 'KEYCODE_DPAD_RIGHT'
g_cmd_key_enter = 'KEYCODE_ENTER'
g_cmd_key_back = 'KEYCODE_BACK'
g_cmd_key_home = 'KEYCODE_HOME'

# --------------------------------------------------------------
#  Build And Format Commands
# --------------------------------------------------------------
def build_repeat_cmd(cmds, cmd, times):
    for i in range(0, times):
        cmds.append(cmd)
    return cmds

def append_exit_cmd(cmds):
    cmds.append('exit')
    return cmds

def format_cmds_to_cmd_for_communicate(cmds):
    output = ''
    for cmd in cmds:
        output += '%s\n' %(cmd)
    return output

# --------------------------------------------------------------
#  Run Multiple Commands Utils
# --------------------------------------------------------------
def run_multiple_cmds_from_one_shell_by_std_write(cmds):
    l_cmds = append_exit_cmd(cmds)
    
    # write commands
    p_console = get_cmd_line_process()
    for cmd in l_cmds:
        p_console.stdin.write('%s\n' %(cmd))
        p_console.stdin.flush()
        time.sleep(g_wait_time_between_cmds)

    # handle output    
    output = ''
    matched_key = 'exit'
    max_times = 500
    i = 0
    while (not output.endswith(matched_key)) and (i < max_times):
        char = p_console.stdout.read(1)
        output += char
        i += 1
    
#     print output.decode('gb2312').encode('utf-8')  # format gb2312 to utf-8
    print output.decode('gb2312')  # utf-8 is default

# cannot add sleep time between each command
def run_multiple_cmds_from_one_shell_by_communicate(cmds):
    # build command
    l_cmds = append_exit_cmd(cmds)
    l_cmd = format_cmds_to_cmd_for_communicate(l_cmds)
    
    # run commands
    p_console = get_cmd_line_process()
    outs,errs = p_console.communicate(l_cmd)
    
    # handle output
    output = ''
    for char in outs:
        output += char
    if errs is not None:
        for char in errs:
            output += char

    print output.decode('gb2312')

def get_cmd_line_process():
    cmd_path = r'C:\Windows\system32\cmd.exe'
    return subprocess.Popen(cmd_path, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# --------------------------------------------------------------
#  Main
# --------------------------------------------------------------
def test_run_multiple_cmds():
    cmds = ['java -version', 'echo hi', 'echo zhengjin']
    
    run_multiple_cmds_from_one_shell_by_std_write(cmds)
#     run_multiple_cmds_from_one_shell_by_communicate(cmds)

def run_repeat_shell_send_key_cmds(key, times):
    cmds = ['adb shell']
    cmd = 'input keyevent %s' %(key)
    cmds = append_exit_cmd(build_repeat_cmd(cmds, cmd, times))  # exit shell ENV

    run_multiple_cmds_from_one_shell_by_communicate(cmds)


if __name__ == '__main__':

    test_run_multiple_cmds()
#     run_repeat_shell_send_key_cmds(g_cmd_key_right, 70)
    
    print '%s Done!' %(os.path.basename(__file__))
    pass