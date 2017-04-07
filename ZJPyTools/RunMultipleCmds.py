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
g_wait_between_cmds = 1

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
def format_cmds_with_new_line_and_ret_str(cmds):
    return '\n'.join(cmds) + '\n'

def format_cmds_with_new_line_and_ret_list(cmds):
    return ('%s\n' % cmd for cmd in cmds)

# --------------------------------------------------------------
#  Run Multiple Commands Utils
# --------------------------------------------------------------
def run_piped_cmds(first_cmd, second_cmd):
    p1 = subprocess.Popen(first_cmd, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p2 = subprocess.Popen(second_cmd, stdin=p1.stdout,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = p2.communicate()
    
    if err is not None:
        print 'Error', err
    if len(out) == 0:
        return 'null'
    return out.replace('\r\n', '\n')

def get_cmd_line_process():
    cmd = r'C:\Windows\system32\cmd.exe'
    return subprocess.Popen(cmd, shell=False, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def run_cmds_by_std_write(cmds):
    ''' run commands in single shell ENV by using stdin.write() '''
    # build commands
    cmds.append('exit')
    cmds = format_cmds_with_new_line_and_ret_list(cmds)
    
    # write commands
    p_shell = get_cmd_line_process()
    for cmd in cmds:
        p_shell.stdin.write(cmd)
        p_shell.stdin.flush()
        time.sleep(g_wait_between_cmds)
    
    # get output
    ret_output = ''
    max_size = 16
    for i in xrange(max_size):
        tmp_str = p_shell.stdout.read(1024)
        if len(tmp_str) == 0:
            break
        ret_output += tmp_str
    
    if len(ret_output) == 0:
        return 'null'
    return ret_output.decode('gbk')  # gbk encode in win shell ENV

def run_cmds_by_communicate(cmds):
    ''' run commands in single shell ENV by using communicate() '''
    # build commands
    cmds.append('exit')
    tmp_cmd = format_cmds_with_new_line_and_ret_str(cmds)
    
    # write commands
    p_shell = get_cmd_line_process()
    out, err = p_shell.communicate(tmp_cmd)
    
    if err is not None:
        print 'Error:', err
    if len(out) == 0:
        return 'null'
    return out.decode('gbk')

# --------------------------------------------------------------
#  Main
# --------------------------------------------------------------
def run_repeat_shell_send_key_cmds(key, times):
    # build commands
    cmds_lst = ['adb shell']
    cmd_input = 'input keyevent ' + key
    cmd_sleep = 'sleep 1'
    for i in xrange(times):
        cmds_lst.append(cmd_input)
        cmds_lst.append(cmd_sleep)
    cmds_lst.append('exit')
    
    run_cmds_by_communicate(cmds_lst)


if __name__ == '__main__':

#     print run_piped_cmds('adb shell ps', 'findstr ott')

    # prefer to use communicate() instead of std_write()
#     cmds1 = ['echo hi', 'java -version', 'ipconfig']
#     print run_cmds_by_std_write(cmds1)
    
    cmds2 = ['echo hi', 'java -version', 'node -v', 'ipconfig']
    print run_cmds_by_communicate(cmds2)

#     run_repeat_shell_send_key_cmds(g_cmd_key_right, 10)
    
    print '%s Done!' % (os.path.basename(__file__))
    pass
