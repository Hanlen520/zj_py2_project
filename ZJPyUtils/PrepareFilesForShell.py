# -*- coding: utf-8 -*-
'''
Created on 2016-6-23

@author: zhengjin

Push files to the shell ENV to prepare data for filemanager test.

'''

import os
import time

# ----------------------------------------------------
# Functions
# ----------------------------------------------------
def run_system_cmd(cmd):
    print cmd
    os.system(cmd)

def adb_connect_devices(device_ip):
    cmd = 'adb connect %s' %(device_ip)
    run_system_cmd(cmd)

def verify_device_connected():
    cmd = 'adb get-serialno'
    print cmd
    for line in os.popen(cmd).readlines():
        if 'unknown' in line:
            print 'There is no device connected.'
            exit(1)

def mk_multiple_dirs_on_shell(paths):
    for path in paths:
        mk_dir_on_shell(path)

def mk_dir_on_shell(path):
    cmd = 'adb shell mkdir %s' %(path)
    run_system_cmd(cmd)

def create_sub_dir_and_push_files_to_shell(s_path,t_path):
    t_path = create_sub_dir_on_shell(s_path,t_path)
    push_files_to_shell(s_path,t_path)

def create_sub_dir_on_shell(s_path,t_path):
    dir_name = os.path.basename(s_path)
    t_path = '%s/%s' %(t_path,dir_name)
    mk_dir_on_shell(t_path)
    
    return t_path

def push_files_to_shell(s_path,t_path):
    cmd = 'adb push %s %s' %(s_path,t_path)
    run_system_cmd(cmd)


# ----------------------------------------------------
# Main
# ----------------------------------------------------
def prepare_files_main():
    
    # adb connect
    if g_flag_adb_connect:
        device_ip = '172.17.5.134'
        adb_connect_devices(device_ip)
        time.sleep(3)
        verify_device_connected()
    
    # make directories
    path_root_shell = '/sdcard/testfiles'
    path_pics_shell = '%s/testpics' %(path_root_shell)
    path_apps_shell =  '%s/testapps' %(path_root_shell)
    path_video_shell = '%s/testvideo' %(path_root_shell)
    path_music_shell = '%s/testmusic' %(path_root_shell)
    paths_shell = (path_root_shell,path_pics_shell,path_apps_shell,path_video_shell,path_music_shell)
    if g_flag_mk_dir:
        mk_multiple_dirs_on_shell(paths_shell)

    # push files to shell
    # pictures
    create_sub_dir_and_push_files_to_shell(r'D:\files_test\Pics_200+',path_pics_shell)
    create_sub_dir_and_push_files_to_shell(r'D:\files_test\Pics_20+',path_pics_shell)
    create_sub_dir_and_push_files_to_shell(r'D:\files_test\Pics_4K',path_pics_shell)
    
    # apps
    create_sub_dir_and_push_files_to_shell(r'D:\files_apps\Thrid_part_Apps', path_apps_shell)
    create_sub_dir_and_push_files_to_shell(r'D:\files_test\Apps_ZJ_Test\Dir_SomeApps', path_apps_shell)
    
    # video
    push_files_to_shell(r'"D:\files_test\Videos_ZJ_Test\4K-HD.Club-2013-Taipei 101 Fireworks Trailer.mp4"', path_video_shell)
    push_files_to_shell(r'"D:\files_test\Videos_ZJ_Test\Im Se Jun - Lie.mp4"', path_video_shell)  # include space in path
    push_files_to_shell(r'D:\files_test\Videos_ZJ_Test\XinShu.mp4', path_video_shell)

    # music
    create_sub_dir_and_push_files_to_shell(r'D:\files_test\Music_ZJ_Test\ShortName', path_music_shell)


if __name__ == '__main__':
    
    g_flag_adb_connect = True
    g_flag_mk_dir = True
    prepare_files_main()
    
    print 'Prepare files for shell env, done!'
    pass
