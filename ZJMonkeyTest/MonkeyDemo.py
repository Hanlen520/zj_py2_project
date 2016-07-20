# -*- coding: utf-8 -*-
'''
@author: zhengjin
'''

import os

series_no = r'0807'
local_dir_path = r'd:\monkey_logs' + '\\' + series_no
shell_dir_path = r'/data/local/tmp/monkey_logs' + '/' + series_no

# --------------------------------------------------------------
# functions: logcat
# --------------------------------------------------------------
def clearLogcat():
    cmd = 'adb logcat -c'
    os.system(cmd)

def startLogcat():
    file_name = r'\logcat.txt'

    # for shell -> adb logcat -f /sdcard/monkey_logs/logcat.txt -v time *:i

    log_cmd = 'adb logcat -v time *:i > ' + local_dir_path + file_name
    print log_cmd
#     subprocess.Popen(log_cmd, shell=False)

def stopLogcat():
    cmd = 'adb kill-server'
    os.system(cmd)

# --------------------------------------------------------------
# functions: Anr tarces files
# --------------------------------------------------------------
anr_path = r'/data/anr/traces.txt'

def clearAnrTracesFile():
    cmd = r'adb shell echo > ' + anr_path
    try:
        os.system(cmd)
    except:
        print r'no auth to clear anr traces file.'
        
def moveAnrTracesFile():
    cmd = 'adb shell busybox mv ' + anr_path + ' ' + shell_dir_path
    os.system(cmd)

# --------------------------------------------------------------
# functions: monkey
# --------------------------------------------------------------
def pullTracesFile():
    cmd = 'adb pull ' + shell_dir_path + ' ' + local_dir_path
    os.system(cmd)

# 'pm list packages -s' for system packages
# 'pm list packages -3' for third part packages

def runMonkeyCmd():
    run_time = '100'
    white_list_path = r'/data/local/tmp/whitelist.txt'
    
    monkey_cmd = 'adb shell monkey ' + \
    r'--pkg-whitelist-file '+ white_list_path + ' ' \
    '--throttle 500 ' + \
    '--ignore-crashes --ignore-timeouts --ignore-native-crashes ' + \
    '--kill-process-after-error --monitor-native-crashes ' + \
    '--pct-touch 0 --pct-motion 0 --pct-trackball 0 --pct-nav 55 --pct-majornav 30 --pct-syskeys 5 --pct-appswitch 10 --pct-flip 0 --pct-anyevent 0 ' + \
    '-v -v ' + \
    run_time + ' ' + \
    '2>' + shell_dir_path + r'/monkey_error.txt ' + \
    '1>' + shell_dir_path + r'/monkey_info.txt'
    # monkey_cmd contains sign '>' which conflict with shell

    print monkey_cmd
#     os.system(monkey_cmd)

# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
def Main():
#     clearLogcat()
#     clearAnrTracesFile()
#     startLogcat()

    runMonkeyCmd()

#     stopLogcat()
#     moveAnrTracesFile()
#     pullTracesFile()

    print 'monkey case done!'

if __name__ == '__main__':
    
    Main()
    pass